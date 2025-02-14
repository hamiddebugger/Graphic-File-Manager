import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import logging
import os
from file_manager import FileManager
from image_preview import ImagePreview
from tags_manager import TagsManager
from search_manager import SearchManager
from drag_and_drop import DragAndDrop
from utils import list_files

class GraphicFileManagerUI:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.root = ttk.Window(themename="cosmo")
        self.root.title("Graphic File Manager")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        self.setup_window_protocols()
        self.file_manager = FileManager()
        self.image_preview = ImagePreview(self.root)
        self.tags_manager = TagsManager()
        self.search_manager = SearchManager()
        self.drag_and_drop = DragAndDrop(self.root)
        # Initialize native drag and drop
        self.current_directory = '.'

        # Setup UI elements
        self.setup_ui()

        # Load initial files
        self.load_files()

    def setup_ui(self):
        # Main content frame
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.file_listbox = tk.Listbox(
            self.main_frame, 
            selectmode=tk.SINGLE,
            bg="#ffffff",
            fg="#333333",
            selectbackground="#0078d7",
            selectforeground="#ffffff",
            font=("Segoe UI", 10)
        )
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.file_listbox.bind("<<ListboxSelect>>", self.on_file_select)
        self.drag_and_drop.enable_drag_and_drop(self.file_listbox)

        self.preview_frame = ttk.Frame(self.main_frame, padding=10, bootstyle="light")
        self.preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.image_preview.set_preview_frame(self.preview_frame)

        self.button_frame = ttk.Frame(self.root, padding=10)
        self.button_frame.pack(fill=tk.X)

        self.select_folder_button = ttk.Button(
            self.button_frame, 
            text="📁 Select Folder", 
            command=self.select_folder,
            bootstyle="primary-outline"
        )
        self.select_folder_button.pack(side=tk.LEFT)

        self.search_entry = ttk.Entry(
            self.button_frame,
            width=30,
            bootstyle="secondary"
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind("<KeyRelease>", self.on_search)

        self.search_button = ttk.Button(
            self.button_frame, 
            text="🔍 Search", 
            command=self.perform_search,
            bootstyle="success-outline"
        )
        self.search_button.pack(side=tk.LEFT)

    def setup_window_protocols(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            if os.path.isdir(folder_selected):
                self.current_directory = folder_selected
                self.load_files()
            else:
                messagebox.showerror("Error", "Invalid directory selected")
                self.logger.error(f"Invalid directory selected: {folder_selected}")

    def load_files(self):
        try:
            self.file_listbox.delete(0, tk.END)
            self.files = list_files(self.current_directory, extensions=['jpg', 'jpeg', 'png', 'webp'])
            if not self.files:
                messagebox.showinfo("Information", "No supported image files found")
                self.logger.info("No supported image files found")
            for file in self.files:
                self.file_listbox.insert(tk.END, file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load files: {str(e)}")
            self.logger.error(f"Error loading files: {e}")

    def on_file_select(self, event):
        """Handle file selection - only show preview"""
        selected_index = self.file_listbox.curselection()
        if selected_index:
            file_path = self.file_listbox.get(selected_index)
            self.image_preview.load_image(file_path)

    def on_search(self, event):
        query = self.search_entry.get()
        self.perform_search(query)

    def perform_search(self, query=None):
        if query is None:
            query = self.search_entry.get()
        results = self.search_manager.search_by_name(self.files, query)
        self.file_listbox.delete(0, tk.END)
        for file in results:
            self.file_listbox.insert(tk.END, file)

    def on_close(self):
        try:
            self.logger.info("Application closing")
            self.root.quit()
        except Exception as e:
            self.logger.error(f"Error during close: {e}")
        finally:
            self.root.destroy()

    def run(self):
        try:
            self.logger.info("Starting UI main loop")
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"UI main loop error: {e}")
            raise
