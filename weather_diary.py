import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import json
from datetime import datetime

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.records = []
        self.load_data()
        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Дата:").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(self.root, date_pattern='dd.MM.yyyy')
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Температура:").grid(row=1, column=0, padx=5, pady=5)
        self.temp_entry = tk.Entry(self.root)
        self.temp_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Описание:").grid(row=2, column=0, padx=5, pady=5)
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Осадки:").grid(row=3, column=0, padx=5, pady=5)
        self.precip_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Да", variable=self.precip_var).grid(row=3, column=1, sticky='w')

        # Кнопки
        tk.Button(self.root, text="Добавить запись", command=self.add_record).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Фильтр по дате", command=self.filter_by_date).grid(row=5, column=0, pady=5)
        tk.Button(self.root, text="Фильтр по температуре", command=self.filter_by_temp).grid(row=5, column=1, pady=5)
        tk.Button(self.root, text="Сохранить в JSON", command=self.save_data).grid(row=6, column=0, pady=5)
        tk.Button(self.root, text="Загрузить из JSON", command=self.load_data_dialog).grid(row=6, column=1, pady=5)

        # Таблица записей
        self.tree = ttk.Treeview(self.root, columns=("date", "temp", "desc", "precip"), show='headings')
        self.tree.heading("date", text="Дата")
        self.tree.heading("temp", text="Температура")
        self.tree.heading("desc", text="Описание")
        self.tree.heading("precip", text="Осадки")
        self.tree.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    def add_record(self):
        date = self.date_entry.get_date().strftime('%d.%m.%Y')
        temp = self.temp_entry.get()
        desc = self.desc_entry.get()
        precip = "Да" if self.precip_var.get() else "Нет"

        if not desc:
            messagebox.showerror("Ошибка", "Описание не может быть пустым!")
            return

        try:
            temp = float(temp)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return

        record = {"date": date, "temperature": temp, "description": desc, "precipitation": precip}
        self.records.append(record)
        self.update_table()
        self.clear_entries()

    def clear_entries(self):
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for rec in self.records:
            self.tree.insert("", tk.END, values=(rec["date"], rec["temperature"], rec["description"], rec["precipitation"]))

    def filter_by_date(self):
        date = self.date_entry.get_date().strftime('%d.%m.%Y')
        filtered = [r for r in self.records if r["date"] == date]
        self.records_view(filtered)

    def filter_by_temp(self):
        try:
            threshold = float(tk.simpledialog.askstring("Фильтр", "Введите порог температуры:"))
            filtered = [r for r in self.records if r["temperature"] > threshold]
            self.records_view(filtered)
        except (ValueError, TypeError):
            messagebox.showerror("Ошибка", "Порог должен быть числом!")

    def records_view(self, records):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for rec in records:
            self.tree.insert("", tk.END, values=(rec["date"], rec["temperature"], rec["description"], rec["precipitation"]))

    def save_data(self):
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Сохранено", "Данные успешно сохранены в data.json")

    def load_data_dialog(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "r", encoding="utf-8") as f:
                self.records = json.load(f)
            self.update_table()

    def load_data(self):
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                self.records = json.load(f)
        except FileNotFoundError:
            self.records = []

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()
