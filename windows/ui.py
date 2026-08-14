import os
import sys
import ctypes
import customtkinter as ctk
from PIL import Image

# --- 1. ШЛЯХИ ТА СИСТЕМНЕ ЗАВАНТАЖЕННЯ ШРИФТУ ДЛЯ WINDOWS ---
def get_resource_path(relative_path):
    """Отримує абсолютний шлях до файлів (підтримує звичайний запуск та PyInstaller .exe)"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

FONT_PATH = get_resource_path(os.path.join("assets", "fonts", "Allerta-Regular.ttf"))
FONT_NAME = "Allerta"

# Завантажуємо шрифт у пам'ять оперативної системи Windows (без прав адміністратора)
if os.path.exists(FONT_PATH):
    FR_PRIVATE = 0x10
    ctypes.windll.gdi32.AddFontResourceExW(FONT_PATH, FR_PRIVATE, 0)
else:
    FONT_NAME = "Arial"  # Резервний шрифт, якщо файл не знайдено

# --- 2. НАЛАШТУВАННЯ ТЕМИ ТА ГЛОБАЛЬНИХ ЗМІННИХ ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Змінні шрифту
FONT_MAIN = (FONT_NAME, 13, "bold")
FONT_LARGE = (FONT_NAME, 18, "bold")

# Колірна палітра
COLOR_BG = "#1e1e2e"
COLOR_BUTTON = "#35354d"
COLOR_TEXT_MAIN = "#cdd6f4"
COLOR_TEXT_MUTED = "#a6adc8"
COLOR_TAB_ACTIVE = "#444462"
COLOR_TAB_INACTIVE = "#35354d"
COLOR_BUG_BTN = "#F38ba8"
COLOR_PLAY_BTN = "#89b4fa"
COLOR_PROGRESS_BG = "#5e5e60"
COLOR_PROGRESS_FG = "#54c46f"

# --- 3. ОСНОВНИЙ КЛАС ПРОГРАМИ ---
class Duina(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Налаштування вікна
        self.title("Duina")
        self.geometry('520x520')
        self.configure(fg_color=COLOR_BG)
        self.resizable(False, False)
        
        # Спроба прибрати іконку з заголовка вікна
        try:
            self.iconbitmap("")
        except Exception:
            pass

        # Початкові дані
        self.current_file = "sketch.ino"
        self.current_port = "COM3 ArduinoUNO"
        self.current_board = "arduino:avr:uno"

        # Завантаження іконок дій
        bug_btn_img = get_resource_path(os.path.join("windows", "assets", "images", "bug.png"))
        run_btn_img = get_resource_path(os.path.join("windows", "assets", "images", "run.png"))


        if os.path.exists(bug_btn_img):
            self.bug_icon = ctk.CTkImage(Image.open(bug_btn_img), size=(30, 30))
        else:
            self.bug_icon = None

        if os.path.exists(run_btn_img):
            self.play_icon = ctk.CTkImage(Image.open(run_btn_img), size=(30, 30))
        else:
            self.play_icon = None

        # Побудова UI (викликається ОДИН раз після ініціалізації даних)
        self._build_ui()

    def _build_ui(self):
        # 1. Верхня секція (Кнопки налаштувань та іконки)
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(20, 10))

        controls = [
            ("Open File", self.current_file),
            ("COM Port", self.current_port),
            ("Board Type", self.current_board)
        ]

        left_container = ctk.CTkFrame(top_frame, fg_color="transparent")
        left_container.pack(side="left", fill="y")

        for btn_text, val_text in controls:
            row = ctk.CTkFrame(left_container, fg_color="transparent")
            row.pack(anchor="w", pady=4)

            btn = ctk.CTkButton(
                row,
                text=btn_text,
                width=100,
                height=32,
                corner_radius=8,
                fg_color=COLOR_BUTTON,
                hover_color="#444462",
                text_color=COLOR_TEXT_MAIN,
                font=FONT_MAIN
            )
            btn.pack(side="left", padx=(0, 12))

            lbl = ctk.CTkLabel(
                row,
                text=val_text,
                text_color=COLOR_TEXT_MAIN,
                font=FONT_MAIN
            )
            lbl.pack(side="left")

        # Права частина (Жук + Плей)
        right_container = ctk.CTkFrame(top_frame, fg_color="transparent")
        right_container.pack(side="right", anchor="n")

        bug_btn = ctk.CTkButton(
            right_container,
            text="",
            image=self.bug_icon,
            width=42,
            height=42,
            corner_radius=10,
            fg_color=COLOR_BUG_BTN,
            hover_color="#e07191",
            border_spacing=0
        )
        bug_btn.pack(side="left", padx=5)

        run_btn = ctk.CTkButton(
            right_container,
            text="" if self.play_icon else "➤",
            image=self.play_icon,
            width=42,
            height=42,
            corner_radius=10,
            fg_color=COLOR_PLAY_BTN,
            hover_color="#739ee8",
        )
        run_btn.pack(side="left", padx=5)

        # 2. Секція вкладок
        tabs_frame = ctk.CTkFrame(self, fg_color="transparent")
        tabs_frame.pack(fill="x", padx=20, pady=(20, 0))

        self.btn_serial = ctk.CTkButton(
            tabs_frame,
            text="Serial Monitor",
            width=120,
            height=28,
            corner_radius=8,
            fg_color=COLOR_TAB_ACTIVE,
            hover_color=COLOR_TAB_ACTIVE,
            text_color=COLOR_TEXT_MAIN,
            font=FONT_MAIN,
            command=self._select_serial
        )
        self.btn_serial.pack(side="left", padx=(0, 5))

        self.btn_terminal = ctk.CTkButton(
            tabs_frame,
            text="Terminal",
            width=100,
            height=28,
            corner_radius=8,
            fg_color=COLOR_TAB_INACTIVE,
            hover_color=COLOR_TAB_ACTIVE,
            text_color=COLOR_TEXT_MUTED,
            font=FONT_MAIN,
            command=self._select_terminal
        )
        self.btn_terminal.pack(side="left")

        # 3. Головна консоль
        self.console_box = ctk.CTkFrame(
            self,
            height=200,
            corner_radius=16,
            fg_color=COLOR_TAB_ACTIVE
        )
        self.console_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # 4. Прогрес-бар
        progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        progress_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            height=22,
            corner_radius=0,
            fg_color=COLOR_PROGRESS_BG,
            progress_color=COLOR_PROGRESS_FG
        )
        self.progress_bar.pack(fill="x")
        self.progress_bar.set(0.37)

        # 5. Панель статусу
        status_frame = ctk.CTkFrame(self, fg_color="transparent")
        status_frame.pack(fill="x", padx=20, pady=(0, 15))

        loading_lbl = ctk.CTkLabel(
            status_frame,
            text="Loading... 37%",
            text_color=COLOR_TEXT_MAIN,
            font=FONT_MAIN
        )
        loading_lbl.pack(side="left")

        compile_lbl = ctk.CTkLabel(
            status_frame,
            text="Compile...",
            text_color=COLOR_TEXT_MAIN,
            font=FONT_MAIN
        )
        compile_lbl.pack(side="right")

    def _select_serial(self):
        self.btn_serial.configure(fg_color=COLOR_TAB_ACTIVE, text_color=COLOR_TEXT_MAIN)
        self.btn_terminal.configure(fg_color=COLOR_TAB_INACTIVE, text_color=COLOR_TEXT_MUTED)

    def _select_terminal(self):
        self.btn_terminal.configure(fg_color=COLOR_TAB_ACTIVE, text_color=COLOR_TEXT_MAIN)
        self.btn_serial.configure(fg_color=COLOR_TAB_INACTIVE, text_color=COLOR_TEXT_MUTED)

if __name__ == "__main__":
    app = Duina()
    app.mainloop()