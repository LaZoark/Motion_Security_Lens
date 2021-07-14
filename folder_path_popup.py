from tkinter import Tk
from tkinter.filedialog import askdirectory
import os


def ask_folder_popup():
    # we don't want a full GUI, so keep the root window from appearing
    Tk().withdraw()
    # show an "Open" dialog box and return the path to the selected file
    root_dir = askdirectory()
    _video_path = root_dir + f"/video/"
    _capture_path = root_dir + f"/image/"

    if os.path.exists(root_dir):
        _video_path = root_dir + f"/video/"
        _capture_path = root_dir + f"/image/"
    else:
        print("""Can't find "{}". Using default path.""".format(root_dir))
        _video_path = "video//"
        _capture_path = "image//"
    if not os.path.exists(_video_path):
        print("""Can't find "{}". making one for you!""".format(_video_path))
        os.makedirs(_video_path)
    if not os.path.exists(_capture_path):
        print("""Can't find "{}". making one for you!""".format(_capture_path))
        os.makedirs(_capture_path)

    return _video_path, _capture_path


if __name__ == "__main__":
    video_path, capture_path = ask_folder_popup()
    print("This function will help you find a good place to store video/image.")
    print("Folder you have choose:\n", video_path, '\n', capture_path)
