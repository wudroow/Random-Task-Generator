import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"
TASKS_FILE = "tasks_data.json"

INITIAL_TASKS = {
    "Учёба": ["Прочитать статью по Python", "Решить 5 задач по математике", "Посмотреть лекцию"],
    "Спорт": ["Сделать зарядку", "Пробежать 2 км", "Сделать 20 приседаний"],
    "Работа": ["Написать отчёт", "Ответить на письма", "Спланировать задачи на день"]
}

tasks = {}
history = []

root = tk.Tk()
new_task_entry = None
task_type_var = None
filter_var = None
filter_combo = None
result_label = None
result_type_label = None
history_listbox = None

def load_tasks():
    global tasks
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                tasks = json.load(f)
        except:
            tasks = {k: v.copy() for k, v in INITIAL_TASKS.items()}
    else:
        tasks = {k: v.copy() for k, v in INITIAL_TASKS.items()}
        save_tasks()

def save_tasks():
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def load_history():
    global history
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except:
            history = []
    else:
        history = []

def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_task_to_list():
    global tasks
    task_text = new_task_entry.get().strip()
    task_type = task_type_var.get()
    
    if task_text == "":
        messagebox.showwarning("Ошибка ввода", "Задача не может быть пустой!")
        return False
    
    if task_type not in tasks:
        tasks[task_type] = []
    tasks[task_type].append(task_text)
    
    save_tasks()
    update_filter_combo()
    new_task_entry.delete(0, tk.END)
    messagebox.showinfo("Успех", f"Задача \"{task_text}\" добавлена в категорию \"{task_type}\"")
    return True

def generate_random_task():
    global history
    selected_filter = filter_var.get()
    
    if selected_filter == "Все типы":
        available_types = [t for t in tasks.keys() if tasks[t]]
    else:
        if selected_filter not in tasks or not tasks[selected_filter]:
            messagebox.showwarning("Нет задач", f"В категории \"{selected_filter}\" нет задач. Добавьте новую!")
            return
        available_types = [selected_filter]
    
    all_available_tasks = []
    for task_type in available_types:
        for task in tasks[task_type]:
            all_available_tasks.append((task_type, task))
    
    if not all_available_tasks:
        messagebox.showwarning("Нет задач", "Нет доступных задач для генерации. Добавьте задачи!")
        return
    
    chosen_type, chosen_task = random.choice(all_available_tasks)
    
    result_label.config(text=f"{chosen_task}")
    result_type_label.config(text=f"Тип: {chosen_type}")
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append({
        "datetime": now,
        "type": chosen_type,
        "task": chosen_task
    })
    save_history()
    refresh_history_display()

def refresh_history_display():
    for item in history_listbox.get_children():
        history_listbox.delete(item)
    
    for entry in reversed(history):
        history_listbox.insert("", tk.END, values=(
            entry["datetime"],
            entry["type"],
            entry["task"]
        ))

def update_filter_combo():
    current_filter = filter_var.get()
    types = ["Все типы"] + list(tasks.keys())
    filter_combo['values'] = types
    if current_filter not in types:
        filter_var.set("Все типы")

def clear_history():
    global history
    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
        history = []
        save_history()
        refresh_history_display()
        messagebox.showinfo("Готово", "История очищена")

def create_widgets():
    global new_task_entry, task_type_var, filter_var, filter_combo, result_label, result_type_label, history_listbox
    
    add_frame = ttk.LabelFrame(root, text="Добавить новую задачу", padding=10)
    add_frame.pack(fill="x", padx=10, pady=5)
    
    ttk.Label(add_frame, text="Название задачи:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    new_task_entry = ttk.Entry(add_frame, width=40, font=("Arial", 10))
    new_task_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(add_frame, text="Тип:").grid(row=0, column=2, padx=5, pady=5)
    task_type_var = tk.StringVar(value="Учёба")
    type_combo = ttk.Combobox(add_frame, textvariable=task_type_var, values=["Учёба", "Спорт", "Работа"], width=12)
    type_combo.grid(row=0, column=3, padx=5, pady=5)
    
    add_btn = ttk.Button(add_frame, text="Добавить задачу", command=add_task_to_list)
    add_btn.grid(row=0, column=4, padx=10, pady=5)
    
    gen_frame = ttk.LabelFrame(root, text="Генерация задачи", padding=10)
    gen_frame.pack(fill="x", padx=10, pady=5)
    
    ttk.Label(gen_frame, text="Фильтр по типу:").grid(row=0, column=0, padx=5, pady=5)
    filter_var = tk.StringVar(value="Все типы")
    filter_combo = ttk.Combobox(gen_frame, textvariable=filter_var, values=["Все типы", "Учёба", "Спорт", "Работа"], width=15)
    filter_combo.grid(row=0, column=1, padx=5, pady=5)
    
    generate_btn = ttk.Button(gen_frame, text="Сгенерировать задачу", command=generate_random_task)
    generate_btn.grid(row=0, column=2, padx=20, pady=5)
    
    result_label = ttk.Label(gen_frame, text="Нажмите кнопку, чтобы получить задачу", font=("Arial", 12), foreground="green")
    result_label.grid(row=1, column=0, columnspan=3, pady=10)
    
    result_type_label = ttk.Label(gen_frame, text="", font=("Arial", 10), foreground="gray")
    result_type_label.grid(row=2, column=0, columnspan=3)
    
    history_frame = ttk.LabelFrame(root, text="История сгенерированных задач", padding=10)
    history_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    columns = ("datetime", "type", "task")
    history_listbox = ttk.Treeview(history_frame, columns=columns, show="headings", height=12)
    history_listbox.heading("datetime", text="Дата и время")
    history_listbox.heading("type", text="Тип")
    history_listbox.heading("task", text="Задача")
    history_listbox.column("datetime", width=140)
    history_listbox.column("type", width=80)
    history_listbox.column("task", width=400)
    
    scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=history_listbox.yview)
    history_listbox.configure(yscrollcommand=scrollbar.set)
    
    history_listbox.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.pack(side=tk.RIGHT, fill="y")
    
    clear_btn = ttk.Button(history_frame, text="Очистить историю", command=clear_history)
    clear_btn.pack(side=tk.BOTTOM, pady=5)

def main():
    global root
    root.title("Random Task Generator")
    root.geometry("750x550")
    root.resizable(True, True)
    
    load_tasks()
    load_history()
    create_widgets()
    refresh_history_display()
    update_filter_combo()
    
    root.mainloop()

if __name__ == "__main__":
    main()
