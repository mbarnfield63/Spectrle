import tkinter as tk
from tkinter import ttk
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

    # Load an image
    image_label = tk.Label(root)
    image_label.grid(row=0, column=0, columnspan=5)
    image_path = "Spectrle_250923.png"  # change
    image = tk.PhotoImage(file=image_path)
    image_label.config(image=image)

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

    root.mainloop()


if __name__ == "__main__":
    main()
