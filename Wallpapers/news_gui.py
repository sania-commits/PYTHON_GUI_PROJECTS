import requests
from tkinter import *

class NewsApp:
    def __init__(self):
        # fetch data:
        self.data = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=e96e9f61b062448694b6c267e8aeb07f').json()

        # initial GUI load:
        self.load_gui()

        # load the 1st news item:
        self.load_news_item(0)

    def load_gui(self):
        self.root = Tk()
        self.root.title("News App")
        self.root.geometry("350x600")
        self.root.resizable(width=False, height=False)
        self.root.configure(background="black")

    def clear_gui(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def load_news_item(self, index):
        # clear the screen for the news item:
        self.clear_gui()
        heading = Label(self.root, text=self.data['articles'][index]["title"],
                bg="black",fg="white",wraplength=350,justify="center")
        heading.pack(pady=(10,20))
        heading.config(font=('verdana',15))

        details = Label(self.root, text=self.data['articles'][index]["description"],
                        bg="black", fg="white", wraplength=350, justify="center")
        heading.pack(pady=(10, 20))
        heading.config(font=('verdana', 15))

        self.root.mainloop()


obj = NewsApp()