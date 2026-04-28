from tkinter import *
from tkinter import filedialog
import os

from schedule.lessons_for_today import get_today_schedule
from schedule.lessons_for_week import get_week_schedule, format_week_schedule
from schedule.calls import get_calls_schedule

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "path_to_table.txt")

# color
BG        = "#0f1117"   # фон приложения
SURFACE   = "#1a1d27"   # фон карточек / окон
SURFACE2  = "#22263a"   # чуть светлее для hover
ACCENT    = "#5c6ef8"   # синий акцент
ACCENT_H  = "#7b8ffb"   # hover акцент
TEXT      = "#e8eaf6"   # основной текст
TEXT_DIM  = "#6b7280"   # второстепенный текст
BORDER    = "#2d3148"   # рамки
SUCCESS   = "#4ade80"   # зелёный (сохранено)
FONT_MAIN = ("Segoe UI", 5)
FONT_H    = ("Segoe UI Semibold", 8)
FONT_BIG  = ("Segoe UI Semibold", 5)
FONT_MONO = ("Consolas", 7)

def _on_enter(btn, color=ACCENT_H):
    btn.config(bg=color)

def _on_leave(btn, color=ACCENT):
    btn.config(bg=color)

def _make_btn(parent, text, icon, cmd):
    """Кнопка с иконкой — эмодзи-префикс + текст."""
    f = Frame(parent, bg=SURFACE, cursor="hand2")
    f.pack(fill=X, pady=5, padx=20)

    inner = Frame(f, bg=ACCENT, bd=0)
    inner.pack(fill=X)

    lbl = Label(
        inner,
        text=f"  {text}",
        bg=ACCENT, fg="white",
        font=FONT_H,
        anchor=W,
        padx=14, pady=12,
    )
    lbl.pack(fill=X)

    for w in (inner, lbl):
        w.bind("<Enter>",  lambda e, b=inner, l=lbl: (b.config(bg=ACCENT_H), l.config(bg=ACCENT_H)))
        w.bind("<Leave>",  lambda e, b=inner, l=lbl: (b.config(bg=ACCENT),   l.config(bg=ACCENT)))
        w.bind("<Button-1>", lambda e: cmd())

    return f

def _drag_start(win, event):
    win._drag_x = event.x
    win._drag_y = event.y

def _drag_move(win, event):
    dx = event.x - win._drag_x
    dy = event.y - win._drag_y
    x  = win.winfo_x() + dx
    y  = win.winfo_y() + dy
    win.geometry(f"+{x}+{y}")

def _make_titlebar(win, title, close_cmd):
    bar = Frame(win, bg=SURFACE2, height=100)
    bar.pack(fill=X)
    bar.pack_propagate(False)

    Label(bar, text=title, bg=SURFACE2, fg=TEXT, font=FONT_H).pack(side=LEFT, padx=14)

    close = Label(bar, text="✕", bg=SURFACE2, fg=TEXT_DIM,
                  font=("Segoe UI", 8, "bold"), cursor="hand2", padx=12)
    close.pack(side=RIGHT)
    close.bind("<Button-1>", lambda e: close_cmd())
    close.bind("<Enter>",    lambda e: close.config(fg="#ef4444"))
    close.bind("<Leave>",    lambda e: close.config(fg=TEXT_DIM))

    bar.bind("<ButtonPress-1>",   lambda e: _drag_start(win, e))
    bar.bind("<B1-Motion>",       lambda e: _drag_move(win, e))

def show_window(title, content):
    win = Toplevel(root)
    win.title(title)
    win.geometry("1060x2250")
    win.configure(bg=SURFACE)
    win.overrideredirect(True)

    _make_titlebar(win, title, win.destroy)
  
    Frame(win, bg=BORDER, height=1).pack(fill=X)

    text_frame = Frame(win, bg=SURFACE, padx=6, pady=6)
    text_frame.pack(fill=BOTH, expand=True)

    scrollbar = Scrollbar(text_frame, troughcolor=SURFACE, bg=SURFACE2,
                          activebackground=ACCENT, relief=FLAT, width=8)
    scrollbar.pack(side=RIGHT, fill=Y)

    text = Text(
        text_frame,
        yscrollcommand=scrollbar.set,
        font=FONT_MONO,
        bg=BG, fg=TEXT,
        insertbackground=TEXT,
        selectbackground=ACCENT,
        relief=FLAT,
        padx=12, pady=10,
        spacing1=3, spacing3=3,
        wrap=WORD,
    )
    text.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=text.yview)

    text.insert(END, content)
    text.config(state=DISABLED)

    win.update_idletasks()
    rx = root.winfo_x() + (root.winfo_width()  - win.winfo_width())  // 2
    ry = root.winfo_y() + (root.winfo_height() - win.winfo_height()) // 2
    win.geometry(f"+{rx}+{ry}")

def show_calls():
    show_window("Расписание звонков", get_calls_schedule())

def show_lessons_today():
    show_window("Расписание на сегодня", get_today_schedule())

def show_lessons_week():
    schedule = get_week_schedule()
    if schedule is None:
        show_window("Расписание на неделю", "Файл не найден или не указан")
    else:
        show_window("Расписание на неделю", format_week_schedule(schedule))

def choose_file():
    file_path = filedialog.askopenfilename(
        title="Выбрать файл расписания",
        filetypes=[("Excel файлы", "*.xls *.xlsx")]
    )
    if file_path:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(file_path)
        short = os.path.basename(file_path)
        file_label.config(text=f"{short}", fg=SUCCESS)

root = Tk()
root.title("Расписание")
root.geometry("1060x2250")
root.configure(bg=BG)
root.overrideredirect(True)
root.resizable(False, False)

root.update_idletasks()
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
root.geometry(f"1060x2250+{(sw-380)//2}+{(sh-440)//2}")

_make_titlebar(root, "Расписание", root.destroy)
Frame(root, bg=BORDER, height=1).pack(fill=X)

Label(root, text="Просмотр расписания",
      bg=BG, fg=TEXT_DIM, font=("Segoe UI", 5)).pack(anchor=W, padx=20, pady=(16, 4))

_make_btn(root, "Расписание на сегодня", " ", show_lessons_today)
_make_btn(root, "Расписание на неделю", " ", show_lessons_week)
_make_btn(root, "Расписание звонков", " ", show_calls)

Frame(root, bg=BORDER, height=1).pack(fill=X, padx=20, pady=14)

Label(root, text="Файл расписания",
      bg=BG, fg=TEXT_DIM, font=("Segoe UI", 5)).pack(anchor=W, padx=20, pady=(0, 4))

_make_btn(root, "Выбрать файл (.xls / .xlsx)", " ", choose_file)

file_label = Label(root, text="", bg=BG, fg=TEXT_DIM, font=("Segoe UI", 9))
file_label.pack(anchor=W, padx=34)

try:
    with open(CONFIG_FILE, encoding="utf-8") as f:
        saved = f.read().strip()
    if saved:
        file_label.config(text=f"{os.path.basename(saved)}", fg=SUCCESS)
except FileNotFoundError:
    pass

root.mainloop()
