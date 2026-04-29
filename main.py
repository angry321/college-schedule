from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.filechooser import FileChooserListView
import platform
import os

from schedule.lessons_for_today import get_today_schedule
from schedule.lessons_for_week import get_week_schedule, format_week_schedule
from schedule.calls import get_calls_schedule

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "path_to_table.txt")

def hex_to_rgba(h, a=1.0):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    return r, g, b, a

BG       = "#0f1117"
SURFACE  = "#1a1d27"
SURFACE2 = "#22263a"
ACCENT   = "#5c6ef8"
ACCENT_H = "#7b8ffb"
TEXT     = "#e8eaf6"
TEXT_DIM = "#6b7280"
BORDER   = "#2d3148"
SUCCESS  = "#4ade80"

Window.clearcolor = hex_to_rgba(BG)


class BgWidget(Widget):
    """Виджет с заливкой фона."""
    def __init__(self, bg_color=SURFACE, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = hex_to_rgba(bg_color)
        with self.canvas.before:
            Color(*self.bg_color)
            self._rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update, size=self._update)

    def _update(self, *_):
        self._rect.pos  = self.pos
        self._rect.size = self.size


class BgBoxLayout(BoxLayout):
    """BoxLayout с заливкой фона."""
    def __init__(self, bg_color=SURFACE, radius=0, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = hex_to_rgba(bg_color)
        self._radius  = radius
        with self.canvas.before:
            Color(*self.bg_color)
            if radius:
                self._rect = RoundedRectangle(pos=self.pos, size=self.size,
                                               radius=[radius])
            else:
                self._rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update, size=self._update)

    def _update(self, *_):
        self._rect.pos  = self.pos
        self._rect.size = self.size


class AccentButton(Button):
    """Кнопка в стиле акцента."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal   = ""
        self.background_down     = ""
        self.background_color    = hex_to_rgba(ACCENT)
        self.color               = (1, 1, 1, 1)
        self.font_size           = dp(14)
        self.bold                = True
        self.size_hint_y         = None
        self.height              = dp(52)
        self.halign              = "left"
        self.padding             = [dp(20), dp(0), dp(20), dp(0)]
        self.bind(on_press=self._press, on_release=self._release)

    def _press(self, *_):
        self.background_color = hex_to_rgba(ACCENT_H)

    def _release(self, *_):
        self.background_color = hex_to_rgba(ACCENT)



def show_content_popup(title, content):
    layout = BgBoxLayout(bg_color=SURFACE, orientation="vertical", padding=dp(8), spacing=dp(6))

    # Заголовок popup
    header = BgBoxLayout(bg_color=SURFACE2, size_hint_y=None, height=dp(48),
                         padding=[dp(14), 0], spacing=dp(8))
    header.add_widget(Label(text=title, color=hex_to_rgba(TEXT), font_size=dp(15),
                            bold=True, halign="left", valign="middle"))
    layout.add_widget(header)

    # Разделитель
    sep = BgWidget(bg_color=BORDER, size_hint_y=None, height=dp(1))
    layout.add_widget(sep)

    # Текст со скроллом
    scroll = ScrollView(size_hint=(1, 1))
    lbl = Label(
        text=content,
        color=hex_to_rgba(TEXT),
        font_size=dp(13),
        halign="left",
        valign="top",
        size_hint_y=None,
        padding=[dp(12), dp(10)],
    )
    lbl.bind(texture_size=lambda inst, val: setattr(inst, "height", val[1]))
    lbl.bind(width=lambda inst, val: setattr(inst, "text_size", (val - dp(24), None)))
    scroll.add_widget(lbl)
    layout.add_widget(scroll)

    popup = Popup(
        title="",
        title_size=0,
        separator_height=0,
        content=layout,
        size_hint=(0.92, 0.85),
        background="",
        background_color=hex_to_rgba(SURFACE),
    )
    # Кнопка закрытия
    close_btn = AccentButton(text="Закрыть", size_hint_y=None, height=dp(44))
    close_btn.bind(on_press=popup.dismiss)
    layout.add_widget(close_btn)

    popup.open()


# Выбор файла

def show_file_chooser(on_select_callback):
    layout = BgBoxLayout(bg_color=SURFACE, orientation="vertical", padding=dp(8), spacing=dp(6))
    
    def get_default_path():
    	# Android
    	if os.path.exists("/storage/emulated/0/Download"):
    		return "/storage/emulated/0/Download"
    	# Windows
    	if os.name == "nt":
    		return os.path.join(os.environ["USERPROFILE"], "Downloads")
    	# Linux
    	return os.path.expanduser("~")

    chooser = FileChooserListView(
    path=get_default_path(),
    filters=["*.xls", "*.xlsx"],
    size_hint=(1, 1),
	)
    chooser.color = hex_to_rgba(TEXT)
    layout.add_widget(chooser)

    btn_row = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))

    cancel_btn = AccentButton(text="Отмена")
    cancel_btn.background_color = hex_to_rgba(SURFACE2)

    select_btn = AccentButton(text="Выбрать")

    btn_row.add_widget(cancel_btn)
    btn_row.add_widget(select_btn)
    layout.add_widget(btn_row)

    popup = Popup(
        title="",
        title_size=0,
        separator_height=0,
        content=layout,
        size_hint=(0.95, 0.9),
        background="",
        background_color=hex_to_rgba(SURFACE),
    )

    def _select(*_):
        if chooser.selection:
            on_select_callback(chooser.selection[0])
            popup.dismiss()

    select_btn.bind(on_press=_select)
    cancel_btn.bind(on_press=popup.dismiss)
    popup.open()


# Главный экран

class MainScreen(BgBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(bg_color=BG, orientation="vertical",
                         padding=[dp(0), dp(0)], spacing=0, **kwargs)
        self._build_ui()

    def _build_ui(self):
        # Заголовок
        title_bar = BgBoxLayout(
            bg_color=SURFACE2, size_hint_y=None, height=dp(56),
            padding=[dp(16), 0], spacing=0,
        )
        title_bar.add_widget(Label(
            text="Расписание",
            color=hex_to_rgba(TEXT),
            font_size=dp(17),
            bold=True,
            halign="left", valign="middle",
        ))
        self.add_widget(title_bar)

        # Разделитель
        self.add_widget(BgWidget(bg_color=BORDER, size_hint_y=None, height=dp(1)))

        # Контент со скроллом
        scroll = ScrollView(size_hint=(1, 1))
        content = BgBoxLayout(
            bg_color=BG, orientation="vertical",
            padding=[dp(16), dp(16)], spacing=dp(6),
            size_hint_y=None,
        )
        content.bind(minimum_height=content.setter("height"))

        # Секция: Просмотр
        content.add_widget(self._section_label("Просмотр расписания"))
        content.add_widget(self._btn("Расписание на сегодня", self.show_today))
        content.add_widget(self._btn("Расписание на неделю",  self.show_week))
        content.add_widget(self._btn("Расписание звонков",    self.show_calls))

        # Разделитель
        content.add_widget(BgWidget(bg_color=BORDER, size_hint_y=None, height=dp(1)))
        content.add_widget(Widget(size_hint_y=None, height=dp(4)))

        # Секция: Файл
        content.add_widget(self._section_label("Файл расписания"))
        content.add_widget(self._btn("Выбрать файл (.xls / .xlsx)", self.choose_file))

        # Метка текущего файла
        self.file_label = Label(
            text="",
            color=hex_to_rgba(TEXT_DIM),
            font_size=dp(12),
            halign="left", valign="top",
            size_hint_y=None, height=dp(32),
            padding=[dp(4), 0],
        )
        self.file_label.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        content.add_widget(self.file_label)

        scroll.add_widget(content)
        self.add_widget(scroll)

        # Загрузить сохранённый путь
        self._load_saved_path()


    def _section_label(self, text):
        lbl = Label(
            text=text,
            color=hex_to_rgba(TEXT_DIM),
            font_size=dp(12),
            halign="left", valign="middle",
            size_hint_y=None, height=dp(28),
            padding=[dp(4), 0],
        )
        lbl.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        return lbl

    def _btn(self, label, callback):
        btn = AccentButton(text=f"  {label}")
        btn.bind(on_release=lambda *_: callback())
        return btn

    # Обработчики

    def show_calls(self):
        show_content_popup("Расписание звонков", get_calls_schedule())

    def show_today(self):
        show_content_popup("Расписание на сегодня", get_today_schedule())

    def show_week(self):
        schedule = get_week_schedule()
        if schedule is None:
            show_content_popup("Расписание на неделю", "Файл не найден или не указан")
        else:
            show_content_popup("Расписание на неделю", format_week_schedule(schedule))

    def choose_file(self):
        def on_select(path):
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                f.write(path)
            short = os.path.basename(path)
            self.file_label.text  = short
            self.file_label.color = hex_to_rgba(SUCCESS)

        show_file_chooser(on_select)

    def _load_saved_path(self):
        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                saved = f.read().strip()
            if saved:
                self.file_label.text  = os.path.basename(saved)
                self.file_label.color = hex_to_rgba(SUCCESS)
        except FileNotFoundError:
            pass


# Приложение

class ScheduleApp(App):
    def build(self):
        self.title = "Расписание"
        Window.size  = (1060, 2250) # Размер окна
        return MainScreen()


if __name__ == "__main__":
    ScheduleApp().run()
