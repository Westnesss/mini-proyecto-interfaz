# MenuGUI.py
import tkinter as tk

class MenuGUI:
    def __init__(self, root, menu):
        self.root = root
        self.root.title("Program Monitor")
        self.menu = menu

        # Crear un frame para los botones a la izquierda
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, padx=10)

        self.label = tk.Label(self.left_frame, text="Seleccione una opción:")
        self.label.pack()

        self.entry_program = tk.Entry(self.left_frame)
        self.entry_program.pack()

        self.button_add = tk.Button(self.left_frame, text="1. Agregar programa", command=self.add_program)
        self.button_add.pack()

        self.button_remove = tk.Button(self.left_frame, text="2. Eliminar programa", command=self.remove_program)
        self.button_remove.pack()

        self.button_show = tk.Button(self.left_frame, text="3. Mostrar programas", command=self.show_programs)
        self.button_show.pack()

        self.button_start = tk.Button(self.left_frame, text="4. Iniciar monitoreo", command=self.start_monitoring)
        self.button_start.pack()

        self.button_stop_monitoring_gui = tk.Button(self.left_frame, text="Detener monitoreo", command=self.stop_monitoring_gui)
        self.button_stop_monitoring_gui.pack()

        self.button_exit = tk.Button(self.left_frame, text="6. Salir", command=self.exit_program)
        self.button_exit.pack()

        # Crear un frame para el texto a la derecha
        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, padx=10)

        self.text_display = tk.Text(self.right_frame, height=10, width=40)
        self.text_display.pack()

    def add_program(self):
        program_name = self.entry_program.get()
        if program_name:
            self.menu.PROGRAM_MONITOR.PROGRAMS_TO_LOG.append(program_name)
            self.entry_program.delete(0, tk.END)  # Limpiar la entrada después de agregar

    def remove_program(self):
        self.menu.remove_program_from_monitor_list()

    def show_programs(self):
        programs_list = self.menu.PROGRAM_MONITOR.PROGRAMS_TO_LOG
        programs_text = "\n".join(programs_list)
        self.text_display.delete(1.0, tk.END)  # Limpiar el contenido actual
        self.text_display.insert(tk.END, programs_text)

    def start_monitoring(self):
        self.menu.start_monitoring()

    def stop_monitoring_gui(self):
        self.menu.stop_monitoring()

    def exit_program(self):
        print("Saliendo del programa...")
        self.root.destroy()


