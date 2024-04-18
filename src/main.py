import tkinter as tk
import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''DROP TABLE IF EXISTS sessions''')
        self.c.execute('''CREATE TABLE sessions (title TEXT, content TEXT)''')
        self.conn.commit()


    def execute(self, query, params=()):
        self.c.execute(query, params)
        self.conn.commit()

    def fetchall(self, query, params=()):
        self.c.execute(query, params)
        return self.c.fetchall()

    def close(self):
        self.conn.close()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db = Database('database.db')
        self.create_widgets()

    def create_widgets(self):
        self.input_text = tk.Text(self)
        self.input_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.create_button(button_frame, "Save", self.save_input)
        self.create_button(button_frame, "Scroll", self.scroll_sessions)

        scrollbar = tk.Scrollbar(self, command=self.input_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_text.config(yscrollcommand=scrollbar.set)

    def create_button(self, frame, text, command):
        button = tk.Button(frame, text=text, command=command)
        button.pack(fill=tk.X)

    def save_input(self):
        input_data = self.input_text.get("1.0", tk.END).strip()
        if input_data:
            self.db.execute("INSERT INTO sessions (title, content) VALUES (?, ?)", (input_data, input_data))
            self.input_text.delete("1.0", tk.END)

    def scroll_sessions(self):
        self.input_text.delete("1.0", tk.END)
        rows = self.db.fetchall("SELECT title FROM sessions")
        for row in rows:
            self.input_text.insert(tk.END, row[0] + '\n')
            self.input_text.tag_bind(row[0], "<Button-1>", lambda event, title=row[0]: self.show_content(title))

    def show_content(self, title):
        content = self.db.fetchall("SELECT content FROM sessions WHERE title=?", (title,))
        if content:
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert(tk.END, content[0][0])

    def __del__(self):
        self.db.close()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
