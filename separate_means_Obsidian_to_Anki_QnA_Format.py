import os
import re

''' 읽어들이는 파일의 한 줄에 대한 가정
읽어들이는 파일의 한 줄은 ' - ' or '- ' + Front : Back1-1, Back1-2; Back2; Back3; ... #front_back\n'와 같다고 가정한다.
위 문자열에 표기된 공백(' ')은 공백 하나를 반드시 포함한 white space(여기서, white space는 [ \t\n\r\f\v] 이다.)들의 모음을 의미한다.
'''

file_path = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE - iCloud Drive/1 Project/Language - English - 해커스 토익 Reading 공부하기/1 GRAMMAR PART 5, 6/3-2-1 토익 공식 2-1-1 동명사를 목적어로 갖는 동사.md"
parent_path = os.path.dirname(file_path)

word_mean_list_dict = {}

with open(file_path, 'r') as f:
    file_line = f.readline()
    
    while(file_line != ""):
        if file_line[-1-11-1:] != " #front_back\n":
            file_line = f.readline()
            continue
        
        # ' #front_back\n' 제거
        file_line = file_line.replace(' #front_back\n', '')
        #  1개 이상의 white space(r"\s+")를 ' '로 바꿈.(\s는 white space(파이썬 re 모듈에서 [ \t\n\r\f\v]가 white space이다.)를 의미함.)
        file_line = re.sub(r"\s+", " ", file_line)
        # 맨 앞에 있는 '- ' or ' - '를 없앰
        first_hyphen_idx = file_line.find('-'); file_line = file_line[first_hyphen_idx+2:]
        # 단어(문자열)와 뜻 모음(배열)로 나눔
        word = file_line.split(": ")[0]
        mean_list = file_line.split(": ")[1].split("; ") # ';'가 없어도 전체 문자열을 포함한 리스트 반환
        # 나눈 단어와 뜻 모음을 딕셔너리에 저장
        word_mean_list_dict[word] = mean_list
        
        file_line = f.readline()

with open(parent_path + '/' + "QnA_Format_separated_means.md", 'w') as f:
    for word, mean_list in word_mean_list_dict.items():
        mean_list_length = mean_list.__len__()
        for order, mean in enumerate(mean_list):
            if  mean_list_length >= 2:
                f.write("Q: " + word + str(order+1) + '\n')
                f.write("A: " + mean + '\n')
                f.write('\n')
            else:
                f.write("Q: " + word + '\n')
                f.write("A: " + mean + '\n')
                f.write('\n')
