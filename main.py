# Импорт основного модуля для работы с графическим интерфейсом
# Импорт элементов для создания таблиц, рамок и всплывающих окон
# Модуль для сохранения данных программы в файл в формате JSON
# Модуль для проверки существования файла перед его загрузкой

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")  # Заголовок окна программы
        self.root.geometry("680x600")  # Размеры окна
        self.root.configure(bg="#1e1e1e")  # Тёмная тема

        # Настройка стилей для виджетов
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TLabel", background="#1e1e1e", foreground="#ffffff", font=("Arial", 10))
        self.style.configure("TLabelframe", background="#252525", foreground="#ffaa00", font=("Arial", 10, "bold"))
        self.style.configure("TLabelframe.Label", background="#252525", foreground="#ffaa00")

        self.movies = []  # Список для хранения фильмов в памяти
        self.load_movies()  # Загрузка базы данных при запуске

        self.setup_ui()  # Инициализация графического интерфейса

    def setup_ui(self):
        # --- ФОРМА ВВОДА ---
        input_frame = ttk.LabelFrame(self.root, text=" Добавление фильма ", padding=10)
        input_frame.pack(pady=10, padx=10, fill="x")

        # Настройка сетки для полей ввода
        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_title = ttk.Entry(input_frame, width=45)
        self.entry_title.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(input_frame, text="Жанр:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_genre = ttk.Entry(input_frame, width=45)
        self.entry_genre.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(input_frame, text="Год выпуска:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_year = ttk.Entry(input_frame, width=45)
        self.entry_year.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(input_frame, text="Рейтинг (0-10):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.entry_rating = ttk.Entry(input_frame, width=45)
        self.entry_rating.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # Кнопка добавления
        self.btn_add = tk.Button(input_frame, text="Добавить фильм", command=self.add_movie,
                                 bg="#ffaa00", fg="#000000", font=("Arial", 9, "bold"), relief="flat")
        self.btn_add.grid(row=4, column=0, columnspan=2, pady=10)

        # --- ФИЛЬТРАЦИЯ ---
        filter_frame = ttk.LabelFrame(self.root, text=" Фильтрация ", padding=10)
        filter_frame.pack(pady=5, padx=10, fill="x")

        ttk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_genre = ttk.Entry(filter_frame, width=20)
        self.filter_genre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Год:").grid(row=0, column=2, padx=5, pady=5)
        self.filter_year = ttk.Entry(filter_frame, width=20)
        self.filter_year.grid(row=0, column=3, padx=5, pady=5)

        btn_filter = tk.Button(filter_frame, text="Применить", command=self.apply_filter,
                               bg="#333333", fg="#ffffff", font=("Arial", 9), relief="flat")
        btn_filter.grid(row=0, column=4, padx=10, pady=5)

        btn_reset = tk.Button(filter_frame, text="Сбросить", command=self.reset_filter,
                              bg="#333333", fg="#ffffff", font=("Arial", 9), relief="flat")
        btn_reset.grid(row=0, column=5, padx=5, pady=5)

        # --- ТАБЛИЦА ФИЛЬМОВ ---
        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        # Определение заголовков
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год выпуска")
        self.tree.heading("rating", text="Рейтинг")

        # Размеры колонок
        self.tree.column("title", width=250)
        self.tree.column("genre", width=120)
        self.tree.column("year", width=100)
        self.tree.column("rating", width=100)

        self.tree.pack(fill="both", expand=True)
        self.update_table_display(self.movies)

    def add_movie(self):
        # Валидация полей
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        year_str = self.entry_year.get().strip()
        rating_str = self.entry_rating.get().strip()

        if not title or not genre or not year_str or not rating_str:
            messagebox.showwarning("Ошибка ввода", "Все поля должны быть заполнены!")
            return

        # Проверка, что год является числом
        try:
            year = int(year_str)
        except ValueError:
            messagebox.showwarning("Ошибка ввода", "Год должен быть целым числом!")
            return

        # Проверка, что рейтинг — это число от 0 до 10
        try:
            rating = float(rating_str)
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showwarning("Ошибка ввода", "Рейтинг должен быть числом от 0 до 10!")
            return

        # Добавление фильма в список
        new_movie = {"title": title, "genre": genre, "year": year, "rating": rating}
        self.movies.append(new_movie)

        # Сохранение и очистка полей
        self.save_movies()
        self.update_table_display(self.movies)

        self.entry_title.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_rating.delete(0, tk.END)

    def update_table_display(self, items):
        # Обновление содержимого таблицы
        self.tree.delete(*self.tree.get_children())
        for m in items:
            self.tree.insert("", tk.END, values=(m["title"], m["genre"], m["year"], m["rating"]))

    def apply_filter(self):
        # Фильтрация данных
        genre_query = self.filter_genre.get().strip().lower()
        year_query = self.filter_year.get().strip()

        filtered = []
        for m in self.movies:
            match_genre = genre_query in m["genre"].lower() if genre_query else True
            match_year = str(m["year"]) == year_query if year_query else True

            if match_genre and match_year:
                filtered.append(m)

        self.update_table_display(filtered)

    def reset_filter(self):
        # Сброс фильтра
        self.filter_genre.delete(0, tk.END)
        self.filter_year.delete(0, tk.END)
        self.update_table_display(self.movies)

    def save_movies(self):
        # Сохранение базы в JSON-файл
        with open("movies.json", "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_movies(self):
        # Загрузка базы из JSON-файла
        if os.path.exists("movies.json"):
            try:
                with open("movies.json", "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
            except json.JSONDecodeError:
                self.movies = []


if __name__ == "__main__":
    app_window = tk.Tk()
    app = MovieLibraryApp(app_window)
    app_window.mainloop()