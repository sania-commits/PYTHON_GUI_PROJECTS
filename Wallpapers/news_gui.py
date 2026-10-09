"""Tkinter news reader. Use --demo for a clearly labeled offline preview."""
import argparse
import io
import os
import webbrowser
from pathlib import Path
from tkinter import Tk, Label, Button, Frame
from tkinter import messagebox
from urllib.request import urlopen

import requests
from PIL import ImageTk, Image

IMAGE_DIR = Path(__file__).resolve().parent / 'wallpaper_viewer'
DEMO_URL = 'https://github.com/sania-commits/PYTHON_GUI_PROJECTS#news-reader'


class NewsApp:
    def __init__(self, demo=False):
        self.root = Tk()
        self.root.title('News App — Offline Demo' if demo else 'News App')
        self.root.geometry('350x700')
        self.root.resizable(False, False)
        self.root.configure(background='black')
        self.demo = demo
        if demo:
            self.articles = [
                {'title': 'Offline demo: explore the news reader', 'description': 'Sample content, not a live news headline. The image is a bundled wallpaper. Browse with Next and Prev; Demo Details opens the setup guide.', 'demo_image': 'img1.jpg', 'url': DEMO_URL},
                {'title': 'Offline demo: article navigation', 'description': 'This second sample demonstrates navigation and a different bundled wallpaper. Configure NEWS_API_KEY for actual headlines and article links.', 'demo_image': 'img2.jpg', 'url': DEMO_URL},
            ]
        else:
            key = os.environ.get('NEWS_API_KEY')
            if not key:
                self.show_error('Set NEWS_API_KEY before starting, or run with --demo for an offline preview.')
                self.root.mainloop()
                return
            try:
                response = requests.get('https://newsapi.org/v2/top-headlines', params={'country': 'us', 'apiKey': key}, timeout=15)
                response.raise_for_status()
                data = response.json()
                if data.get('status') != 'ok' or not data.get('articles'):
                    raise ValueError('The API returned no usable articles.')
                self.articles = data['articles']
            except (requests.RequestException, ValueError):
                self.show_error('Headlines could not be loaded. Check your connection, API key and account access. You can also use --demo.')
                self.root.mainloop()
                return
        self.load_news_item(0)
        self.root.mainloop()

    def show_error(self, text):
        Label(self.root, text=text, fg='white', bg='black', wraplength=320, font=('verdana', 12)).pack(padx=15, pady=30)

    def load_news_item(self, index):
        for widget in self.root.pack_slaves():
            widget.destroy()
        article = self.articles[index]
        try:
            with Image.open(IMAGE_DIR / article.get('demo_image', 'img1.jpg')) as local_image:
                image = local_image.convert('RGB').resize((350, 250))
        except OSError:
            image = Image.new('RGB', (350, 250), '#24384a')
        image_url = article.get('urlToImage')
        if image_url and not self.demo:
            try:
                with urlopen(image_url, timeout=10) as response:
                    image = Image.open(io.BytesIO(response.read())).convert('RGB').resize((350, 250))
            except (OSError, ValueError, TypeError):
                pass
        photo = ImageTk.PhotoImage(image)
        label = Label(self.root, image=photo, bg='black')
        label.image = photo
        label.pack()
        if self.demo:
            Label(self.root, text='OFFLINE DEMO · SAMPLE CONTENT', fg='#b8daff', bg='black', font=('verdana', 9)).pack(pady=8)
        Label(self.root, text=article.get('title') or 'No title available', fg='white', bg='black', wraplength=330, justify='center', font=('verdana', 15)).pack(pady=(10, 20))
        Label(self.root, text=article.get('description') or 'No description available', fg='white', bg='black', wraplength=330, justify='center', font=('verdana', 12)).pack(pady=(10, 20))
        frame = Frame(self.root, bg='black')
        frame.pack(side='bottom', pady=15)
        count = len(self.articles)
        Button(frame, text='Prev', width=10, height=3, command=lambda: self.load_news_item((index - 1) % count)).pack(side='left')
        url = article.get('url')
        Button(frame, text='Demo Details' if self.demo else 'Read More', width=10, height=3, command=lambda: self.open_link(url)).pack(side='left')
        Button(frame, text='Next', width=10, height=3, command=lambda: self.load_news_item((index + 1) % count)).pack(side='left')

    def open_link(self, url):
        if url and url.startswith(('https://', 'http://')):
            try:
                opened = webbrowser.open(url)
                if not opened:
                    messagebox.showinfo('News App', 'No browser could be opened. Article URL: ' + url)
            except webbrowser.Error:
                messagebox.showinfo('News App', 'The browser could not be opened. Article URL: ' + url)
        else:
            messagebox.showinfo('News App', 'No web article is available for this item.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--demo', action='store_true', help='Show offline sample content without an API key')
    NewsApp(demo=parser.parse_args().demo)
