# Импорт основного модуля для работы с графическим интерфейсом
# Импорт элементов для создания таблиц, рамок и всплывающих окон
# Модуль для сохранения данных программы в файл в формате JSON
# Модуль для работы с датами и проверки формата
# Модуль для проверки существования файла перед его загрузкой

import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os


class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")  # Заголовок окна программы
        self.root.geometry("680x600")  # Размеры окна
        self.root.configure(bg="#1a1a1a")  # Тёмная тема

        # Настройка стилей для виджетов
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TLabel", background="#1a1a1a", foreground="#ffffff", font=("Arial", 10))
        self.style.configure("TLabelframe", background="#252525", foreground="#00e676", font=("Arial", 10, "bold"))
        self.style.configure("TLabelframe.Label", background="#252525", foreground="#00e676")

        self.trainings = []  # Список для хранения тренировок в памяти
        self.load_trainings()  # Загрузка базы данных при запуске

        self.setup_ui()  # Инициализация графического интерфейса

    def setup_ui(self):
        # --- ФОРМА ВВОДА ---
        input_frame = ttk.LabelFrame(self.root, text=" Добавление тренировки ", padding=10)
        input_frame.pack(pady=10, padx=10, fill="x")

        # Настройка сетки для полей ввода
        ttk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_date = ttk.Entry(input_frame, width=45)
        self.entry_date.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(input_frame, text="Тип тренировки:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_type = ttk.Entry(input_frame, width=45)
        self.entry_type.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(input_frame, text="Длительность (мин):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_duration = ttk.Entry(input_frame, width=45)
        self.entry_duration.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Кнопка добавления
        self.btn_add = tk.Button(input_frame, text="Добавить тренировку", command=self.add_training,
                                 bg="#00e676", fg="#000000", font=("Arial", 9, "bold"), relief="flat")
        self.btn_add.grid(row=3, column=0, columnspan=2, pady=10)

        # --- ФИЛЬТРАЦИЯ ---
        filter_frame = ttk.LabelFrame(self.root, text=" Фильтрация ", padding=10)
        filter_frame.pack(pady=5, padx=10, fill="x")

        ttk.Label(filter_frame, text="Тип тренировки:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_type = ttk.Entry(filter_frame, width=20)
        self.filter_type.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=2, padx=5, pady=5)
        self.filter_date = ttk.Entry(filter_frame, width=20)
        self.filter_date.grid(row=0, column=3, padx=5, pady=5)

        btn_filter = tk.Button(filter_frame, text="Применить", command=self.apply_filter,
                               bg="#333333", fg="#ffffff", font=("Arial", 9), relief="flat")
        btn_filter.grid(row=0, column=4, padx=10, pady=5)

        btn_reset = tk.Button(filter_frame, text="Сбросить", command=self.reset_filter,
                              bg="#333333", fg="#ffffff", font=("Arial", 9), relief="flat")
        btn_reset.grid(row=0, column=5, padx=5, pady=5)

        # --- ТАБЛИЦА ТРЕНИРОВОК ---
        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ("date", "type", "duration")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        # Определение заголовков
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность (мин)")

        # Размеры колонок
        self.tree.column("date", width=150)
        self.tree.column("type", width=250)
        self.tree.column("duration", width=150)

        self.tree.pack(fill="both", expand=True)
        self.update_table_display(self.trainings)

    def add_training(self):
        # Валидация полей
        date_str = self.entry_date.get().strip()
        training_type = self.entry_type.get().strip()
        duration_str = self.entry_duration.get().strip()

        if not date_str or not training_type or not duration_str:
            messagebox.showwarning("Ошибка ввода", "Все поля должны быть заполнены!")
            return

        # Проверка правильности формата даты (ДД.ММ.ГГГГ)
        try:
            valid_date = datetime.strptime(date_str, "%d.%m.%Y")
            formatted_date = valid_date.strftime("%d.%m.%Y")
        except ValueError:
            messagebox.showwarning("Ошибка ввода", "Дата должна быть в формате ДД.ММ.ГГГГ (например, 01.01.2026)!")
            return

        # Проверка, что длительность — это положительное число
        try:
            duration = float(duration_str)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Ошибка ввода", "Длительность должна быть положительным числом!")
            return

        # Добавление тренировки в список
        new_training = {"date": formatted_date, "type": training_type, "duration": duration}
        self.trainings.append(new_training)

        # Сохранение и очистка полей
        self.save_trainings()
        self.update_table_display(self.trainings)

        self.entry_date.delete(0, tk.END)
        self.entry_type.delete(0, tk.END)
        self.entry_duration.delete(0, tk.END)

    def update_table_display(self, items):
        # Обновление содержимого таблицы
        self.tree.delete(*self.tree.get_children())
        for t in items:
            self.tree.insert("", tk.END, values=(t["date"], t["type"], t["duration"]))

    def apply_filter(self):
        # Фильтрация данных
        type_query = self.filter_type.get().strip().lower()
        date_query = self.filter_date.get().strip()

        filtered = []
        for t in self.trainings:
            match_type = type_query in t["type"].lower() if type_query else True
            match_date = t["date"] == date_query if date_query else True

            if match_type and match_date:
                filtered.append(t)

        self.update_table_display(filtered)

    def reset_filter(self):
        # Сброс фильтра
        self.filter_type.delete(0, tk.END)
        self.filter_date.delete(0, tk.END)
        self.update_table_display(self.trainings)

    def save_trainings(self):
        # Сохранение базы в JSON-файл
        with open("trainings.json", "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def load_trainings(self):
        # Загрузка базы из JSON-файла
        if os.path.exists("trainings.json"):
            try:
                with open("trainings.json", "r", encoding="utf-8") as f:
                    self.trainings = json.load(f)
            except json.JSONDecodeError:
                self.trainings = []


if __name__ == "__main__":
    app_window = tk.Tk()
    app = TrainingPlannerApp(app_window)
    app_window.mainloop()