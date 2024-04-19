import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

def create_database():
    with Database('notes.db') as db:
        db.execute('''CREATE TABLE IF NOT EXISTS notes (title TEXT, content TEXT)''')

class NoteTakingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Note Taking App")
        self.master.geometry("800x600")
        self.create_widgets()
        self.load_titles()

    def create_widgets(self):
        self.button_frame = tk.Frame(self.master, width=200)
        self.button_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")

        self.text_box = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=60, height=60)
        self.text_box.grid(row=0, column=1, rowspan=3, sticky="nsew")

        self.title_frame = tk.Frame(self.master)
        self.title_frame.grid(row=0, column=2, rowspan=3, sticky="nsew")

        self.title_scrollbar = tk.Scrollbar(self.title_frame, orient=tk.VERTICAL)
        self.title_listbox = tk.Listbox(self.title_frame, width=180, yscrollcommand=self.title_scrollbar.set)  # Triple the width
        self.title_listbox.grid(row=0, column=0, sticky="nsew")
        self.title_scrollbar.config(command=self.title_listbox.yview)
        self.title_scrollbar.grid(row=0, column=1, sticky="ns")

        button_configs = [
            ("New", self.new_note),
            ("Update", self.update_note),
            ("Save", self.save_note),
            ("Delete", self.delete_note),
            ("List Hide", self.toggle_list),
            ("Exit", self.master.destroy),

        ]

        for row, (text, command) in enumerate(button_configs):
            button = tk.Button(self.button_frame, text=text, command=command, width=12, height=2)
            button.grid(row=row, column=0, padx=5, pady=5, sticky="nsew")

        self.selected_title = None
        self.is_list_shown = True

        self.title_listbox.bind("<ButtonRelease-1>", self.display_selected_note)  # Bind
    def load_titles(self):
        with Database('notes.db') as db:
            db.execute("SELECT title FROM notes")
            titles = db.fetchall()
        self.title_listbox.delete(0, tk.END)
        for title in titles:
            self.title_listbox.insert(tk.END, title[0])

    def display_selected_note(self, event):
        selected_index = self.title_listbox.curselection()
        if selected_index:
            self.selected_title = self.title_listbox.get(selected_index)
            with Database('notes.db') as db:
                db.execute("SELECT content FROM notes WHERE title=?", (self.selected_title,))
                content = db.fetchone()
            if content:
                self.text_box.delete(1.0, tk.END)
                self.text_box.insert(tk.END, content[0])
            else:
                self.text_box.delete(1.0, tk.END)
                self.text_box.insert(tk.END, "No content available for this title.")

    def update_note(self):
        if self.selected_title:
            content = self.text_box.get(1.0, tk.END)
            conn = sqlite3.connect('notes.db')
            c = conn.cursor()
            c.execute("UPDATE notes SET content=? WHERE title=?", (content, self.selected_title))
            conn.commit()
            conn.close()
            messagebox.showinfo("Update", f"Note '{self.selected_title}' updated successfully")
        else:
            messagebox.showerror("Error", "No title selected. Please select a title.")

    def new_note(self):
        self.text_box.delete(1.0, tk.END)
        self.selected_title = None


    def save_note(self):
        title = simpledialog.askstring("New Note", "Enter a title for the new note")
        if title:
            content = self.text_box.get(1.0, tk.END)
            conn = sqlite3.connect('notes.db')
            c = conn.cursor()
            c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
            conn.commit()
            conn.close()
            self.load_titles()  # Reload titles after saving
            self.selected_title = title  # Set the new title as the selected title
        else:
            messagebox.showwarning("Warning", "Please enter a title for the new note.")


    def delete_note(self):
        selected_index = self.title_listbox.curselection()
        if selected_index:
            title_to_delete = self.title_listbox.get(selected_index)
            confirmation = messagebox.askyesno("Delete", f"Are you sure you want to delete the note '{title_to_delete}'?")
            if confirmation:
                conn = sqlite3.connect('notes.db')
                c = conn.cursor()
                c.execute("DELETE FROM notes WHERE title=?", (title_to_delete,))
                conn.commit()
                conn.close()
                self.load_titles()  # Reload titles after deletion
                self.text_box.delete(1.0, tk.END)  # Clear text box after deletion
        else:
            messagebox.showerror("Error", "Please select a title to delete")# Delete note logic remains unchanged, but uses Database context manager
        # ...

    def toggle_list(self):
        if self.is_list_shown:
            self.title_frame.grid_remove()
            self.is_list_shown = False
        else:
            self.title_frame.grid()
            self.is_list_shown = True# Toggle list logic remains unchanged
        # ...

if __name__ == "__main__":
    create_database()
    root = tk.Tk()
    app = NoteTakingApp(root)
    root.mainloop()
