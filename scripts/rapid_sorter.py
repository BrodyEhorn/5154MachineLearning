import os
import shutil
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class ImageSorter:
    def __init__(self, master):
        self.master = master
        self.master.title("Carabiner Rapid Sorter")
        self.master.geometry("900x750")
        
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.raw_dir = os.path.join(self.base_dir, "data", "raw")
        self.open_dir = os.path.join(self.raw_dir, "open")
        self.closed_dir = os.path.join(self.raw_dir, "closed")
        self.trash_dir = os.path.join(self.raw_dir, "trash")
        os.makedirs(self.trash_dir, exist_ok=True)
        
        # Gather all images from ONLY the open dir (since closed is already verified)
        self.image_paths = []
        for d in [self.open_dir]:
            for f in os.listdir(d):
                p = os.path.join(d, f)
                if os.path.isfile(p) and f.lower().endswith(('jpg', 'jpeg', 'png')):
                    self.image_paths.append(p)
                    
        self.current_idx = 0
        self.total = len(self.image_paths)
        
        if self.total == 0:
            messagebox.showinfo("Done", "No images found to sort!")
            self.master.destroy()
            return
            
        # UI Elements
        self.lbl_info = tk.Label(master, text="", font=("Arial", 16, "bold"))
        self.lbl_info.pack(pady=10)
        
        self.lbl_img = tk.Label(master)
        self.lbl_img.pack(expand=True)
        
        instructions = (
            "Keyboard Shortcuts:\n"
            "[O] = Classify as OPEN (loop is disconnected)\n"
            "[C] = Classify as CLOSED (two ends touching)\n"
            "[D] or [Backspace] = Delete (irrelevant image)\n"
            "[Space] = Skip (leave in current folder)"
        )
        self.lbl_instructions = tk.Label(master, text=instructions, font=("Arial", 12), fg="blue")
        self.lbl_instructions.pack(pady=10)
        
        # Key binds
        self.master.bind('o', lambda e: self.move_image(self.open_dir))
        self.master.bind('O', lambda e: self.move_image(self.open_dir))
        self.master.bind('c', lambda e: self.move_image(self.closed_dir))
        self.master.bind('C', lambda e: self.move_image(self.closed_dir))
        self.master.bind('d', lambda e: self.move_image(self.trash_dir))
        self.master.bind('D', lambda e: self.move_image(self.trash_dir))
        self.master.bind('<BackSpace>', lambda e: self.move_image(self.trash_dir))
        self.master.bind('<Delete>', lambda e: self.move_image(self.trash_dir))
        self.master.bind('<space>', lambda e: self.next_image())

        self.load_image()

    def load_image(self):
        if self.current_idx >= self.total:
            messagebox.showinfo("Done", "All images have been sorted! You can close this window.")
            self.master.destroy()
            return
            
        cur_path = self.image_paths[self.current_idx]
        current_folder = os.path.basename(os.path.dirname(cur_path))
        
        self.lbl_info.config(
            text=f"Image {self.current_idx + 1} / {self.total}\nCurrently in: [{current_folder.upper()}]"
        )
        
        try:
            img = Image.open(cur_path)
            # Maintain aspect ratio
            img.thumbnail((800, 550), Image.Resampling.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(img)
            self.lbl_img.config(image=self.tk_img)
        except Exception as e:
            print(f"Error loading {cur_path}: {e}")
            self.move_image(self.trash_dir) # automatically trash corrupt images

    def move_image(self, target_dir):
        src = self.image_paths[self.current_idx]
        filename = os.path.basename(src)
        dst = os.path.join(target_dir, filename)
        
        if os.path.abspath(src) != os.path.abspath(dst):
            try:
                if os.path.exists(dst):
                    base, ext = os.path.splitext(filename)
                    dst = os.path.join(target_dir, f"{base}_sorted{ext}")
                shutil.move(src, dst)
            except Exception as e:
                print(f"Failed to move: {e}")
                
        self.next_image()
        
    def next_image(self):
        self.current_idx += 1
        self.load_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSorter(root)
    
    # Force focus so keys work immediately
    root.focus_force()
    root.mainloop()
