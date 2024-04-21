import tkinter as tk
import mainFrame

class Page(tk.Frame):
    def __init__(self, app, word_dic):
        self.app = app
        self.app.title("單字卡")

        tk.Frame.__init__(self, app, height=600, width=400)
        
        self.canvas = tk.Canvas(self, width=400, height=300, bg='white')
        self.canvas.pack(pady=20)
        
        self.btn_previous = tk.Button(self, text="上一個", command=self.previous_word)
        self.btn_previous.pack(side=tk.LEFT, padx=10)
        
        self.btn_next = tk.Button(self, text="下一個", command=self.next_word)
        self.btn_next.pack(side=tk.RIGHT, padx=10)
        
        self.btn_toggle_translation = tk.Button(self, text="顯示翻譯", command=self.toggle_translation)
        self.btn_toggle_translation.pack(side=tk.BOTTOM, pady=10)

        tk.Button(
            self, text='回到主視窗', command=self.toggle_parrent_page
        ).pack()
        
        self.dictionary = word_dic  # 你的英文單字和翻譯字典
        self.current_word_index = 0
        self.show_translation = False
        self.translation_to_english = True
        
        self.display_current_word()

    def toggle_parrent_page(self):
        self.app.switch_frame(mainFrame.StartPage)

    def display_current_word(self):
        self.canvas.delete("word")  # 清除Canvas上的所有單字卡
        
        word = list(self.dictionary.keys())[self.current_word_index]        
        if self.show_translation:
            if self.translation_to_english:
                text = self.dictionary[word]
            else:
                text = word
        else:
            text = word
        
        self.canvas.create_text(200, 150, text=text, font=("Helvetica", 20, 'bold'), tags="word")
        
    def toggle_translation(self):
        self.show_translation = not self.show_translation
        if self.show_translation:
            self.btn_toggle_translation.config(text="顯示英文")
        else:
            self.btn_toggle_translation.config(text="顯示翻譯")
        self.display_current_word()
        
    def previous_word(self):
        self.current_word_index -= 1
        if self.current_word_index < 0:
            self.current_word_index = len(self.dictionary) - 1
        self.display_current_word()
    
    def next_word(self):
        self.current_word_index += 1
        if self.current_word_index >= len(self.dictionary):
            self.current_word_index = 0
        self.display_current_word()

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
