import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
import logging

class DragAndDrop:
    def __init__(self, root):
        self.root = root
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def enable_drag_and_drop(self, widget):
        try:
            # Only bind drag events, not click events
            widget.bind("<B1-Motion>", self.on_drag)
            widget.bind("<ButtonRelease-1>", self.on_drop)
            self.logger.info("Drag and drop enabled for widget (without click handling)")

        except Exception as e:
            self.logger.error(f"Error enabling drag and drop: {e}")



    def on_drag(self, event):
        pass  # Placeholder for future drag functionality

    def on_drop(self, event):
        try:
            file_path = self.root.clipboard_get()
            if os.path.exists(file_path):
                dest_dir = filedialog.askdirectory(title="Select Destination Directory")
                if dest_dir:
                    try:
                        shutil.copy(file_path, dest_dir)
                        self.logger.info(f"File copied to {dest_dir}")
                        self.show_success_message(f"File successfully copied to {dest_dir}")
                    except Exception as e:
                        self.logger.error(f"Error copying file: {e}")
                        self.show_error_message(f"Error copying file: {e}")
        except Exception as e:
            self.logger.error(f"Error during drop operation: {e}")

    def show_success_message(self, message):
        messagebox.showinfo("Success", message)

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    def cleanup(self):
        try:
            self.root.clipboard_clear()
            self.logger.info("Clipboard cleared")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
