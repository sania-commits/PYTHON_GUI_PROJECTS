import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

path = Path(__file__).resolve().parents[1] / 'Wallpapers/news_gui.py'
spec = importlib.util.spec_from_file_location('news_gui', path)
news = importlib.util.module_from_spec(spec)
spec.loader.exec_module(news)


class NewsTests(unittest.TestCase):
    def test_demo_images_and_links_without_network(self):
        with patch.object(news, 'Tk'), patch.object(news.NewsApp, 'load_news_item'), patch.object(news.requests, 'get') as get:
            app = news.NewsApp(demo=True)
            get.assert_not_called()
        self.assertEqual(len(app.articles), 2)
        for article in app.articles:
            self.assertTrue((news.IMAGE_DIR / article['demo_image']).is_file())
            self.assertTrue(article['url'].startswith('https://'))

    def test_open_article(self):
        with patch.object(news.webbrowser, 'open', return_value=True) as browser:
            news.NewsApp.__new__(news.NewsApp).open_link('https://example.com/article')
            browser.assert_called_once_with('https://example.com/article')

    def test_missing_link(self):
        with patch.object(news.messagebox, 'showinfo') as message, patch.object(news.webbrowser, 'open') as browser:
            news.NewsApp.__new__(news.NewsApp).open_link(None)
            message.assert_called_once()
            browser.assert_not_called()

    def test_browser_failure(self):
        with patch.object(news.messagebox, 'showinfo') as message, patch.object(news.webbrowser, 'open', return_value=False):
            news.NewsApp.__new__(news.NewsApp).open_link('https://example.com/article')
            message.assert_called_once()


if __name__ == '__main__':
    unittest.main()
