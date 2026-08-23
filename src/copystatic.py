import os
import shutil

def copy_static(old_path, new_path):
    if os.path.exists(new_path):
        shutil.rmtree(new_path)
    os.mkdir(new_path)
    for item in os.listdir(old_path):
        old_item = os.path.join(old_path, item)
        new_item = os.path.join(new_path, item)
        if os.path.isfile(old_item):
            shutil.copy(old_item, new_item)
        else:
            copy_static(old_item, new_item)
