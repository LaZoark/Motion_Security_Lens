from tkinter import Tk
from tkinter.filedialog import askdirectory
def ask_folder_popup():
    # we don't want a full GUI, so keep the root window from appearing
    Tk().withdraw() 
    # show an "Open" dialog box and return the path to the selected file
    foldername = askdirectory() 
    return foldername

if __name__ == "__main__":
    foldername = ask_folder_popup()
    print("This function will help you find a good place to store video/image.")
    print("Folder you have choose:")
    print(foldername)