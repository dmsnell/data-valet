import pathlib
import tkinter as tk
from tkinter import ttk

from valet.lib import human, strings
from valet.lib.project import Project

class FileInfoPanel(tk.Frame):
    project: Project
    sort_column = None
    sort_direction = None

    def __init__(self, master, project):
        super().__init__(master)

        self.project = project

        self.file_meta = self.project.get_source_files()
        self.create_table()
        self.pack(fill="both", expand=True)

    def create_table(self):
        style = ttk.Style()
        style.theme_use("clam")  # Use the "clam" theme for a more native look
        style.configure("Treeview", background="#F0F0F0", foreground="#000000", rowheight=25, fieldbackground="#F0F0F0")
        style.configure("Treeview.Heading", background="#CCCCCC", foreground="#000000")
        style.map("Treeview", background=[("selected", "#CCCCCC")])

        self.table = ttk.Treeview(self)
        self.table['columns'] = ('filename', 'file_size', 'file_type', 'file_length', 'transcribed', 'transcription_excerpt')

        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.column("filename", anchor=tk.W, stretch=tk.YES)
        self.table.column("file_size", anchor=tk.W, width=100, stretch=tk.YES)
        self.table.column("file_type", anchor=tk.W, width=60, stretch=tk.NO)
        self.table.column("file_length", anchor=tk.W, width=120, stretch=tk.YES)
        self.table.column("transcribed", anchor=tk.W, width=40, stretch=tk.NO)
        self.table.column("transcription_excerpt", anchor=tk.W, stretch=tk.YES)

        self.table.heading("#0", text='', anchor=tk.W)
        self.table.heading("filename", text='Filename', anchor=tk.W, command=lambda: self.sort_table("filename"))
        self.table.heading("file_size", text='File Size', anchor=tk.W, command=lambda: self.sort_table("file_size"))
        self.table.heading("file_type", text='File Type', anchor=tk.W, command=lambda: self.sort_table("file_type"))
        self.table.heading("file_length", text='File Length', anchor=tk.W, command=lambda: self.sort_table("file_length"))
        self.table.heading("transcribed", text='Transcribed', anchor=tk.W, command=lambda: self.sort_table("transcribed"))
        self.table.heading("transcription_excerpt", text='Transcription Excerpt', anchor=tk.W, command=lambda: self.sort_table("transcription_excerpt"))

        self.table_frame = tk.Frame(self)
        self.table_frame.pack(fill="both", expand=True)

        self.yscrollbar = ttk.Scrollbar(self.master)
        self.yscrollbar.pack(side="right", fill="y")

        self.xscrollbar = ttk.Scrollbar(self.master, orient="horizontal")
        self.xscrollbar.pack(side="bottom", fill="x")

        self.table.pack(side="left", fill="both", expand=True)

        self.table_frame.rowconfigure(0, weight=1)
        self.table_frame.columnconfigure(0, weight=1)

        self.table.configure(yscrollcommand=self.yscrollbar.set)
        self.yscrollbar.configure(command=self.table.yview)
        self.table.configure(xscrollcommand=self.xscrollbar.set)
        self.xscrollbar.configure(command=self.table.xview)

        for filename, audio_meta in self.file_meta.items():
            transcript = self.project.transcription_for(filename)

            self.table.insert('', 'end', values=(
                filename.name, 
                human.file_size(filename.stat().st_size), 
                audio_meta.codecName,
                human.duration(audio_meta.duration),
                '✅' if transcript else '🚫',
                strings.truncate_words(30, transcript) if transcript else ''
            ))

    def sort_table(self, column):
        if self.sort_column == column:
            self.sort_column = column
            self.sort_direction = 'asc'

        self.table.delete(*self.table.get_children())

        sorted_items = sorted(self.file_meta.items(), key=lambda x: x[1].__dict__[column] if column in x[1].__dict__ else x[0].name, reverse=self.sort_direction == 'desc')

        for filename, audio_meta in sorted_items:
            transcript = self.project.transcription_for(filename)

            self.table.insert('', 'end', values=(
                filename.name, 
                human.file_size(filename.stat().st_size), 
                audio_meta.codecName,
                human.duration(audio_meta.duration),
                '✅' if transcript else '🚫',
                strings.truncate_words(30, transcript) if transcript else ''
            ))

        if self.sort_direction == 'asc':
            self.table.heading(column, text=column.capitalize() + ' ↑', anchor=tk.W, command=lambda: self.sort_table(column))
        else:
            self.table.heading(column, text=column.capitalize() + ' ↓', anchor=tk.W, command=lambda: self.sort_table(column))
