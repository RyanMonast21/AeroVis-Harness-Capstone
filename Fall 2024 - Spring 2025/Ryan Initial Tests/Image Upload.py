#This code snippet would be attached to an upload feature inside the GUI of the HoloLens application.  

import cv2
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

def imageUpload ():
    file_path = filedialog.askopenfilename(
        title = "Please select a valid schematic file.",
        filetypes = [("Image Files","*.jpg;*.jpeg;*.png;*.bmp")]
    )
    return file_path

selectedImage = imageUpload()

if selectedImage:
#Need to replace this line in order to save the image to the memory of the application to eventually be called later.
  print(f"Selected Image:  {selectedImage}")
else:
    print("Valid image not found.")
