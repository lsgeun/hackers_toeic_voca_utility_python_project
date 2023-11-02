import os
import re

# * 공통적으로 필요한 변수를 전역 변수로 선언
# 현재 파일 경로와 현재 폴더 경로를 정의
md_file_path = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE-iCloud_Drive/1 Projects/해커스 토익 기출 보카/2 Day 02 드레스코드 - 규칙 법률.md"
current_directory_path = os.path.dirname(md_file_path)

# file_lines에서 word_means를 찾아내기 위한 패턴
word_means_pattern = re.compile(r"(#{2,}?) [a-zA-Z]+?.*?\n(?:.*?\n)+?(?=#)", re.MULTILINE)
# means에서 mean을 찾아내기 위한 패턴
# ','나 '\n'로 구분된 1개 이상의 문자열을 찾음.
mean_pattern = re.compile(r"[^,\n]+")
# mean에서 cloze를 찾아내기 위한 패턴
cloze_pattern = re.compile(r"{(\d+)\|.+?}")

# means에서 정규식을 찾을 때의 시작 인덱스
means_cloze_search_index = None
# means에 쓰일 cloze를 만들 때 쓰는 인덱스
current_cloze_index = 1

# mean 바로 앞 공백 인덱스
front_spacebar_index = None
# mean 바로 뒤 공백 인덱스
back_spacebar_index = None

# * 파일을 문자열로 불러오기
file_lines = None
with open(md_file_path, 'r') as f:
    file_lines = f.readlines()
    file_lines = "".join(file_lines)

# * file_line에서 word_means을 찾아낸 후 word_means의 각 means에 cloze 넣기
word_means_match = word_means_pattern.search(file_lines, 0)
while word_means_match:
    # * word_means에서 means, means_cloze를 만듦
    # word_means에서 means 구하기
    word_means = word_means_match.group(0)
    # word_means에서 word, tts, Anki ID, 맨 마지막 줄 바꿈을 모두 없애 means를 만듦.
    means = re.sub(r"#+? [a-zA-Z]+?.*?\n", "", word_means)
    means = re.sub(r"호주.+?\n", "", means)
    means = re.sub(r"<!--ID:.+?\n", "", means)
    means = re.sub(r"\n+?$", "", means)
    # means_cloze을 means으로 초기화한 후 means_cloze에서 mean에 cloze를 넣음
    means_cloze = means
    
    # * current_cloze_index 찾기
    ## * mean_cloze_index의 최대값 구해 current_cloze_index에 할당
    # word의 제목의 깊이
    word_heading_depth = len(word_means_match.group(1))
    # word_heading_depth가 2일 때만
    if word_heading_depth == 2:
        # means에 쓰일 cloze를 만들 때 쓰는 인덱스
        current_cloze_index = 1
    
    # word_means를 찾았을 때 current_cloze_index 시작 값
    start_cloze_index = current_cloze_index
    # * means_cloze에서 각 mean에 cloze 넣기
    # means_cloze에 더해진 문자의 개수
    added_char_count = 0
    # means_cloze_search_index 위치를 0으로 초기화
    means_cloze_search_index = 0
    
    mean_match = mean_pattern.search(means_cloze, means_cloze_search_index)
    while mean_match:
        mean = mean_match.group(0)
        
        # * mean에 cloze가 존재한다면 다음 mean을 찾아봄
        # mean에 cloze가 존재하는지 확인하는 변수
        cloze_match = re.search(cloze_pattern, mean)
        if cloze_match:
            # means_cloze_search_index를 다음 위치로 이동
            means_cloze_search_index = mean_match.end(0)
            # 다음 mean_match 구함
            mean_match = mean_pattern.search(means_cloze, means_cloze_search_index)
            continue
        
        # * 공백 인덱스를 구함.
        # front_spacebar_index를 찾음
        front_spacebar_index = None
        for i, mean_char in enumerate(mean):
            if not (mean_char == ' '):
                break
            else:
                front_spacebar_index = i
        
        # back_spacebar_index를 찾음
        back_spacebar_index = None
        # mean[::-1]는 mean을 거꾸로 뒤집은 것
        for i, mean_char in enumerate(mean[::-1]):
            if not (mean_char == ' '):
                break
            else:
                back_spacebar_index = len(mean)-1 - i
        
        # * 앞 뒤 공백을 이용해 mean에 cloze를 넣음
        if not (front_spacebar_index == None) and not (back_spacebar_index == None):
            mean = mean[:front_spacebar_index + 1] + "{" + str(current_cloze_index) + "|" + mean[front_spacebar_index + 1:back_spacebar_index] + "}" + mean[back_spacebar_index:]
        elif front_spacebar_index == None and not (back_spacebar_index == None):
            mean = "{" + str(current_cloze_index) + "|" + mean[:back_spacebar_index] + "}" + mean[back_spacebar_index:]
        elif not (front_spacebar_index == None) and back_spacebar_index == None:
            mean = mean[:front_spacebar_index + 1] + "{" + str(current_cloze_index) + "|" + mean[front_spacebar_index + 1:] + "}"
        else:
            mean = "{" + str(current_cloze_index) + "|" + mean + "}"
        
        # * means_cloze_search_index와 current_cloze_index를 다음 위치로 이동
        # cloze_index의 자릿수를 구함
        cloze_index_digit_count = 1
        quotient = current_cloze_index // 10
        while not (quotient == 0):
            cloze_index_digit_count += 1
            quotient = quotient // 10
        # means_cloze_search_index를 mean의 마지막 위치에 추가된 문자의 개수만큼 더 더해서 할당
        means_cloze_search_index = mean_match.end(0) + 3 + cloze_index_digit_count
        
        # current_cloze_index에 1을 더함
        current_cloze_index += 1
        
        # * added_char_count에 means_cloze에 추가된 문자 개수를 더함
        added_char_count += 3 + cloze_index_digit_count
        
        # * means_cloze의 mean을 cloze를 넣은 mean으로 대체
        means_cloze = means_cloze[:mean_match.start(0)] + mean + means_cloze[mean_match.end(0):]
        
        # * 다음 mean_match 구함
        mean_match = mean_pattern.search(means_cloze, means_cloze_search_index)
    
    # * means_cloze에서 소괄호 안의 '}', '{\d+?\|' 부분을 없애고 없앤 개수 만큼 added_char_count 차감.
    means_cloze_search_index = 0
    cloze_match = cloze_pattern.search(means_cloze, means_cloze_search_index)
    while cloze_match:
        cloze = cloze_match.group(0)
        
        # cloze가 왼쪽 소괄호를 가지는지 알려주는 변수
        left_parentheses_index = cloze.find('(')
        cloze_has_left_parentheses = (left_parentheses_index >= 0)
        # cloze가 오른쪽 소괄호를 가지는 알려주는 변수
        right_parentheses_index = cloze.find(')')
        cloze_has_right_parentheses = (right_parentheses_index >= 0)
        
        # * cloze가 왼쪽 소괄호(left_parentheses)를 가지지 않을 때 다음 cloze로 탐색
        if not cloze_has_left_parentheses:
            means_cloze_search_index = cloze_match.end(0)
            cloze_match = cloze_pattern.search(means_cloze, means_cloze_search_index)
            continue
        
        # * cloze가 왼쪽 소괄호(left_parentheses)와 오른쪽 소괄호(right_parentheses)를 모두 가질 때 다음 cloze로 탐색
        if cloze_has_left_parentheses and cloze_has_right_parentheses:
            means_cloze_search_index = cloze_match.end(0)
            cloze_match = cloze_pattern.search(means_cloze, means_cloze_search_index)
            continue
        
        # * 왼쪽 소괄호(left_parentheses)를 가진 cloze의 가장 마지막 오른쪽 중괄호(right brace) 제거
        # means_cloze에 추가된 문자 개수를 1 뺌
        added_char_count -= 1
        # means_cloze_search_index를 위치를 왼쪽으로 한 칸 이동
        means_cloze_search_index = cloze_match.end(0) - 1
        
        # cloze에서 가장 마지막 중괄호 제거
        cloze = cloze[:-1]
        
        # * means_cloze의 cloze을 변경된 cloze으로 대체
        means_cloze = means_cloze[:cloze_match.start(0)] + cloze + means_cloze[cloze_match.end(0):]
        
        # * 다음 cloze를 탐색
        cloze_match = cloze_pattern.search(means_cloze, means_cloze_search_index)
        cloze = cloze_match.group(0)
        
        # * cloze가 오른쪽 소괄호(right_parentheses)를 가지지 않는 동안 cloze_prefix('{\d+?\|') , '}'를 모두 제거
        # cloze가 오른쪽 소괄호(right_parentheses)를 가지는지 판단하는 변수 할당
        right_parentheses_index = cloze.find(')')
        cloze_has_right_parentheses = (right_parentheses_index >= 0)
        while not cloze_has_right_parentheses:            
            # * cloze의 cloze_prefix('^{\d+?\|') 제거
            # cloze에서 cloze_prefix 찾기
            cloze_prefix_pattern = re.compile(r"^{\d+?\|")
            cloze_prefix_match = cloze_prefix_pattern.search(cloze)
            cloze_prefix = cloze_prefix_match.group(0)
            # means_cloze에 추가된 문자 개수를 cloze_prefix 길이 만큼 뺌
            added_char_count -= len(cloze_prefix)
            # means_cloze_search_index를 위치를 왼쪽으로 cloze_prefix 길이 만큼 이동
            means_cloze_search_index = cloze_match.end(0) - len(cloze_prefix)
            
            # cloze의 cloze_prefix('^{\d+?\|') 제거
            cloze = re.sub(r"^{\d+?\|", "", cloze)
            
            # * cloze의 가장 마지막 오른쪽 중괄호(right brace) 제거
            # means_cloze에 추가된 문자 개수를 1 뺌
            added_char_count -= 1
            # means_cloze_search_index를 위치를 왼쪽으로 한 칸 이동
            means_cloze_search_index = means_cloze_search_index - 1
            
            # cloze에서 가장 마지막 중괄호 제거
            cloze = cloze[:-1]
            
            # * means_cloze의 cloze을 변경된 cloze으로 대체
            means_cloze = means_cloze[:cloze_match.start(0)] + cloze + means_cloze[cloze_match.end(0):]
            
            # * 다음 cloze를 탐색
            cloze_match = cloze_pattern.search(means_cloze, means_cloze_search_index)
            cloze = cloze_match.group(0)
            # cloze가 오른쪽 소괄호(right_parentheses)를 가지는지 판단하는 변수 할당
            right_parentheses_index = cloze.find(')')
            cloze_has_right_parentheses = (right_parentheses_index >= 0)
        
        # * 오른쪽 소괄호(right_parentheses)를 가진 cloze의 cloze_prefix('^{\d+?\|') 제거
        # cloze에서 cloze_prefix 찾기
        cloze_prefix_pattern = re.compile(r"^{\d+?\|")
        cloze_prefix_match = cloze_prefix_pattern.search(cloze)
        cloze_prefix = cloze_prefix_match.group(0)
        # means_cloze에 추가된 문자 개수를 cloze_prefix 길이 만큼 뺌
        added_char_count -= len(cloze_prefix)
        # means_cloze_search_index를 위치를 왼쪽으로 cloze_prefix 길이 만큼 이동
        means_cloze_search_index = cloze_match.end(0) - len(cloze_prefix)
        
        # cloze의 cloze_prefix('^{\d+?\|') 제거
        cloze = re.sub(r"^{\d+?\|", "", cloze)
        
        # * means_cloze의 cloze을 변경된 cloze으로 대체
        means_cloze = means_cloze[:cloze_match.start(0)] + cloze + means_cloze[cloze_match.end(0):]
        
        # * 다음 cloze를 탐색
        cloze_match = cloze_pattern.search(means_cloze, means_cloze_search_index)
    
    # * means_cloze에 속한 cloze의 인덱스를 1부터 차례대로 부여
    if word_heading_depth == 2:
        current_cloze_index = 1
    else:
        current_cloze_index = start_cloze_index
    
    means_cloze_search_index = 0
    cloze_match = cloze_pattern.search(means_cloze, means_cloze_search_index)
    while cloze_match:
        cloze_index = int(cloze_match.group(1))
        
        # modified_char_count는 문자가 1개 이상 추가되었다면 양수, 문자가 1개 이상 삭제되었다면 음수, 문자 수에 변동이 없다면 0이다.
        modified_char_count = len(str(current_cloze_index)) - len(str(cloze_index))
        # means_cloze에 추가된 문자 개수를 modified_char_count 만큼 더함
        added_char_count += modified_char_count
        # means_cloze_search_index를 위치를 왼쪽으로 modified_char_count 길이 만큼 이동
        means_cloze_search_index = cloze_match.end(0) + modified_char_count
        
        # * means_cloze에 속한 cloze의 cloze_index을 current_cloze_index으로 대체
        means_cloze = means_cloze[:cloze_match.start(1)] + str(current_cloze_index) + means_cloze[cloze_match.end(1):]
        
        # current_cloze_index를 1 증가시킴
        current_cloze_index += 1
        
        # * 다음 cloze를 탐색
        cloze_match = cloze_pattern.search(means_cloze, means_cloze_search_index)
    
    # * file_lines에서 means를 means_cloze로 대체
    # file_lines에서 word_means를 찾은 시작점부터 끝점까지를 탐색 범위로 해서 means를 탐색 후
    # means의 시작점과 끝점을 변수에 할당
    start_index_of_means = file_lines.find(means, word_means_match.start(0), word_means_match.end(0))
    end_index_of_means = start_index_of_means + len(means)
    # means의 시작점과 끝점을 이용해 file_lines의 means 위치에 means 대신 means_cloze를 삽입
    file_lines = file_lines[:start_index_of_means] + means_cloze + file_lines[end_index_of_means:]

    # * 다음 word_means_match 구함
    word_means_match = word_means_pattern.search(file_lines, word_means_match.end(0) + added_char_count)

with open(md_file_path, 'w') as f:
    f.writelines(file_lines)
