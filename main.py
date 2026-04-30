import tkinter as tk # Подключаем графическую библиотеку
from tkinter import messagebox, ttk # Инструменты для окон и таблиц
import random # Для случайного выбора цитат
import json # Для работы с файлом истории
import os # Для проверки наличия файлов

# import tkinter as tk

class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Quotes v2.0") # Изменен заголовок окна
        self.root.geometry("650x650")
        self.root.configure(bg="#1e1e1e") # Установлен темный фон окна

        # Полностью обновленная база данных цитат
        self.quotes = [
            {"text": "Простота — это высшая форма сложности.", "author": "Леонардо да Винчи", "theme": "Дизайн"},
            {"text": "Ваше время ограничено, не тратьте его, живя чужой жизнью.", "author": "Стив Джобс", "theme": "Успех"},
            {"text": "Ошибки — это знаки препинания жизни, без которых, как и в тексте, нет смысла.", "author": "Харуки Мураками", "theme": "Жизнь"}
        ]

        self.history = []
        self.load_history() # Загружаем старые записи из файла

        self.setup_ui() # Запускаем создание интерфейса

    def setup_ui(self):
        # Надпись для цитаты: изменен шрифт и цвет на ярко-бирюзовый
        self.quote_label = tk.Label(self.root, text="Нажмите кнопку для вдохновения",
                                    wraplength=500, font=("Verdana", 12, "italic"),
                                    fg="#00adb5", bg="#1e1e1e")
        self.quote_label.pack(pady=20)

        # Кнопка: изменен цвет фона и текста
        btn_gen = tk.Button(self.root, text="Сгенерировать цитату", command=self.generate_quote,
                            bg="#393e46", fg="#eeeeee", font=("Arial", 10, "bold"))
        btn_gen.pack(pady=5)

        # Секция добавления: изменена цветовая схема рамки
        add_frame = tk.LabelFrame(self.root, text="Добавить свою цитату", bg="#222831", fg="#00adb5")
        add_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(add_frame, text="Текст:", bg="#222831", fg="white").grid(row=0, column=0)
        self.entry_text = tk.Entry(add_frame, width=50, bg="#393e46", fg="white")
        self.entry_text.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(add_frame, text="Автор:", bg="#222831", fg="white").grid(row=1, column=0)
        self.entry_author = tk.Entry(add_frame, width=50, bg="#393e46", fg="white")
        self.entry_author.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(add_frame, text="Тема:", bg="#222831", fg="white").grid(row=2, column=0)
        self.entry_theme = tk.Entry(add_frame, width=50, bg="#393e46", fg="white")
        self.entry_theme.grid(row=2, column=1, padx=5, pady=2)

        btn_add = tk.Button(add_frame, text="Добавить в базу", command=self.add_custom_quote, bg="#00adb5", fg="white")
        btn_add.grid(row=3, column=0, columnspan=2, pady=5)

        # Секция фильтра
        filter_frame = tk.Frame(self.root, bg="#1e1e1e")
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Поиск в истории:", bg="#1e1e1e", fg="white").pack(side=tk.LEFT)
        self.filter_entry = tk.Entry(filter_frame, bg="#393e46", fg="white")
        self.filter_entry.pack(side=tk.LEFT, padx=5)
        self.filter_entry.bind("<KeyRelease>", lambda event: self.apply_filter()) # Живой поиск при вводе

        # Список истории: изменены цвета на темные
        tk.Label(self.root, text="История сгенерированных цитат:", bg="#1e1e1e", fg="#eeeeee").pack()
        self.history_listbox = tk.Listbox(self.root, width=80, height=8, bg="#222831", fg="#eeeeee", borderwidth=0)
        self.history_listbox.pack(pady=5, padx=10)
        self.update_history_display()

    def add_custom_quote(self):
        # Метод для сохранения новой цитаты от пользователя
        text = self.entry_text.get()
        author = self.entry_author.get()
        theme = self.entry_theme.get()

        if not text.strip() or not author.strip() or not theme.strip():
            messagebox.showwarning("Внимание", "Поля не могут быть пустыми!")
            return

        self.quotes.append({"text": text, "author": author, "theme": theme})
        self.entry_text.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_theme.delete(0, tk.END)
        messagebox.showinfo("Успех", "Цитата успешно добавлена!")

    def generate_quote(self):
        # Метод для выбора случайной цитаты и обновления истории
        if not self.quotes: return
        quote = random.choice(self.quotes)
        self.quote_label.config(text=f'"{quote["text"]}"\n— {quote["author"]} ({quote["theme"]})')

        self.history.append(quote)
        self.save_history()
        self.update_history_display()

    def update_history_display(self, items=None):
        # Метод обновления визуального списка истории
        self.history_listbox.delete(0, tk.END)
        display_items = items if items is not None else self.history
        for q in reversed(display_items):
            self.history_listbox.insert(tk.END, f"[{q['theme']}] {q['author']}: {q['text']}")

    def apply_filter(self):
        # Логика поиска по автору или теме
        query = self.filter_entry.get().lower()
        filtered = [q for q in self.history if query in q['author'].lower() or query in q['theme'].lower()]
        self.update_history_display(filtered)

    def save_history(self):
        # Запись истории в JSON файл
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        # Чтение истории из файла при запуске
        if os.path.exists("history.json"):
            try:
                with open("history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except: self.history = []

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()