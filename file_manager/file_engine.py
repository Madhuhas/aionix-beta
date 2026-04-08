import os
import shutil
import glob
import datetime

class FileEngine:

    def list_files(self, path="."):
        try:
            return os.listdir(path)
        except Exception as e:
            return [f"Error: {str(e)}"]

    def find_by_extension(self, ext, path="."):
        pattern = os.path.join(path, f"*.{ext}")
        return glob.glob(pattern)

    def copy_files(self, src_pattern, dest_folder):
        try:
            os.makedirs(dest_folder, exist_ok=True)
            for file in glob.glob(src_pattern):
                shutil.copy(file, dest_folder)
            return ["Copy complete."]
        except Exception as e:
            return [f"Error: {str(e)}"]

    def delete_files(self, pattern):
        deleted = []
        try:
            for file in glob.glob(pattern):
                os.remove(file)
                deleted.append(file)
            return deleted or ["No files matched."]
        except Exception as e:
            return [f"Error: {str(e)}"]

    def rename_extension(self, old_ext, new_ext, path="."):
        renamed = []
        try:
            for file in glob.glob(os.path.join(path, f"*.{old_ext}")):
                new_name = file.replace(f".{old_ext}", f".{new_ext}")
                os.rename(file, new_name)
                renamed.append(new_name)
            return renamed or ["No files renamed."]
        except Exception as e:
            return [f"Error: {str(e)}"]
