import os
import subprocess
import threading
import tkinter as t
from tkinter import filedialog
from tkinter import ttk

status = None
filename = ""

# Default directory for temporary files
Off_directory = "C:/PythonIDE"
os.makedirs(Off_directory, exist_ok=True)


def Opening_Project():
    """Open an existing project file."""
    global status
    status = "Opened"

    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py")]
    )

    if file_path:
        print(f"Opened file: {file_path}")  # Debugging log
        return file_path
    else:
        return None


def show_error(message):
    """Display an error message."""
    error_window = t.Toplevel()
    error_window.geometry("300x150")
    error_window.title("Error")

    label = t.Label(error_window, text=message, fg="red", font=("Calibri", 16))
    label.pack(padx=10, pady=20)

    close_button = t.Button(
        error_window,
        text="Close",
        font=("Calibri", 12),
        command=error_window.destroy
    )
    close_button.pack(pady=10)


def save_file_name():
    """Prompt the user to give a file name."""
    global filename
    name_window = t.Toplevel()
    name_window.geometry("300x200")
    name_window.title("Give File Name")

    label = t.Label(name_window, text="File Name: ", fg="black", font=("Calibri", 20))
    label.pack(padx=5, pady=10)

    text_area = t.Entry(name_window, font=("Calibri", 20))
    text_area.pack(padx=5, pady=10)

    def on_save():
        global filename
        filename = text_area.get().strip()
        if filename:
            name_window.destroy()
        else:
            show_error("File name cannot be empty.")

    save_button = t.Button(
        name_window,
        text="Save",
        font=("Calibri", 12),
        command=on_save
    )
    save_button.pack(padx=5, pady=10)

    # Make the window modal
    name_window.grab_set()
    name_window.wait_window()

    return filename


def Creating_Project():
    """Create a new project file."""
    global status
    status = "Created"

    given_directory = filedialog.askdirectory(title="Select a directory")
    if not given_directory:
        return  # User canceled directory selection

    file_name_given = save_file_name()
    if not file_name_given:
        return  # User canceled or gave invalid file name

    try:
        file_path = os.path.join(given_directory, f"{file_name_given}.py")
        with open(file_path, "w") as file:
            pass
        print(f"Created file: {file_path}")
        Writing_area(file_path)
    except Exception as e:
        print(f"Error occurred: {e}")
        show_error("Failed to create the file. Try again.")


def Writing_area(file_path):
    """Create the writing area in the Notepad-like interface."""
    Programming_place = t.Toplevel()
    Programming_place.geometry("800x500")
    Programming_place.configure(bg="lightblue")
    Programming_place.title("Programming Area")

    notebook = ttk.Notebook(Programming_place)
    notebook.pack(expand=True, fill="both")

    tab_area = ttk.Frame(notebook)
    file_name = os.path.basename(file_path)
    notebook.add(tab_area, text=file_name)

    text_area = t.Text(tab_area, wrap="word", height=20, width=100)
    text_area.pack(padx=20, pady=20)

    def run_code():
        """Run the code in the text area."""
        code = text_area.get(1.0, t.END)
        terminal = t.Toplevel()
        terminal.geometry("600x400")
        terminal.title("Output")

        output_text = t.Text(terminal, wrap="word", height=20, width=80, bg="black", fg="white")
        output_text.pack(padx=10, pady=10, fill="both", expand=True)

        input_frame = t.Frame(terminal)
        input_frame.pack(fill="x", padx=10, pady=5)

        input_label = t.Label(input_frame, text="Input:", font=("Calibri", 12))
        input_label.pack(side="left", padx=5)

        input_entry = t.Entry(input_frame, font=("Calibri", 12), width=40)
        input_entry.pack(side="left", fill="x", expand=True, padx=5)

        def send_input():
            """Send user input to the subprocess."""
            user_input = input_entry.get()
            if process and process.stdin:
                process.stdin.write(user_input + "\n")
                process.stdin.flush()
            input_entry.delete(0, t.END)

        send_button = t.Button(input_frame, text="Send", font=("Calibri", 12), command=send_input)
        send_button.pack(side="left", padx=5)

        process = None

        def execute():
            """Run the code in a subprocess with interactive input support."""
            nonlocal process
            with open(os.path.join(Off_directory, "temp_code.py"), "w") as temp_file:
                temp_file.write(code)

            try:
                process = subprocess.Popen(
                    ["python", os.path.join(Off_directory, "temp_code.py")],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    text=True
                )

                def read_stream(stream, output_text):
                    """Read and display the output or error stream."""
                    for line in iter(stream.readline, ""):
                        output_text.insert(t.END, line)
                        output_text.see(t.END)

                # Start threads for stdout and stderr
                threading.Thread(target=read_stream, args=(process.stdout, output_text), daemon=True).start()
                threading.Thread(target=read_stream, args=(process.stderr, output_text), daemon=True).start()

            except Exception as e:
                output_text.insert(t.END, f"Error: {str(e)}\n")

        # Run code execution in a separate thread
        threading.Thread(target=execute, daemon=True).start()

    button_run = t.Button(tab_area, text="Run", font=("Calibri", 20), command=run_code)
    button_run.pack(padx=20, pady=20)

    try:
        with open(file_path, "r") as file:
            content = file.read()
            text_area.insert(t.END, content)
    except Exception as e:
        print(f"Error loading file: {e}")


def open_project_with_file():
    """Open the selected project file in a text area."""
    file_path = Opening_Project()
    if file_path:
        Writing_area(file_path)


def start_up_window():
    """Create the main startup window."""
    root = t.Tk()
    root.geometry("800x800")
    root.configure(bg="lightblue")
    root.title("IDE")

    Window_label = t.Label(
        root, text="Get Started:", font=("Calibri", 40), bg="lightblue"
    )
    Create_project = t.Button(
        root,
        text="Create Project",
        font=("Calibri", 30),
        highlightbackground="black",
        highlightcolor="lightblue",
        padx=10,
        pady=5,
        command=Creating_Project,
    )

    Open_project = t.Button(
        root,
        text="Open Project",
        font=("Calibri", 30),
        highlightbackground="black",
        highlightcolor="lightblue",
        padx=10,
        pady=5,
        command=open_project_with_file,
    )

    exit_button = t.Button(
        root,
        text="Exit",
        font=("Calibri", 25),
        padx=100,
        pady=5,
        command=root.destroy,
    )

    Window_label.grid(padx=10, pady=30)
    Open_project.grid(row=1, column=0, padx=97, pady=50)
    Create_project.grid(row=1, column=1, padx=3, pady=5)
    exit_button.grid(row=2, column=0, padx=3, pady=5)

    root.mainloop()


# Start the main application
start_up_window()
