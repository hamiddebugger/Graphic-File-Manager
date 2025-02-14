from PIL import Image, ImageTk, UnidentifiedImageError
import tkinter as tk
from tkinter import Menu, filedialog, messagebox
import io
import platform
import win32clipboard
import shutil
import logging
from pathlib import Path

class ImagePreview:
    def __init__(self, root):
        self.root = root
        self.preview_label = None
        self.current_image_path = None
        self.logger = logging.getLogger(__name__)
        self.max_size = (800, 800)  # Maximum preview dimensions
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif']

    def set_preview_frame(self, frame):
        self.preview_label = tk.Label(frame)
        self.preview_label.pack(fill=tk.BOTH, expand=True)
        self.setup_context_menu()

    def setup_context_menu(self):
        self.context_menu = Menu(self.preview_label, tearoff=0)
        self.context_menu.add_command(label="Copy Image", command=self.copy_to_clipboard)
        self.context_menu.add_command(label="Copy Image to Folder", command=self.copy_to_folder)
        self.preview_label.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def copy_to_clipboard(self):
        if self.current_image_path:
            try:
                with Image.open(self.current_image_path) as image:
                    if platform.system() == "Windows":
                        # Windows-specific clipboard handling
                        output = io.BytesIO()
                        image.convert("RGB").save(output, "BMP")
                        data = output.getvalue()[14:]  # Remove BMP header
                        output.close()
                        
                        win32clipboard.OpenClipboard()
                        win32clipboard.EmptyClipboard()
                        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                        win32clipboard.CloseClipboard()
                    else:
                        # Fallback for other platforms
                        output = io.BytesIO()
                        image.save(output, format="PNG")
                        data = output.getvalue()
                        output.close()
                        
                        self.root.clipboard_clear()
                        self.root.clipboard_append(self.current_image_path)
                        self.root.clipboard_append(data, format="image/png")
                    
                    self.logger.info(f"Image copied to clipboard: {self.current_image_path}")
                    messagebox.showinfo("Success", "Image copied to clipboard")
                    
            except Exception as e:
                self.logger.error(f"Error copying image to clipboard: {e}")
                messagebox.showerror("Error", f"Failed to copy image: {e}")

    def copy_to_folder(self):
        if self.current_image_path:
            try:
                dest_folder = filedialog.askdirectory(title="Select Destination Folder")
                if dest_folder:
                    dest_path = shutil.copy(self.current_image_path, dest_folder)
                    self.logger.info(f"Image copied to: {dest_path}")
                    messagebox.showinfo("Success", f"Image copied to:\n{dest_path}")
            except Exception as e:
                self.logger.error(f"Error copying image to folder: {e}")
                messagebox.showerror("Error", f"Failed to copy image: {e}")

    def load_image(self, file_path):
        self.current_image_path = file_path
        try:
            if not Path(file_path).is_file():
                raise FileNotFoundError(f"File not found: {file_path}")
                
            if Path(file_path).suffix.lower() not in self.supported_formats:
                raise ValueError(f"Unsupported file format: {Path(file_path).suffix}")
                
            with Image.open(file_path) as image:
                # Preserve aspect ratio while fitting within max_size
                image.thumbnail(self.max_size, Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.preview_label.config(image=photo)
                self.preview_label.image = photo
                self.logger.info(f"Successfully loaded image: {file_path}")
                
        except FileNotFoundError as e:
            self.logger.error(f"File not found: {file_path}")
            messagebox.showerror("Error", f"File not found: {file_path}")
        except UnidentifiedImageError as e:
            self.logger.error(f"Invalid image file: {file_path}")
            messagebox.showerror("Error", f"Invalid image file: {file_path}")
        except ValueError as e:
            self.logger.error(f"Unsupported format: {file_path}")
            messagebox.showerror("Error", f"Unsupported image format: {Path(file_path).suffix}")
        except Exception as e:
            self.logger.error(f"Error loading image: {e}")
            messagebox.showerror("Error", f"Failed to load image: {e}")
