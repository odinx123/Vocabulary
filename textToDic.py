import string

def is_not_english(word):
    # 檢查單詞中的每個字元是否都是英文字母、數字或特殊符號
    for char in word:
        if char not in string.ascii_letters and not char.isdigit() and char not in string.punctuation:
            return True
    return False

def read_txt_file(file_path):
    word_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 移除每一行中的換行符號
            line = line.strip().split()
            # 如果行是空的，則跳過
            if not line:
                continue
            
            # 拆分單詞和翻譯
            first_chi_idx = len(line)
            for i, word in enumerate(line):
                if is_not_english(word):  # 如果單詞不是英文，則為翻譯
                    first_chi_idx = i
                    break
            #print(line, first_chi_idx)
            english_word = line[:first_chi_idx]
            translation = line[first_chi_idx:]
            
            # 將單詞和翻譯添加到字典中
            word_dict[' '.join(english_word)] = ' '.join(translation)
    
    return word_dict
        
if __name__ == '__main__':
    # 指定要讀取的txt文件路徑
    file_path = 'words.txt'

    # 讀取txt文件並將單詞和翻譯存儲到字典中
    word_dictionary = read_txt_file(file_path)
    for word, translation in word_dictionary.items():
        print(f"{word}: {translation}")
