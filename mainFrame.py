import tkinter as tk
import textToDic
import page

class App(tk.Tk):
    def __init__(self, word_dic):
        tk.Tk.__init__(self)
        self.geometry('450x420+550+100')
        self._frame = None
        self.words_dictionary = word_dic  # constant
        self._word_dic_number = len(word_dic)  # constant
        # self._word_dic_number = 1000  # constant
        self.page_pos = 0
        self.page_size = 10
        self.switch_frame(StartPage)

    def set_page_pos(self, pos = 0):
        self.page_pos = pos
    
    def set_page_size(self, size = 10):
        self.page_size = size

    def switch_frame(self, frame):
        my_data = dict( list(self.words_dictionary.items())[self.page_pos : self.page_pos+self.page_size] )
        new_frame = frame(self, my_data)  # 根據傳入的要建立的page建構Page
        
        # 如果現在APP有frame就刪除，並且將新建立的frame換上
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):  # 是個tk.Frame
    def __init__(self, app, _):
        tk.Frame.__init__(self, app)  # self是__init__一定要傳的，實際上parent是app，沒有其他option
        self.app = app
        
        self.canvas = tk.Canvas(self, height=420, width=400)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)  # 更新scrollBar
        self.canvas.bind('<Configure>', self.on_configure)  # 限制滾輪範圍
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)  # 滾輪事件

        # Create an interior frame to contain all the buttons，不然要每個button都create_window
        self.interior = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.interior, anchor=tk.NW)
        
        self.display()
    
    def display(self):
        tk.Label(self.interior, text="Start page", font=("Helvetica", 18, "bold")).grid(row=0, column=1)
        n = self.app._word_dic_number // 10 + (self.app._word_dic_number % 10 != 0)
        
        for i in range(n):
            btn = tk.Button(self.interior, text=f"第{i+1}天", font=("Helvetica", 16, "bold"), width=7
            , command=lambda i=i*10: self.toggle_to_vocabulary(i))
            btn.grid(row=i//3+1, column=i%3, sticky="ewns", padx=13)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def toggle_to_vocabulary(self, pos):
        self.app.set_page_pos(pos)
        self.app.set_page_size(10)
        self.app.switch_frame(page.Page)

if __name__ == "__main__":
    # 指定要讀取的txt文件路徑
    file_path = 'words.txt'

    # 讀取txt文件並將單詞和翻譯存儲到字典中
    word_dictionary = textToDic.read_txt_file(file_path)

    app = App(word_dictionary)
    app.mainloop()