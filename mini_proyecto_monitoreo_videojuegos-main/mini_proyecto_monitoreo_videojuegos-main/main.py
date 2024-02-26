# main.py
from scr.Menu import Menu
from scr.MenuGUI import MenuGUI
from scr.ProgramMonitor import ProgramMonitor
import tkinter as tk

def main():
    menu = Menu()

    root = tk.Tk()
    menu_gui = MenuGUI(root, menu)
    
    while True:
        menu.show_menu()
        option = input("Seleccione una opción: ")
        menu.execute_option(option)

if __name__ == "__main__":
    main()

