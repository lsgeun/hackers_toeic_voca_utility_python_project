import os
import re
from gtts import gTTS

def save_tts_mp3(md_file_path, source, file_name_prefix):
    '''
    md_file_path에서 {현재 폴더 경로}와 {md 파일명}을 추출하여 '{현재 폴더 경로}/0 Attachment/{md 파일명}/'에 호주, 영국, 미국로 tts한 source를 file_name_prefix 이용한 파일명으로 mp3 파일로 저장
    
    '{현재 폴더 경로}/0 Attachment/{현재 파일명}/' 경로상에 폴더가 존재하지 않는다면 폴더 생성
    '''
    global current_directory_path
    
    # '{현재 폴더 경로}/0 Attachment'에 위치한 mp3 파일이 저장될 폴더 이름
    md_file_name_no_ext = os.path.basename(md_file_path).split('.')[0]
    
    # '{현재 폴더 경로}/0 Attachment/' 폴더가 존재하지 않는다면 생성
    if not os.path.isdir(f"{current_directory_path}/0 Attachment"):
        os.system(f"mkdir \"{current_directory_path}/0 Attachment\"")
    # '{현재 폴더 경로}/0 Attachment/{md 파일명}/' 폴더가 존재하지 않는다면 생성
    if not os.path.isdir(f"{current_directory_path}/0 Attachment/{md_file_name_no_ext}"):
        os.system(f"mkdir \"{current_directory_path}/0 Attachment/{md_file_name_no_ext}\"")
    
    # 호주, 영국, 미국에 대한 tts 값을 '{현재 폴더 경로}/0 Attachment/{md 파일명}/' 폴더에 각각 'file_name_prefix_{aust|uk|us}.mp3'로 저장
    # 속도를 위해 mp3 파일이 없을 경우에만 tts를 요청하여 mp3 파일 생성
    if not os.path.isfile(f"{current_directory_path}/0 Attachment/{md_file_name_no_ext}/{file_name_prefix}_aust.mp3"):
        aust = gTTS(text=source, lang='en', tld='com.au', slow=False)
        aust.save(f"{current_directory_path}/0 Attachment/{md_file_name_no_ext}/{file_name_prefix}_aust.mp3")
    if not os.path.isfile(f"{current_directory_path}/0 Attachment/{md_file_name_no_ext}/{file_name_prefix}_uk.mp3"):
        uk = gTTS(text=source, lang='en', tld='co.uk', slow=False)
        uk.save(f"{current_directory_path}/0 Attachment/{md_file_name_no_ext}/{file_name_prefix}_uk.mp3")
    if not os.path.isfile(f"{current_directory_path}/0 Attachment/{md_file_name_no_ext}/{file_name_prefix}_us.mp3"):
        us = gTTS(text=source, lang='en', tld='us', slow=False)
        us.save(f"{current_directory_path}/0 Attachment/{md_file_name_no_ext}/{file_name_prefix}_us.mp3")

def insert_word_tts_mp3_file_link():
    # 전역 변수 선언
    global word, word_match, search_entrance_index, insert_index, md_file_path, file_lines, current_directory_path, md_file_name_no_ext
    # 단어를 포함한 줄을 word에 할당, search_entrance_index, insert_index를 변경시키기 위함
    word = word_match.group(0)
    # search_entrance_index, insert_index를 현재 word의 end 위치로 변경
    search_entrance_index = word_match.start(); search_entrance_index += len(word)
    insert_index = word_match.start(); insert_index += len(word)
    
    # 단어만 word에 할당, tts를 적용시키기 위함
    word = re.sub(r"#{2,}?\s+?", "", word); word = re.sub(r"\n", "", word)
    
    # tts mp3 파일의 존재성 여부를 변수에 할당
    existence_of_tts_mp3_file_path = True
    
    tts_mp3_file_paths = [f"{current_directory_path}/0 Attachment/{md_file_name_no_ext}/{word}_aust.mp3", f"{current_directory_path}/0 Attachment/{md_file_name_no_ext}/{word}_uk.mp3", f"{current_directory_path}/0 Attachment/{md_file_name_no_ext}/{word}_us.mp3"]
    
    for tts_mp3_file_path in tts_mp3_file_paths:
        if not os.path.isfile(tts_mp3_file_path):
            existence_of_tts_mp3_file_path = False
            break
    # tts mp3 파일이 존재하지 않는다면 파일 생성
    if not existence_of_tts_mp3_file_path:
        save_tts_mp3(md_file_path=md_file_path, source=word, file_name_prefix=word)
    # tts mp3 파일 링크의 존재성 여부를 변수에 할당
    tts_mp3_file_link = "호주 " + f"![{word}_aust.mp3](0 Attachment/{md_file_name_no_ext}/{word}_aust.mp3)".replace(' ', "%20") + " 영국 " + f"![{word}_uk.mp3](0 Attachment/{md_file_name_no_ext}/{word}_uk.mp3)".replace(' ', "%20") + " 미국 " + f"![{word}_us.mp3](0 Attachment/{md_file_name_no_ext}/{word}_us.mp3)".replace(' ', "%20") + '\n'; 
    
    existence_of_tts_mp3_file_link = False if file_lines.find(tts_mp3_file_link, insert_index) == -1 else True;
    # tts mp3 파일 링크가 존재하지 않는다면 링크 생성
    if not existence_of_tts_mp3_file_link:
        file_lines = file_lines[:insert_index] + tts_mp3_file_link + file_lines[insert_index:]
    
    # search_entrance_index를 삽입된 tts_file_link의 end 위치로 변경
    search_entrance_index += len(tts_mp3_file_link)

def insert_example_sentence_tts_mp3_file_link():
    # 전역 변수 선언
    global example_sentence_match, example_sentence_pattern, file_lines, search_entrance_index, insert_index, md_file_path, file_lines, word, current_directory_path, md_file_name_no_ext
    # 예문 문자열 할당
    # 예문 패턴으로 찾은 문자열에 대한 매치
    example_sentence_match = example_sentence_pattern.search(file_lines, pos=search_entrance_index)
    # 예문 문자열, '### 예문\n...#'에서 '...'에 해당하는 부분
    example_sentence = example_sentence_match.group(0)
    # 예문에 ID가 있다면 없앰
    # 참고로, ID는 맨 마지막에 있음
    example_sentence = re.sub(r"<!--.+?-->\n", '', example_sentence)
    # 예문에 mp3 파일 링크가 있다면 없앰
    example_sentence = re.sub(r"\t- 호주.*?\n", '', example_sentence)
    # 예문에 2번 이상의 '\n'를 '\n'로 바꿈
    example_sentence = re.sub(r"\n{2,}", '\n', example_sentence)
    
    # search_entrance_index, insert_index를 매치 시작 위치로 변경
    search_entrance_index = example_sentence_match.start(); insert_index = example_sentence_match.start()
    
    # 예문 줄 수
    line_count = example_sentence.count('\n')
    # 예문 줄 수//2(= 영어로 된 문장이 있는 수) 만큼 반복
    for i in range(line_count//2):
        # 2*i 번째 예문
        example_sentence_2i_th = example_sentence.split('\n')[2*i]; example_sentence_2i_th += '\n'
        
        # * search_entrance_index, insert_index를 2*i 번째 예문의 end 위치로 변경
        search_entrance_index += len(example_sentence_2i_th)
        insert_index += len(example_sentence_2i_th)
        
        # 2*i 번째 예문의 '\s*?-\s*?', '\n+' 부분을 없앰
        example_sentence_2i_th = re.sub(r"\s*?-\s*?", "", example_sentence_2i_th)
        example_sentence_2i_th = re.sub(r"\n+?", "", example_sentence_2i_th)
        
        # tts mp3 파일의 존재성 여부를 변수에 할당
        existence_of_tts_mp3_file_path = True

        tts_mp3_file_paths = [f"{current_directory_path}/0 Attachment/{md_file_name_no_ext}/{word}_example_sentence{i+1}_aust.mp3", f"{current_directory_path}/0 Attachment/{md_file_name_no_ext}/{word}_example_sentence{i+1}_uk.mp3", f"{current_directory_path}/0 Attachment/{md_file_name_no_ext}/{word}_example_sentence{i+1}_us.mp3"]

        for tts_mp3_file_path in tts_mp3_file_paths:
            if not os.path.isfile(tts_mp3_file_path):
                existence_of_tts_mp3_file_path = False
                break
        # tts mp3 파일이 존재하지 않는다면 파일 생성
        if not existence_of_tts_mp3_file_path:
            save_tts_mp3(md_file_path=md_file_path, source=example_sentence_2i_th, file_name_prefix=f"{word}_example_sentence{i+1}")
        
        # tts mp3 파일 링크의 존재성 여부를 변수에 할당
        tts_mp3_file_link = "\t- 호주 " + f"![{word}_example_sentence{i+1}_aust.mp3](0 Attachment/{md_file_name_no_ext}/{word}_example_sentence{i+1}_aust.mp3)".replace(' ', "%20") + " 영국 " + f"![{word}_example_sentence{i+1}_uk.mp3](0 Attachment/{md_file_name_no_ext}/{word}_example_sentence{i+1}_uk.mp3)".replace(' ', "%20") + " 미국 " + f"![{word}_example_sentence{i+1}_us.mp3](0 Attachment/{md_file_name_no_ext}/{word}_example_sentence{i+1}_us.mp3)".replace(' ', "%20") + '\n'; 
        
        existence_of_tts_mp3_file_link = False if file_lines.find(tts_mp3_file_link, insert_index) == -1 else True;
        # tts mp3 파일 링크가 존재하지 않는다면 링크 생성
        if not existence_of_tts_mp3_file_link:
            file_lines = file_lines[:insert_index] + tts_mp3_file_link + file_lines[insert_index:]
        
        # * search_entrance_index, insert_index를 삽입된 tts_mp3_file_link의 end 위치로 변경
        search_entrance_index += len(tts_mp3_file_link)
        insert_index += len(tts_mp3_file_link)
        
        # 2*i + 1 번째 예문
        example_sentence_2i_plus_1_th = example_sentence.split('\n')[2*i + 1]; example_sentence_2i_plus_1_th += '\n'
        # * search_entrance_index, insert_index를 2*i + 1 번째 예문의의 end 위치로 변경
        search_entrance_index += len(example_sentence_2i_plus_1_th)
        insert_index += len(example_sentence_2i_plus_1_th)

# 파일 및 부모 폴더 경로와 파일명(확장자 있는 것과 없는 것)을 변수로 받음
md_file_path = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE-iCloud_Drive/1 Projects/해커스 토익 Reading/1 GRAMMAR PART 5, 6/1-2-3-3 목적격 보어를 갖는 동사.md"

current_directory_path = os.path.dirname(md_file_path)
md_file_name = md_file_path.split('/')[-1]; md_file_name_no_ext = md_file_name[:-3]
# 파일의 내용을 읽어서 하나의 문자열로 저장함
file_lines = None
with open(md_file_path, 'r') as f:
    file_lines = f.readlines()
    file_lines = "".join(file_lines)

# 예문과 단어를 찾기 위한 정규식 패턴
example_sentence_pattern = re.compile(r"(?<=### 예문\n)(?:.*?\n)+?(?=#)")
word_pattern = re.compile(r"#{2,}? [a-zA-Z]+?.*?\n")

# 다음 패턴을 찾기 위한 첫 인덱스, 찾은 패턴 이후를 탐색하기 위해 패턴을 찾을 때마다 인덱스가 늘어남
search_entrance_index = None
# 문자열을 삽입하려는 위치
insert_index = None
# 단어 패턴으로 찾은 문자열에 대한 패치
word_match = word_pattern.search(file_lines, pos=0)
# 탐색 종료 여부를 나타내는 변수
ternimation_of_search = False

# 패턴으로 문자열을 찾지 못할 때까지 반복
while(word_match is not None):
    # * 단어
    insert_word_tts_mp3_file_link()
    # * 예문
    insert_example_sentence_tts_mp3_file_link()
    
    # word_pattern으로 word에 대한 word_match 변수 정의
    word_match = word_pattern.search(file_lines, pos=search_entrance_index)
    # word_pattern를 찾지 못하면 에러 메세지를 띄우고 while문 탈출
    # ternimation_of_search를 참으로 만듦
    if word_match is None:
        ternimation_of_search = True
    # ternimation_of_search가 참이므로 while문 탈출
    if ternimation_of_search:
        break
    # word_match으로 word 변수 정의
    word = word_match.group(0)
    
    # word_pattern으로 찾은 word가 하위 단어인지 검사하는 word_prefix_match 변수 정의
    word_prefix_match = re.search(r"^#{4,}", word)
    # word가 하위 단어일 동안 반복
    while(word_prefix_match is not None):
        # * 하위 단어
        insert_word_tts_mp3_file_link()
        
        # word_pattern으로 word에 대한 word_match 변수 정의
        word_match = word_pattern.search(file_lines, pos=search_entrance_index)
        # word_pattern를 찾지 못하면 에러 메세지를 띄우고 while문 탈출
        # ternimation_of_search를 참으로 만듦
        if word_match is None:
            ternimation_of_search = True
            break
        # word_match으로 word 변수 정의
        word = word_match.group(0)
        
        # word_pattern으로 찾은 word가 하위 단어인지 검사하는 word_prefix_match 변수 정의
        word_prefix_match = re.search("^#{4,}", word)
        
    # ternimation_of_search가 참이므로 while문 탈출
    if ternimation_of_search:
        break

# 모든 링크를 기입한 file_lines를 md_file 파일에 저장
with open(md_file_path, 'w') as f:
    f.writelines(file_lines)
