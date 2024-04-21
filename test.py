import tkinter as tk

class MyApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', self.on_configure)

        # Create an interior frame to contain all the buttons
        self.interior = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.interior, anchor=tk.NW)
        
        self.display()

    def display(self):
        tk.Label(self.interior, text="Start page", font=("Helvetica", 18, "bold")).grid(row=0, column=1)
        n = 20  # for testing
        
        for i in range(n):
            tk.Button(
                self.interior, text=f"第{i+1}天", font=("Helvetica", 16, "bold"), width=7
            ).grid(row=i//3+1, column=i%3, sticky="ew", padx=13)

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

root = tk.Tk()
app = MyApp(root)
root.mainloop()
