import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

import modules.taskmanager as tm

class CSVEditorWindow:
    def __init__(self, root, db_file: Path | str):
        self.window = tk.Toplevel(root)
        self.window.title("Tasks List")
        self.window.resizable(False, False)

        self.file_path = db_file
        self.columns = []
        self.data = []

        # Create the Treeview for displaying tasks
        self.tree = ttk.Treeview(self.window, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10)

        # Create buttons for CRUD operations
        frm_buttons = tk.Frame(self.window)
        frm_buttons.pack(fill=tk.X, padx=5, pady=5)

        # TODO: For next release manage task data (edit and delete task)
        """
        edit_button = tk.Button(frm_buttons, text="Edit", command=self.edit_row)
        edit_button.pack(side=tk.LEFT)

        delete_button = tk.Button(frm_buttons, text="Delete", command=self.delete_row)
        delete_button.pack(side=tk.LEFT)
        """

        delete_button = tk.Button(frm_buttons, text="Retour", command=self.window.destroy)
        delete_button.pack(side=tk.RIGHT)

        self.load_datafile()

    def load_datafile(self):
        self.data.clear()
        self.columns.clear()

        try:
            self.columns, self.data = tm.load_data(self.file_path)
            self.display_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks file: {e}")

    def display_data(self):
        """ Display CSV data in Treeview """
        self.tree.delete(*self.tree.get_children())  # Clear existing data

        # Set up columns in Treeview
        self.tree["columns"] = self.columns
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Insert rows into Treeview
        for row in self.data:
            self.tree.insert("", tk.END, values=[row[col] for col in self.columns])

    def edit_row(self):
        pass

    def delete_row(self):
        pass