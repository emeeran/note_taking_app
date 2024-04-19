import sqlite3
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Connect to SQLite database
conn = sqlite3.connect('notes.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS notes
             (title text, content text)''')

def save_note(self):
    title = self.title_entry.get()
    content = self.text_area.get("1.0", "end-1c")
    if title:
        c.execute("INSERT INTO notes VALUES (?,?)", (title, content))
        conn.commit()
        self.load_titles()
        messagebox.showinfo("Saved", "Your note is saved successfully.")
    else:
        messagebox.showerror("Title Needed", "Please enter a title for your note.")

def load_note(event):
    title = title_listbox.get(title_listbox.curselection())
    c.execute("SELECT content FROM notes WHERE title=?", (title,))
    content = c.fetchone()[0]
    text_area.delete("1.0", "end")
    text_area.insert("1.0", content)

def delete_note():
    title = title_listbox.get(title_listbox.curselection())
    if title:
        c.execute("DELETE FROM notes WHERE title=?", (title,))
        conn.commit()
        load_titles()
        messagebox.showinfo("Deleted", "Your note is deleted successfully.")
    else:
        messagebox.showerror("No Selection", "Please select a note to delete.")

def load_titles():
    c.execute("SELECT title FROM notes")
    titles = c.fetchall()
    title_listbox.delete(0, "end")
    for title in titles:
        title_listbox.insert("end", title[0])

root = tk.Tk()

title_label = tk.Label(root, text="Title:")
title_label.pack(side="left")
title_entry = tk.Entry(root)
title_entry.pack(side="left")

text_area = scrolledtext.ScrolledText(root)
text_area.pack()

button_frame = tk.Frame(root)
button_frame.pack(side="left")

save_button = tk.Button(button_frame, text="Save", command=save_note)
save_button.pack(side="left")

delete_button = tk.Button(button_frame, text="Delete", command=delete_note)
delete_button.pack(side="left")

exit_button = tk.Button(button_frame, text="Exit", command=root.quit)
exit_button.pack(side="left")

title_listbox = tk.Listbox(root)
title_listbox.pack(side="right")
title_listbox.bind('<<ListboxSelect>>', load_note)

load_titles()

root.mainloop()
