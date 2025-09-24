import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys


def create_entry_grid(root, rows, columns):
    entry_grid = []
    for i in range(rows):
        row = []
        for j in range(columns):
            entry = tk.Entry(root, width=5)
            entry.grid(row=i+1, column=j, padx=5, pady=5)
            row.append(entry)
        entry_grid.append(row)
    return entry_grid


def resize_image(image_path, max_width, max_height):
    """Resize image while maintaining aspect ratio"""
    try:
        # Open the original image
        original_image = Image.open(image_path)
        
        # Get original dimensions
        orig_width, orig_height = original_image.size
        
        # Calculate scaling factor to fit within max dimensions
        width_ratio = max_width / orig_width
        height_ratio = max_height / orig_height
        scale_factor = min(width_ratio, height_ratio)
        
        # Calculate new dimensions
        new_width = int(orig_width * scale_factor)
        new_height = int(orig_height * scale_factor)
        
        # Resize the image
        resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return ImageTk.PhotoImage(resized_image)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


def update_image_size(root, image_label, image_path):
    """Update image size based on current window size"""
    # Get current window dimensions
    root.update_idletasks()  # Ensure geometry is updated
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    
    # Reserve space for the entry grid and buttons (approximately 300px)
    available_height = max(200, window_height - 300)
    available_width = max(200, window_width - 100)
    
    # Resize and update the image
    new_image = resize_image(image_path, available_width, available_height)
    if new_image:
        image_label.config(image=new_image)
        image_label.image = new_image  # Keep a reference to prevent garbage collection


def check_answers(row_entries, molecule_f, pt):
    # correctFlag = {}
    # for i in molecule:
    #     correctFlag[i] = False

    correctCount = 0

    # Create array of guesses so that 'same group' atoms don't go orange if the correct atom is later in the guess
    guess = []
    for entry in row_entries:
        att = entry.get().strip()
        if att != "":
            if att in pt.keys():
                guess.append(att)
    print(guess)
    # prevent same atom being double counted as green - remove said atom once it's been 'used'
    molecule_check = molecule_f.copy()
    for entry in row_entries:
        atom = entry.get().strip()
        # prevent errors from typos
        if (atom not in pt.keys()) & (atom != ''):
            entry.config(bg='red')
            continue
        if atom in molecule_check:
            entry.config(bg="green")
            # correctFlag[atom] = True
            correctCount += 1
            molecule_check.remove(atom)
            continue
        if (atom not in molecule_check) & (atom != ""):
            if pt[atom] in [pt[a] for a in molecule_check]:
                group = pt[atom]
                mark = True
                # check correct atom won't be later in molecule
                for check_a in molecule_check:
                    if (pt[check_a] == group) & (check_a not in guess):
                        entry.config(bg="orange")
                        molecule_check.remove(check_a)
                        mark = False
                        break
                if mark:
                    entry.config(bg='red')

            elif (pt[atom] in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]) & (True in [pt[el] in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] for el in molecule_check]):
                entry.config(bg="blue")
                continue
            else:
                entry.config(bg="red")
                continue
        # if atom=="":
        #     entry.config(bg="red")
        #     continue
    # all([value for value in correctFlag.values()]):
    if correctCount == len(molecule_f) == len(guess):
        for entry in row_entries:
            entry.config(bg="green")


def main():
    root = tk.Tk()
    root.title("Image and Entry Fields")
    
    # Set minimum window size
    root.minsize(600, 500)
    
    # Make the window resizable
    root.resizable(True, True)

    # Create image label
    image_label = tk.Label(root)
    image_label.grid(row=0, column=0, columnspan=6, pady=10)
    
    image_path = "Test_images/Spectrle_test_ZrO.png"  # change
    molecule = ["Zr", "O"]  # change

    periodicTable = periodic_table = {
        "H": 1,
        "Li": 1,
        "Na": 1,
        "K": 1,
        "Rb": 1,
        "Cs": 1,
        "Fr": 1,
        "Be": 2,
        "Mg": 2,
        "Ca": 2,
        "Sr": 2,
        "Ba": 2,
        "Ra": 2,
        "Sc": 3,
        "Y": 3,
        "La": 3,
        "Ac": 3,
        "Ti": 4,
        "Zr": 4,
        "Hf": 4,
        "Rf": 4,
        "V": 5,
        "Nb": 5,
        "Ta": 5,
        "Db": 5,
        "Cr": 6,
        "Mo": 6,
        "W": 6,
        "Sg": 6,
        "Mn": 7,
        "Tc": 7,
        "Re": 7,
        "Bh": 7,
        "Fe": 8,
        "Ru": 8,
        "Os": 8,
        "Hs": 8,
        "Co": 9,
        "Rh": 9,
        "Ir": 9,
        "Mt": 9,
        "Ni": 10,
        "Pd": 10,
        "Pt": 10,
        "Ds": 10,
        "Cu": 11,
        "Ag": 11,
        "Au": 11,
        "Rg": 11,
        "Zn": 12,
        "Cd": 12,
        "Hg": 12,
        "Cn": 12,
        "B": 13,
        "Al": 13,
        "Ga": 13,
        "In": 13,
        "Tl": 13,
        "Nh": 13,
        "C": 14,
        "Si": 14,
        "Ge": 14,
        "Sn": 14,
        "Pb": 14,
        "Fl": 14,
        "N": 15,
        "P": 15,
        "As": 15,
        "Sb": 15,
        "Bi": 15,
        "Mc": 15,
        "O": 16,
        "S": 16,
        "Se": 16,
        "Te": 16,
        "Po": 16,
        "Lv": 16,
        "F": 17,
        "Cl": 17,
        "Br": 17,
        "I": 17,
        "At": 17,
        "Ts": 17,
        "He": 18,
        "Ne": 18,
        "Ar": 18,
        "Kr": 18,
        "Xe": 18,
        "Rn": 18,
        "Og": 18,
        "+": -2,
    }

    # Create entry fields
    rows = 5
    columns = 5
    entry_grid = create_entry_grid(root, rows, columns)
    
    # Create buttons for each row
    for i in range(rows):
        button = tk.Button(root, text="Check", command=lambda row=i: check_answers(
            entry_grid[row], molecule, periodicTable))
        button.grid(row=i+1, column=columns, padx=5, pady=5)

    # Initial image load
    def on_configure(event=None):
        """Called when window is resized"""
        if event and event.widget == root:
            root.after_idle(lambda: update_image_size(root, image_label, image_path))
    
    # Bind window resize event
    root.bind('<Configure>', on_configure)
    
    # Load initial image
    root.after(100, lambda: update_image_size(root, image_label, image_path))

    root.mainloop()


if __name__ == "__main__":
    main()