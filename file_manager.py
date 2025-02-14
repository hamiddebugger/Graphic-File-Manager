import os
import shutil
import logging
from datetime import datetime

class FileManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def rename_file(self, old_path, new_name):
        try:
            if not os.path.exists(old_path):
                raise FileNotFoundError(f"Source file not found: {old_path}")
                
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            
            if os.path.exists(new_path):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                base, ext = os.path.splitext(new_name)
                new_name = f"{base}_{timestamp}{ext}"
                new_path = os.path.join(os.path.dirname(old_path), new_name)
                self.logger.warning(f"File already exists, renamed with timestamp: {new_name}")
                
            os.rename(old_path, new_path)
            self.logger.info(f"File renamed from {old_path} to {new_path}")
            return new_path
        except Exception as e:
            self.logger.error(f"Error renaming file: {e}")
            raise

    def move_file(self, src_path, dest_path):
        try:
            if not os.path.exists(src_path):
                raise FileNotFoundError(f"Source file not found: {src_path}")
                
            if os.path.isdir(dest_path):
                dest_path = os.path.join(dest_path, os.path.basename(src_path))
                
            if os.path.exists(dest_path):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                base, ext = os.path.splitext(os.path.basename(src_path))
                new_name = f"{base}_{timestamp}{ext}"
                dest_path = os.path.join(os.path.dirname(dest_path), new_name)
                self.logger.warning(f"File already exists, renamed with timestamp: {new_name}")
                
            shutil.move(src_path, dest_path)
            self.logger.info(f"File moved from {src_path} to {dest_path}")
            return dest_path
        except Exception as e:
            self.logger.error(f"Error moving file: {e}")
            raise

    def create_backup(self, file_path):
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base, ext = os.path.splitext(file_path)
            backup_path = f"{base}_backup_{timestamp}{ext}"
            
            shutil.copy(file_path, backup_path)
            self.logger.info(f"Backup created at {backup_path}")
            return backup_path
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            raise
