from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, RoundedRectangle
import requests
from bs4 import BeautifulSoup


class Card(BoxLayout):
    def __init__(self, title, index, color, callback, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, height=100, padding=10, spacing=5, **kwargs)
        with self.canvas.before:
            Color(*color)
            self.rect = RoundedRectangle(radius=[15], pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.btn = Button(
            text=f"{index}. {title}",
            size_hint=(1, 1),
            halign='left',
            valign='middle',
            text_size=(Window.width - 80, None),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1) if color[0] < 0.5 else (0, 0, 0, 1)
        )
        self.btn.bind(on_release=callback)
        self.add_widget(self.btn)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class NewsApp(App):
    def build(self):
        self.url = "https://www.hurriyet.com.tr/gundem/"
        self.css_selector = ".category__list a"
        self.dark_mode = False
        self.news = []

        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.header = BoxLayout(size_hint_y=None, height=60, padding=10, spacing=10)

        self.menu_button = Button(text='≡', size_hint_x=None, width=50)
        self.menu_button.bind(on_release=self.open_menu)
        self.header.add_widget(self.menu_button)

        self.title_label = Label(text='📰 Haber Uygulaması', font_size=20, bold=True)
        self.header.add_widget(self.title_label)

        self.root.add_widget(self.header)

        self.scroll = ScrollView()
        self.container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15)
        self.container.bind(minimum_height=self.container.setter('height'))
        self.scroll.add_widget(self.container)

        self.root.add_widget(self.scroll)

        self.load_news(self.url, self.css_selector)
        return self.root

    def apply_theme(self):
        if self.dark_mode:
            Window.clearcolor = (0.1, 0.1, 0.1, 1)
            bg_color = (0.2, 0.2, 0.2, 1)
        else:
            Window.clearcolor = (1, 1, 1, 1)
            bg_color = (0.9, 0.9, 0.9, 1)

        self.container.clear_widgets()
        for idx, item in enumerate(self.news, 1):
            card = Card(item["title"], idx, bg_color, lambda btn, i=idx - 1: self.show_details(i))
            self.container.add_widget(card)

    def load_news(self, url, selector):
        self.news = self.get_news(url, selector)
        self.apply_theme()

    def get_news(self, url, selector):
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            articles = soup.select(selector)
            news = []
            for article in articles:
                title = article.get_text(strip=True)
                href = article.get("href")
                if title and href:
                    if not href.startswith("http"):
                        href = "https://www.hurriyet.com.tr" + href
                    news.append({"title": title, "url": href})
            return news
        except Exception as e:
            return [{"title": f"Hata: {e}", "url": ""}]

    def show_details(self, index):
        item = self.news[index]
        detail_text = self.fetch_article_detail(item["url"])

        detail_label = Label(
            text=detail_text,
            size_hint_y=None,
            halign='left',
            valign='top',
            text_size=(Window.width * 0.8, None),
            color=(1, 1, 1, 1) if self.dark_mode else (0, 0, 0, 1),
        )
        detail_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(detail_label)

        popup = Popup(
            title=item["title"],
            content=scroll,
            size_hint=(0.9, 0.9),
            auto_dismiss=True,
        )
        popup.open()

    def fetch_article_detail(self, url):
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")
            content_div = soup.select_one(".news-content")
            if content_div:
                paragraphs = content_div.find_all("p")
                return "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))[:2000]
            return "Detay bulunamadı."
        except Exception as e:
            return f"Detay alınamadı: {e}"

    def open_menu(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        url_input = TextInput(text=self.url, hint_text="Haber Sayfası URL'si", multiline=False, size_hint_y=None, height=40)
        css_input = TextInput(text=self.css_selector, hint_text="CSS Seçici", multiline=False, size_hint_y=None, height=40)

        theme_switch = Switch(active=self.dark_mode, size_hint_y=None, height=30)
        theme_label = Label(text="Karanlık Mod", size_hint_y=None, height=30)

        load_button = Button(text="Yükle", size_hint_y=None, height=40)

        def on_load_press(btn):
            self.url = url_input.text.strip()
            self.css_selector = css_input.text.strip() or ".category__list a"
            self.dark_mode = theme_switch.active
            self.load_news(self.url, self.css_selector)
            popup.dismiss()

        load_button.bind(on_release=on_load_press)

        layout.add_widget(Label(text="Haber Sayfası:", size_hint_y=None, height=30))
        layout.add_widget(url_input)
        layout.add_widget(Label(text="CSS Seçici:", size_hint_y=None, height=30))
        layout.add_widget(css_input)
        layout.add_widget(theme_label)
        layout.add_widget(theme_switch)
        layout.add_widget(load_button)

        popup = Popup(title="Ayarlar", content=layout, size_hint=(0.9, 0.7), auto_dismiss=True)
        popup.open()


if __name__ == '__main__':
    NewsApp().run()
