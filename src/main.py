import tkinter as tk
import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS sessions (input TEXT)''')
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
        self.create_button(button_frame, "Delete", self.delete_input)
        self.create_button(button_frame, "Scroll Up", self.scroll_up_sessions)
        self.create_button(button_frame, "Scroll Down", self.scroll_down_sessions)

        scrollbar = tk.Scrollbar(self, command=self.input_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_text.config(yscrollcommand=scrollbar.set)

    def create_button(self, frame, text, command):
        button = tk.Button(frame, text=text, command=command)
        button.pack(fill=tk.X)

    def save_input(self):
        input_data = self.input_text.get("1.0", tk.END).strip()
        if input_data:
            self.db.execute("INSERT INTO sessions (input) VALUES (?)", (input_data,))
            self.input_text.delete("1.0", tk.END)

    def delete_input(self):
        selected_input = self.input_text.get(tk.ACTIVE)
        if selected_input:
            self.db.execute("DELETE FROM sessions WHERE input=?", (selected_input,))
            self.input_text.delete(tk.ACTIVE)

    def scroll_up_sessions(self):
        self.input_text.delete("1.0", tk.END)
        rows = self.db.fetchall("SELECT input FROM sessions")
        for row in rows:
            self.input_text.insert(tk.END, row[0] + '\n')
    def scroll_down_sessions(self):
        self.input_text.delete("1.0", tk.END)
        rows = self.db.fetchall("SELECT input FROM sessions")
        for row in rows:
            self.input_text.insert(tk.END, row[0] + '\n')
    def __del__(self):
        self.db.close()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
