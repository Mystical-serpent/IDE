# IDE
Personal IDE made in python! Allows the users to create or open an existing file and run the program.

## NOTE!
* No syntax highlighting present.
* Indentation feature is NOT present.
* Code is NOT polished with errors included :)
  
## Interpreter
The code is redirected to the cmd for execution.
```python
process = subprocess.Popen(
    ["python", os.path.join(Off_directory, "temp_code.py")],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdin=subprocess.PIPE,
    text=True
)
```
## Opening a file
```python
import tkinter as t
from tkinter import filedialog

def open_and_read_file():
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py")]
    )
    
    if file_path:
        try:
            with open(file_path, "r") as file:
                content = file.read()
                print(f"Opened file: {file_path}")
                print(content)
        except Exception as e:
            print(f"Error loading file: {e}")
    else:
        print("No file selected.")

root = t.Tk()
root.withdraw()
open_and_read_file()

```

## Creating a file (Backend)
```python
import os
import subprocess
import threading

Off_directory = "C:/PythonIDE"
os.makedirs(Off_directory, exist_ok=True)

def save_file_name():
    filename = input("Enter file name: ").strip()
    if filename:
        return filename
    else:
        print("File name cannot be empty.")
        return None

def Creating_Project():
    global status
    status = "Created"

    given_directory = input("Enter the directory to save the file: ").strip()
    if not given_directory:
        return

    file_name_given = save_file_name()
    if not file_name_given:
        return

    try:
        file_path = os.path.join(given_directory, f"{file_name_given}.py")
        with open(file_path, "w") as file:
            pass
        print(f"Created file: {file_path}")
        Writing_area(file_path)
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Failed to create the file. Try again.")

def Writing_area(file_path):
    print(f"Editing file: {file_path}")
    code = input("Enter your code here:\n")

    def run_code():
        terminal = subprocess.Popen(
            ["python", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True
        )

        def read_stream(stream):
            for line in iter(stream.readline, ""):
                print(line, end="")

        threading.Thread(target=read_stream, args=(terminal.stdout,), daemon=True).start()
        threading.Thread(target=read_stream, args=(terminal.stderr,), daemon=True).start()

        try:
            with open(file_path, "w") as temp_file:
                temp_file.write(code)
        except Exception as e:
            print(f"Error: {str(e)}")

    run_code()

def open_project_with_file():
    file_path = input("Enter the file path to open: ").strip()
    if file_path:
        Writing_area(file_path)

```
## Example 
![Image](https://github.com/user-attachments/assets/81170e97-b7f4-403a-addf-a6dc82bcec9f)

