# IDE
Personal IDE made in python using tkinter for the backend and using subprocess to run the code using cmd. The code is executed by:
"process = subprocess.Popen(
    ["python", os.path.join(Off_directory, "temp_code.py")],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdin=subprocess.PIPE,
    text=True
)".
 This, stores the user code in temp_code file and that is opened and interpreted by cmd. The main programming area is does not contain functions like: indentation or syntax highlighting so the user must be careful when running a code. 
 File handeling is present in the code and allows the user to open or create an existing file.


![Image](https://github.com/user-attachments/assets/81170e97-b7f4-403a-addf-a6dc82bcec9f)

