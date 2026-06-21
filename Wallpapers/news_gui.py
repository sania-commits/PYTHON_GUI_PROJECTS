import requests
import subprocess
from tkinter import *
from urllib.request import urlopen
from PIL import ImageTk,Image
import io

class NewsApp:
    def __init__(self):
        # fetch data:
        self.data = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=e96e9f61b062448694b6c267e8aeb07f').json()

        # initial GUI load:
        self.load_gui()

        # load the 1st news item:
        self.load_news_item(0)
        self.root.mainloop()

    def load_gui(self):
        self.root = Tk()
        self.root.title("News App")
        self.root.geometry("350x700")
        self.root.resizable(width=False, height=False)
        self.root.configure(background="black")

    def clear_gui(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def load_news_item(self, index):
        # clear the screen for the news item
        self.clear_gui()

        #image:
        try:
            img_url = self.data["articles"][index]["urlToImage"]
            raw_data = urlopen(img_url).read()
            im= Image.open(io.BytesIO(raw_data)).resize((350,250))
            photo = ImageTk.PhotoImage(im)

        except:
            img_url = 'https://images.wondershare.com/repairit/article/fixing-the-image-not-available-error-01.png'
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((350, 250))
            photo = ImageTk.PhotoImage(im)

        label = Label(self.root, image=photo)
        label.image = photo
        label.pack()

        title = self.data['articles'][index].get('title') or 'No title available'
        heading = Label(self.root,text=title,fg="white",bg="black",wraplength=350,justify="center")
        heading.pack(pady=(10,20))
        heading.config(font=('verdana', 15))

        description = self.data['articles'][index].get('description') or "No description available"
        details = Label(self.root,text=description,fg="white",bg="black",wraplength=350,justify="center")
        details.pack(pady=(10,20))
        details.config(font=('verdana', 12))

        frame = Frame(self.root,bg="black")
        frame.pack(expand=True, fill="both")

        total_articles = len(self.data['articles'])

        prev = Button(frame, text='Prev', width=10, height=3,command= lambda: self.load_news_item((index-1) % total_articles))
        prev.pack(side="left")

        print(self.data['articles'][index].get('url'))
        read = Button(frame, text='Read More', width=10, height=3, command= lambda: self.open_link(self.data['articles'][index].get('url')))
        read.pack(side="left")

        next = Button(frame, text='Next', width=10, height=3,command= lambda: self.load_news_item((index+1) % total_articles))
        next.pack(side="left")

    def open_link(self, url):
        try:
            print("Opening:", url)
            subprocess.run(["cmd.exe", "/c", "start", url])
        except Exception as e:
            print("Error:", e)

obj = NewsApp()