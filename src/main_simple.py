import sqlite3
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog

class NotesDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS notes
                             (title text, content text)''')
        self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def save_note(self, title, content):
        self.conn.execute("INSERT INTO notes VALUES (?,?)", (title, content))
        self.conn.commit()

    def load_note_content(self, title):
        cursor = self.conn.execute("SELECT content FROM notes WHERE title=?", (title,))
        return cursor.fetchone()[0]

    def update_note_content(self, title, content):
        self.conn.execute("UPDATE notes SET content=? WHERE title=?", (content, title))
        self.conn.commit()

    def delete_note(self, title):
        self.conn.execute("DELETE FROM notes WHERE title=?", (title,))
        self.conn.commit()

    def load_titles(self):
        cursor = self.conn.execute("SELECT title FROM notes")
        return cursor.fetchall()

class NotesApp:
    def __init__(self, root):
        self.db = NotesDB('notes.db')
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(side="left")

        save_button = tk.Button(button_frame, text="Save", command=self.save_note, width=10, height=2)
        save_button.pack(side="top")

        update_button = tk.Button(button_frame, text="Update", command=self.update_note, width=10, height=2)
        update_button.pack(side="top")

        delete_button = tk.Button(button_frame, text="Delete", command=self.delete_note, width=10, height=2)
        delete_button.pack(side="top")

        new_button = tk.Button(button_frame, text="New", command=self.new_note, width=10, height=2)
        new_button.pack(side="top")

        close_button = tk.Button(button_frame, text="Close", command=self.root.quit, width=10, height=2)
        close_button.pack(side="top")

        self.title_listbox = tk.Listbox(self.root)
        self.title_listbox.pack(side="left", fill="both", expand=True)
        self.title_listbox.bind('<<ListboxSelect>>', self.load_note)
        self.title_listbox.grid_remove()

        self.text_area = scrolledtext.ScrolledText(self.root)
        self.text_area.pack(side="right", fill="both", expand=True)

        self.load_titles()

    def save_note(self):
        title = simpledialog.askstring("Input", "Enter session title:")
        if title:
            content = self.text_area.get("1.0", "end-1c")
            self.db.save_note(title, content)
            self.load_titles()
            messagebox.showinfo("Saved", "Your note is saved successfully.")
        else:
            messagebox.showerror("Title Needed", "Please enter a title for your note.")

    def load_note(self, event):
        title = self.title_listbox.get(self.title_listbox.curselection())
        content = self.db.load_note_content(title)
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", content)

    def update_note(self):
        title = self.title_listbox.get(self.title_listbox.curselection())
        content = self.text_area.get("1.0", "end-1c")
        self.db.update_note_content(title, content)
        self.load_titles()
        messagebox.showinfo("Updated", "Your note is updated successfully.")

    def delete_note(self):
        title = self.title_listbox.get(self.title_listbox.curselection())
        if title:
            self.db.delete_note(title)
            self.load_titles()
            messagebox.showinfo("Deleted", "Your note is deleted successfully.")
        else:
            messagebox.showerror("No Selection", "Please select a note to delete.")

    def new_note(self):
        self.text_area.delete("1.0", "end")
        self.title_listbox.grid()

    def load_titles(self):
        titles = self.db.load_titles()
        self.title_listbox.delete(0, "end")
        for title in titles:
            self.title_listbox.insert("end", title[0])

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()
