from random import randint
import sys
import os

# 1. 매개변수로 path를 지정할 때
# path = sys.argv[1]
# 2. 전역변수로 path를 지정할 때
path = "/Users/isgeun/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOTE - iCloud Drive/1 Project/Language - English - 해커스 토익 보카 단어 외우기/시험/해커스 토익 기출 보카__Day 04 업무 노하우 - 일반사무 2.md"
current_directory = os.path.dirname(path)
file_name_prefix = os.path.basename(path).split('.')[0]

if __name__ == "__main__":
    word_mean_file = open(path, "r")
    
    duplicated_word_means = word_mean_file.readlines()
    # word_mixed_mean_lists_dict 생성
    word_mixed_mean_lists_dict = {}
    # word(key)에 대한 value를 mean이 차례대로 넣어진 리스트 형태(mean_list)로 만들기
    for word_mean in duplicated_word_means:
        word = word_mean.split('\t')[0]
        mean = word_mean.split('\t')[1][:-1] # [:-1] -> '\n' 제외
        
        key_list = list(word_mixed_mean_lists_dict.keys())
        if word in key_list:
            word_mixed_mean_lists_dict[word].append(mean)
        else:
            word_mixed_mean_lists_dict[word] = [mean]
    # mean_list 섞기
    for word in word_mixed_mean_lists_dict:
        mean_list = word_mixed_mean_lists_dict[word]
        
        mix_mean_list = []
        initial_length_of_means_list = len(mean_list)
        for _ in range(initial_length_of_means_list):
            random_index = randint(0, len(mean_list)-1)
            random_mean = mean_list.pop(random_index)
            mix_mean_list.append(random_mean)
        word_mixed_mean_lists_dict[word] = mix_mean_list
    # word_mixed_means 생성 
    word_mixed_means_list = []
    for word in word_mixed_mean_lists_dict:
        word_mixed_means = ""
        word_mixed_means += word + " "
        for mean in word_mixed_mean_lists_dict[word]:
            word_mixed_means += mean + ", "
        word_mixed_means = word_mixed_means[:-2] + '\n'
        
        word_mixed_means_list.append(word_mixed_means)
    # mixed_word_mixed_means 생성 및 단어와 뜻 파일 생성
    mixed_word_mixed_means = []
    initial_length_of_word_mixed_means = len(word_mixed_means_list)
    for _ in range(initial_length_of_word_mixed_means):
        random_index = randint(0, len(word_mixed_means_list)-1)
        random_word = word_mixed_means_list.pop(random_index)
        mixed_word_mixed_means.append(random_word)
    with open(f"{current_directory}/{file_name_prefix} word and means.md", "w") as f:
        f.writelines(mixed_word_mixed_means)
    # create mixed words 생성 및 단어 파일 생성
    mixed_words = []
    for word_mixed_mean in mixed_word_mixed_means:
        end_of_word_index = -1
        for i, word_mixed_mean_char in enumerate(word_mixed_mean):
            # ord 부분은 영어임을 확인하는 부분, 영어와 영어가 아닌 것(한글 포함)을 구분하기 위해 작성함.
            if word_mixed_mean_char == ' ' and not ord('a') <= ord(word_mixed_mean[i+1].lower()) <= ord('z'):
                end_of_word_index = i
                break
        mixed_words.append(word_mixed_mean[0:end_of_word_index] + ' \n')
    with open(f"{current_directory}/{file_name_prefix} words.md", "w") as f:
        f.writelines(mixed_words)   
