import tkinter as tk
from tkinter import ttk
import sqlite3

# Главное окно. В нем располагается панель инструментов и сама база сотрудников.
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#979797', bd=1)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка добавления
        self.add_img = tk.PhotoImage(file='./img/add.png')
        self.btn_add_dialog = tk.Button(
            toolbar, bg='#979797', bd=0, image=self.add_img, command=self.open_dialog
        )
        self.btn_add_dialog.pack(side=tk.LEFT)

        # Кнопка редактирования записи
        self.edit_img = tk.PhotoImage(file='./img/edit.png')
        self.btn_edit_dialog = tk.Button(
            toolbar, bg='#979797', bd=0, image=self.edit_img, command=self.open_edit_dialog
        )
        self.btn_edit_dialog.pack(side=tk.LEFT)
        
        # Кнопка поиска сотрудника
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#979797', bd=0, image=self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # Кнопка удаления сотрудника
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#979797', bd=0, image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)
        
        

        # Отображение таблицы
        self.tree = ttk.Treeview(
            self, columns=("id","name", "number", "email", "salary"), height=45, show="headings"
        )

        self.tree.column("id", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("number", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=150, anchor=tk.CENTER)

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("number", text="Телефон")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("salary", text="Зарплата")

        self.tree.pack(side=tk.LEFT)

    # Обновление записей после действий(добавление, редактирование, удаление)
    def view_records(self):
        self.db.cursor.execute("SELECT * FROM db")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]


    # Функция, вызывающая функцию добавления записей в таблицу db
    def records(self, name, number, email, salary):
        self.db.insert_data(name, number, email, salary)
        self.view_records()

    # Открытие окон добавления, редактирования и поиска сотрудников
    def open_dialog(self):
        Child()

    def open_edit_dialog(self):
        Edit()
    
    def open_search_dialog(self):
        Search()
    
    # Функция редактирования записей
    def edit_records(self, name, number, email, salary):
        self.db.cursor.execute(
            '''UPDATE db SET name=?, number=?, email=?, salary=? WHERE id=?''', 
            (name, number, email, salary, self.tree.set(self.tree.selection()[0], "#1")) 
            # Редактирование первой выделенной записи, "#1" - Браться будет id записи
        )
        self.db.conn.commit()
        self.view_records()


    # Функция поиска записи
    def search_records(self, name):
        name = "%" + name + "%"
        self.db.cursor.execute("SELECT * FROM db WHERE name LIKE ?", (name,))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]

    def delete_records(self):
        for selection_items in self.tree.selection():
            self.db.cursor.execute(
                "DELETE FROM db WHERE id=?", (self.tree.set(selection_items, "#1"))
            )
        self.db.conn.commit()
        self.view_records()

# Дочернее окно.Открывается при добавлениии, редактировании и поиске сотрудника.
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.db = db
        self.view = app


    # Инициализация дочернего окна.Тут же и добавление нового сотрудника.
    def init_child(self): 
        self.title("Добавление сотрудника")
        self.geometry("450x300")
        self.resizable(False, False)


        self.grab_set()  # Захват пользовательского ввода
        self.focus_set() # Пользовательский ввод будет сфокусирован на данном окне.

        # Форма ввода нового контакта
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=100, y=20)
        label_number = tk.Label(self, text='Номер телефона')
        label_number.place(x=100, y=50)
        label_email = tk.Label(self, text='E-mail')
        label_email.place(x=100, y=80)
        label_salary = tk.Label(self, text='Зарплата')
        label_salary.place(x=100, y=110)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=250, y=20)
        self.entry_number = ttk.Entry(self)
        self.entry_number.place(x=250, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=250, y=80)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=250, y=110)


        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=100, y=180)


        self.btn_add = tk.Button(self, text='Добавить')
        self.btn_add.place(x=290, y=180)

        # Отслеживание нажатия на кнопку
        self.btn_add.bind(
            "<Button-1>",
            lambda event:self.view.records(
                self.entry_name.get(), self.entry_number.get(), self.entry_email.get(), self.entry_salary.get()
            ),
        )

class Edit(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title("Редактирование")
        btn_update = ttk.Button(self, text="Редактировать")
        btn_update.place(x=290, y=180)
        btn_update.bind(
            "<Button-1>",
            lambda event: self.view.edit_records(
                self.entry_name.get(), self.entry_number.get(), self.entry_email.get(), self.entry_salary.get()
            ),
        )
        btn_update.bind("<Button-1>", lambda event: self.destroy(), add="+")
        self.btn_add.destroy()
        
    # Отображение данных которые присутствовали до редактирования
    def default_data(self):
        self.db.cursor.execute('SELECT * FROM db WHERE id=?', 
        self.view.tree.set(self.view.tree.selection()[0], "#1")
        )

        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_number.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])
        
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.view = app
        self.init_search()
        

    def init_search(self):
        self.title("Поиск сотрудника")
        self.geometry("300x100")
        self.resizable(False, False)

        label_search = tk.Label(self, text="ФИО")
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=150, y=50)

        search_btn = ttk.Button(self, text="Найти")
        search_btn.place(x=50, y=50)
        search_btn.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        search_btn.bind("<Button-1>", lambda event: self.destroy(), add="+")

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect("db.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS db(
                id INTEGER PRIMARY KEY,
                name TEXT, 
                number TEXT,
                email TEXT,
                salary INTEGER
            )'''
        )
        self.conn.commit()

    def insert_data(self,name, number, email, salary):
        self.cursor.execute(
            '''INSERT INTO db(name, number, email, salary) VALUES (?, ?, ?, ?)''', (name, number, email, salary)
        )
        self.conn.commit()



if __name__ == "__main__":
    root = tk.Tk()
    db = DataBase()
    app = Main(root)
    app.pack()
    root.title("Список сотрудников компании")
    root.geometry("850x450")
    root.resizable(True, True)
    root.mainloop()