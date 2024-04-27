from TranslationSpeech import translate_text, text_to_speech, dectect_lang
import tkinter as tk
import threading
import mainFrame
import time

class Page(tk.Frame):
    def __init__(self, app, word_dic):
        self.app = app
        self.app.title("單字卡")

        # self.app.protocol("WM_DELETE_WINDOW", self.on_closing)

        tk.Frame.__init__(self, app, height=600, width=400)
        
        self.canvas = tk.Canvas(self, width=400, height=300, bg='white')
        self.canvas.grid(row=0, column=0, columnspan=3)
        
        self.btn_previous = tk.Button(self, text="上一個", command=self.previous_word)
        self.btn_previous.grid(row=2, column=0, pady=10)
        
        self.btn_next = tk.Button(self, text="下一個", command=self.next_word)
        self.btn_next.grid(row=2, column=2, pady=10)
        
        self.btn_toggle_translation = tk.Button(self, text="英翻中", command=self.toggle_translation)
        self.btn_toggle_translation.grid(row=1, column=0, pady=10)

        self.btn_show_translation = tk.Button(self, text="顯示翻譯", command=self.show_translation)
        self.btn_show_translation.grid(row=2, column=1, pady=10)

        self.btn_text_to_speech = tk.Button(self, text="voice", command=self.voice)
        self.btn_text_to_speech.grid(row=1, column=2, pady=10)

        self.return_main_frame = tk.Button(
            self, text='回到主視窗', command=self.toggle_parrent_page
        )
        self.return_main_frame.grid(row=1, column=1)
        
        self.dictionary = word_dic  # 你的英文單字和翻譯字典
        self.current_word_index = 0
        self.show_translation_bit = False  # False == 英翻中 是當前翻譯模式
        self.current_lang_state = False  # False == 英文，只是當前顯示的是英文還是中文
        self.translation_to_english = True
        
        word = self.get_current_word()
        self.display_current_word(word)

    def toggle_parrent_page(self):
        self.app.switch_frame(mainFrame.StartPage)

    def display_current_word(self, word):
        self.canvas.delete("word")  # 清除Canvas上的所有單字卡
        if word == '':
            self.current_lang_state = not self.current_lang_state
            word = self.get_current_word()  # self.show_translation_bit == True -> 中文
            key_word = word
            word, _ = translate_text(word)
            self.current_lang_state = not self.current_lang_state
            self.dictionary[key_word] = word
        self.canvas.create_text(200, 150, text=word, font=("Helvetica", 20, 'bold'), tags="word")

    # def on_closing(self):
    #     self.app.destroy()

    def voice(self):
        self.btn_text_to_speech['state'] = tk.DISABLED
        word = self.get_current_word()
        lang = dectect_lang(word)

        flag = threading.Event()  # 創建一個 Event 來控制子執行緒的狀態
        thread = threading.Thread(target=text_to_speech, args=(word, lang, flag))
        thread.daemon = True
        thread.start()

        self.wait_voice_thread = threading.Thread(target=self.reset_voice_btn, args=(flag,))
        self.wait_voice_thread.daemon = True
        self.wait_voice_thread.start()

    def reset_voice_btn(self, flag, ):
        while True:
            time.sleep(0.1)
            if flag.is_set():
                break
        self.btn_text_to_speech['state'] = tk.NORMAL

    def show_translation(self):
        self.current_lang_state = not self.current_lang_state
        word = self.get_current_word()  # self.show_translation_bit == True -> 中文

        self.display_current_word(word)
        
    def toggle_translation(self):
        self.show_translation()
        self.show_translation_bit = not self.show_translation_bit  # False 英翻中
        self.current_lang_state = self.show_translation_bit
        if self.show_translation_bit:
            self.btn_toggle_translation.config(text="中翻英")
        else:
            self.btn_toggle_translation.config(text="英翻中")

    def get_current_word(self):
        word = list(self.dictionary.keys())[self.current_word_index]
        if self.current_lang_state:
            word = self.dictionary[word]
        return word

    def previous_word(self):
        self.current_word_index -= 1
        if self.current_word_index < 0:
            self.current_word_index = len(self.dictionary) - 1
        self.current_lang_state = self.show_translation_bit
        word = self.get_current_word()
        self.display_current_word(word)
    
    def next_word(self):
        self.current_word_index += 1
        if self.current_word_index >= len(self.dictionary):
            self.current_word_index = 0
        self.current_lang_state = self.show_translation_bit
        word = self.get_current_word()
        self.display_current_word(word)

if __name__ == "__main__":
    import textToDic
    # 指定要讀取的txt文件路徑
    file_path = 'words.txt'

    # 讀取txt文件並將單詞和翻譯存儲到字典中
    word_dictionary = textToDic.read_txt_file(file_path)

    app = tk.Tk()
    app = Page(app, word_dictionary)
    app.pack()
    app.mainloop()
