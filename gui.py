import tkinter as tk
from task_manager import run_task

TASKS = {
    "": {
        "key": "standard",
        "inputs": []
    },
    "Criar Usuário": {
        "key": "create",
        "inputs": ["Nome Completo", "Email", "Usuario Espelho",
                   {"label": "Espelhar Agenda", "type": "checkbox"}]
    },
    "Resetar Usuário": {
        "key": "reset",
        "inputs": ["Usuario", "Base SOC"]
    },
    "Inativar Usuário": {
        "key": "inactivate",
        "inputs": ["Usuario", "Base SOC"]
    },
    "Espelhar Usuário": {
        "key": "copycat",
        "inputs": ["Usuario", "Usuario Espelho", "Base SOC", 
                   {"label": "Acessos", "type": "checkbox"}, 
                   {"label": "Empresas", "type": "checkbox"}, 
                   {"label": "Agenda", "type": "checkbox"}]
    },
    "Coletar Deduplicador": {
        "key": "dedup_data",
        "inputs": ["Codigo Empresa", 
                   {"label": "Completo", "type": "checkbox"}]
        
    },
    "Rodar Deduplicador": {
        "key": "dedup_run",
        "inputs": ["Codigo Empresa"]
    },
    "Validador Matricula": {
        "key": "mat_validate",
        "inputs": ["Codigo Empresa"]
    }
    
}

def launch_gui():

    def update_inputs(*_):
        # Clear current input fields
        for widget in input_frame.winfo_children():
            widget.destroy()

        selected_display = task_var.get()
        inputs = TASKS[selected_display]["inputs"]
        entry_fields.clear()

        for item in inputs:
            
            if isinstance(item, str):
                tk.Label(input_frame, text=item).pack(anchor="w")
                entry = tk.Entry(input_frame, show="*" if "password" in item.lower() else "")
                entry.pack(fill="x")
                entry_fields[item] = entry

            elif isinstance(item, dict) and item.get("type") == "checkbox":
                var = tk.BooleanVar()
                cb = tk.Checkbutton(input_frame, text=item["label"], variable=var)
                cb.pack(anchor="w")
                entry_fields[item["label"]] = var

    def on_run():
        selected_display = task_var.get()
        task_key = TASKS[selected_display]["key"]
         # Collect input values
        inputs = {}
        for label, widget in entry_fields.items():
            if isinstance(widget, tk.Entry):
                inputs[label] = widget.get()
            elif isinstance(widget, tk.BooleanVar):
                inputs[label] = widget.get()
        run_task(task_key, inputs)

    def center_window(win, width=600, height=400):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        win.geometry(f"{width}x{height}+{x}+{y}")

    root = tk.Tk()
    root.title("Aposenta SOC")
    center_window(root, 600, 400)
    root.resizable(False, False)

    task_var = tk.StringVar(value=list(TASKS.keys())[0])
    entry_fields = {}

    tk.Label(root, text="Escolher Tarefa").pack(pady=5)
    tk.OptionMenu(root, task_var, *TASKS.keys(), command=update_inputs).pack()

    input_frame = tk.Frame(root)
    input_frame.pack(pady=10, fill="x")

    tk.Button(root, text="Executar Tarefa", command=on_run).pack(pady=10)

    update_inputs()
    root.mainloop()