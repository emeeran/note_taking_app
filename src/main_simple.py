import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import tkinter.simpledialog as simpledialog
import sqlite3

class TextEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Text Editor")
        self.master.geometry("800x600")

        self.create_widgets()
        self.load_titles()
        self.selected_title = None
        self.is_list_shown = False

    def create_widgets(self):
        # Text editor
        self.text_box = scrolledtext.ScrolledText(self.master, wrap=tk.WORD)
        self.text_box.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Button frame
        self.button_frame = tk.Frame(self.master)
        self.button_frame.grid(row=1, column=0, sticky="w")

        # Title list frame (hidden by default)
        self.title_frame = tk.Frame(self.master)
        self.title_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Title listbox (scrollable)
        self.title_scrollbar = tk.Scrollbar(self.title_frame, orient=tk.VERTICAL)
        self.title_listbox = tk.Listbox(self.title_frame, width=30, yscrollcommand=self.title_scrollbar.set)
        self.title_scrollbar.config(command=self.title_listbox.yview)
        self.title_listbox.grid(row=0, column=0, sticky="nsew")
        self.title_scrollbar.grid(row=0, column=1, sticky="ns")

        # Button configurations
        button_configs = [
            ("New", self.new_text),
            ("Update", self.update_text),
            ("Save", self.save_text),
            ("Delete", self.delete_text),
            ("List", self.toggle_list),
            ("Close", self.master.destroy)
        ]

        # Create buttons
        for text, command in button_configs:
            button = tk.Button(self.button_frame, text=text, command=command, width=10, height=2)
            button.pack(side="left", padx=5, pady=5)

    def load_titles(self):
        conn = sqlite3.connect('text_editor.db')
        c = conn.cursor()
        c.execute("SELECT title FROM texts")
        titles = c.fetchall()
        conn.close()
        for title in titles:
            self.selected_title = title[0]
            self.title_listbox.insert(tk.END, title[0])

    def new_text(self):
        self.text_box.delete(1.0, tk.END)

    def update_text(self):
        pass

    def save_text(self):
        title = simpledialog.askstring("Title", "Enter title:")
        content = self.text_box.get(1.0, tk.END)
        conn = sqlite3.connect('text_editor.db')
        c = conn.cursor()
        c.execute("INSERT INTO texts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        self.title_listbox.insert(tk.END, title)

    def delete_text(self):
        selected_title = self.title_listbox.get(tk.ACTIVE)
        conn = sqlite3.connect('text_editor.db')
        c = conn.cursor()
        c.execute("DELETE FROM texts WHERE title=?", (selected_title,))
        conn.commit()
        conn.close()
        self.title_listbox.delete(tk.ACTIVE)

    def toggle_list(self):
        if self.is_list_shown:
            self.title_frame.grid_forget()
            self.is_list_shown = False
        else:
            self.title_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
            self.is_list_shown = True

def create_database():
    conn = sqlite3.connect('text_editor.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS texts (title TEXT, content TEXT)''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    root = tk.Tk()
    app = TextEditorApp(root)
    root.mainloop()
