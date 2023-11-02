# README
[README](README.md)

# Python
[create_mean_cloze_in_hackers_voca.py](create_mean_cloze_in_hackers_voca.py)는 관련 파일 하나에서만 단어에 cloze를 만든다. ','와 '\n' 구분되었다면 다른 cloze이다.

[hackers_toeic_voca_insert_gtts.py](hackers_toeic_voca_insert_gtts.py)는 관련 파일 하나에서만 단어와 예문에 tts를 만든다.

아래의 3개 파일은 쓰이지 않는 파이썬 파일이다.

[hackers_toeic_voca_insert_gtts_in_directory.py](hackers_toeic_voca_insert_gtts_in_directory.py)는 [hackers_toeic_voca_insert_gtts.py](hackers_toeic_voca_insert_gtts.py)처럼 관련 파일 하나에서만 단어와 예문에 tts를 만들지 않는다. 관련 파일을 담고 있는 폴더 경로를 변수로 넘겨주면 관련 파일 모두에서 단어와 예문에 tts를 만든다. 관련 파일 1개마다 tts를 만들 것이므로 필요하지 않다.

gtts의 request 제한으로 일괄적으로 tts를 못 만드는 것도 있고, 일괄적으로 tts를 만든다고 해도 MD 단어 뜻 파일의 내용을 바로 Anki로 옮기지 않으니 딱히 필요가 없다.

Obsidian에서 Anki로 내보내는 Obsidian_to_Anki의 정규식 표현 중에 QnA 포맷이라는 것이 있는데 [separate_means_Obsidian_to_Anki_QnA_Format.py](separate_means_Obsidian_to_Anki_QnA_Format.py)는 파일 경로를 넘겨주면 특정 패턴를 QnA 포맷으로 바꾸어 준다.

기본 카드만 가진 덱의 카드 단어 뜻을 파일로 내보낸 후 [hackers_toeic_voca_mix_word.py](hackers_toeic_voca_mix_word.py)를 이용해 그 파일을 이용해 단어와 뜻을 섞어 문제, 답변을 만든다.

# Folder
```dataview
TABLE file.mday as 수정일, file.cday as 생성일, file.size as "파일 크기"
WHERE
	length(split(regexreplace(replace(file.folder, this.file.folder, ""), "^/", ""),  "/")) = 1
	AND startswith(file.name, "0 ")
	AND startswith(file.folder, this.file.folder)
	AND file.name != this.file.name
SORT file.name ASC
```

# MD File
```dataview
TABLE file.mday as 수정일, file.cday as 생성일, file.size as "파일 크기"
WHERE
	file.folder = this.file.folder
	AND file.name != this.file.name
	AND !regexmatch(".* - (웹 클립|유튜브)$", file.name)
SORT file.mday DESC
```

# Layer 0
```dataview
TABLE file.mday as 수정일, file.cday as 생성일, file.size as "파일 크기"
WHERE
	file.folder = this.file.folder
	AND file.name != this.file.name
	AND regexmatch(".* - (웹 클립|유튜브)$", file.name)
SORT file.mday DESC
```
