import customtkinter as ctk
import tkinter as tk
from tkinter import font
from tkinter import filedialog as TkFileDialog
from pyperclip import copy
from pyperclip import paste
import CTkMenuBar as ctkmb

root = ctk.CTk()

root.after(0, lambda: root.state("zoomed"))
root.title("Digital Logic Simulator")
root.iconbitmap("_internal/icon/Logicians.ico")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

code_entry = ctk.CTkTextbox(root, width=1500, height=490, text_color="white", font=("Arial", 12), border_width=0, fg_color="#3e3e3e")
code_entry.place(x=10, y=35)

terminal = ctk.CTkTextbox(root, width=600, height=230, state=ctk.DISABLED, fg_color="#2e2e2e")
terminal.place(x=300, y=530)

error_terminal = ctk.CTkTextbox(root, width=590, height=230, state=ctk.DISABLED, fg_color="#1e1e1e", text_color="red")
error_terminal.place(x=920, y=530)


#region Shell
shell = ctk.CTkEntry(root, width=250, height=40, fg_color="#3e3e3e", text_color="green")
shell.place(x=30, y=675)


def replace(pars):
    to_replace, replace_with = pars
    my_code = str(code_entry.get("1.0", tk.END))
    new_text = my_code.replace(to_replace, replace_with)
    code_entry.delete("1.0", tk.END)
    code_entry.insert("1.0", new_text)

def delete(line, c: str):
    lines = c.splitlines()
    lines.remove(lines[int(line) - 1])
    final = ""
    for i in lines:
        final += f"{i}\n"
    code_entry.delete(1.0, ctk.END)
    code_entry.insert(ctk.END, final)

def handle_shell():
    my_code = str(code_entry.get("1.0", tk.END))
    shell_input = str(shell.get()).replace("\n", "")
    if shell_input.startswith("REPLACE "):
        replace(shell_input[8:].split(" WITH "))
    if shell_input.startswith("REMOVE "):
        replace([shell_input[7:], ""])
    if shell_input.startswith("APPEND "):
        replace([my_code, my_code + shell_input[8:]])
    if shell_input.startswith("DELETE "):
        delete(shell_input[7:], my_code)
    if shell_input == "EXIT" or shell_input == "QUIT":
        root.quit()
    shell.delete(0, ctk.END)



shell_submit = ctk.CTkButton(root, text="Progress Shell", width=250, height=40, command=handle_shell)
shell_submit.place(x=30, y=720)


#endregion







def is_int(input) -> bool:
    try:
        int(input)
    except:
        return False
    return True

isReadingFunction = False
isInNonReadFunction = False
function_data = {}
line_at_before_function_call = 0


current_line = 0
data = {}
display = []



def update_terminal(input: str):
    terminal.configure(state=ctk.NORMAL)
    terminal.delete(1.0, ctk.END)
    terminal.insert(ctk.END, input)
    terminal.configure(state=ctk.DISABLED)

def insert_code(input: str, newLine: bool):
    if newLine: code_entry.insert(ctk.END, f"\n{input}")
    else: code_entry.insert(ctk.END, input)

def raise_error(input: str):
    error_terminal.configure(state=ctk.NORMAL)
    error_terminal.delete(1.0, ctk.END)
    error_terminal.insert(ctk.END, input)
    error_terminal.configure(state=ctk.DISABLED)

def add_error(input: str, newLine: bool):
    error_terminal.configure(state=ctk.NORMAL)
    if newLine: error_terminal.insert(ctk.END, f"\n{input}")
    else: error_terminal.insert(ctk.END, f"{input}\n")
    error_terminal.configure(state=ctk.DISABLED)

def get_all_data() -> dict:
    return {**data, **function_data}

def return_interpreter_value(value: str) -> any:
    try:
        isDict = get_all_data()[str(value)]
    except:
        return int(value)
    return get_all_data()[str(value)]

def save():
    file_to_save = str(TkFileDialog.asksaveasfilename(title="Save File", filetypes=[("Low Level Program", "*.llp")]))
    if not file_to_save: return
    with open(f"{file_to_save}.llp", "w") as file:
        file.write(code_entry.get("1.0", tk.END))
def load():
    file_to_load = str(TkFileDialog.askopenfilename(title="Load File", filetypes=[("Low Level Program", "*.llp")]))
    if not file_to_load: return
    with open(file_to_load, 'r') as file:
        data = file.read()
    code_entry.delete("1.0", tk.END)
    code_entry.insert(tk.END, data)

#region Menu
menubar = ctkmb.CTkMenuBar(root, bg_color="#1e1e1e")
filemenu = menubar.add_cascade("File")
editmenu = menubar.add_cascade("Edit")
insertmenu = menubar.add_cascade("Insert")

file_dropdown = ctkmb.CustomDropdownMenu(filemenu)
file_dropdown.add_option(option="Save File", command=save)
file_dropdown.add_option(option="Open File", command=load)
file_dropdown.add_separator()
file_dropdown.add_option(option="Exit", command=root.quit)


edit_dropdown = ctkmb.CustomDropdownMenu(editmenu)
edit_dropdown.add_option(option="Copy All", command=lambda: copy(str(code_entry.get("1.0", tk.END))))
edit_dropdown.add_option(option="Paste", command=lambda: insert_code(root.clipboard_get(), False))
edit_dropdown.add_separator()





insertmenu = ctkmb.CustomDropdownMenu(insertmenu)
insertmenu.add_option(option="SET Command", command=lambda:insert_code("SET [variable name], [value]", True))
insertmenu.add_option(option="GLOBAL SET Command", command=lambda:insert_code("GSET [variable name], [value]", True))
insertmenu.add_option(option="DISPLAY Command", command=lambda:insert_code("DIS [flag], [input]", True))
insertmenu.add_option(option="OUTPUT Command", command=lambda:insert_code("OUT [flag], [input]", True))
insertmenu.add_option(option="ADD Operation", command=lambda:insert_code("ADD [in 1] [in 2] [out]", True))
insertmenu.add_option(option="SUBTRACT Operation", command=lambda:insert_code("SUB [in 1] [in 2] [out]", True))
insertmenu.add_option(option="MULTIPLY Operation", command=lambda:insert_code("MUP [in 1] [in 2] [out]", True))
insertmenu.add_option(option="DIVIDE Operation", command=lambda:insert_code("DIV [in 1] [in 2] [out]", True))
insertmenu.add_option(option="MOVE Command", command=lambda:insert_code("MOV [in] [out]", True))
insertmenu.add_option(option="RESET Command", command=lambda:insert_code("RESET", True))
insertmenu.add_option(option="RESET DISPLAY Command", command=lambda:insert_code("REDIS", True))
insertmenu.add_option(option="RAISE ERROR Command", command=lambda:insert_code("RAE [error to raise]", True))
insertmenu.add_option(option="SLIDE Command", command=lambda:insert_code("SLD [lines to slide]", True))
insertmenu.add_option(option="SLIDE IF Command", command=lambda:insert_code("SIF [variable], [value to check] [lines to slide]", True))
insertmenu.add_option(option="SLIDE IF NOT Command", command=lambda:insert_code("SOT [variable], [value to check] [lines to slide]", True))
insertmenu.add_option(option="FUNCTION Declarement", command=lambda:insert_code(".function [function name]\n[Your Code]\n.endfunction", True))
insertmenu.add_option(option="COMMENT Line", command=lambda:insert_code(";[Your Comment]", True))

def reset(*args):
    global data
    global display
    if "data" in args: data.clear()
    if "display" in args: display.clear()
    if "function" in args: function_data.clear()

#Data Menu

data_reset_type = tk.IntVar()
data_reset_type.set(1)

#endregion






#region ######################################LOGIC#######################################

def end():
    output = ""
    for item in display:
        output += str(item)
    update_terminal(output)
def SET(pars: str):
    for par in pars:
        par = par.strip()
    parameters = pars
    if not isReadingFunction: data[parameters[0]] = int(parameters[1])
    else: function_data[parameters[0]] = int(parameters[1])
def GSET(pars: str):
    for par in pars:
        par = par.strip()
    parameters = pars
    data[parameters[0]] = int(parameters[1])
def ADD(pars: str):
    for par in pars:
        par = par.strip()
    a, b, c = pars
    output = return_interpreter_value(a) + return_interpreter_value(b)
    data[c] = output
def SUB(pars: str):
    for par in pars:
        par = par.strip()
    a, b, c = pars
    output = return_interpreter_value(a) - return_interpreter_value(b)
    data[c] = output
def MUP(pars: str):
    for par in pars:
        par = par.strip()
    a, b, c = pars
    output = return_interpreter_value(a) * return_interpreter_value(b)
    data[c] = output
def DIV(pars: str):
    for par in pars:
        par = par.strip()
    a, b, c = pars
    output = return_interpreter_value(a) / return_interpreter_value(b)
    data[c] = output
def DIS(pars, line):
    global raised_error
    for par in pars:
        par = par.strip()
    try:
        flag, value = pars
        value = str(value).strip()
        if flag == "dt": display.append(get_all_data()[value])
        if flag == "tx": display.append(value)
        else: raise_error(f"Error: Incorrect flag in DIS Command at line {line + 1}")
    except Exception as e:
        raise_error(f"Error: {e} in line {line + 1}")
        raised_error = True
def OUT(pars, line):
    global raised_error
    for par in pars:
        par = par.strip()
    try:
        flag, value = pars
        value = value.strip()
        if flag == "dt": display.append(f"{get_all_data()[value]}\n")
        if flag == "tx": display.append(f"{value}\n")
        else: raise_error(f"Error: Incorrect flag in OUT Command at line {line + 1}")
    except Exception as e:
        raise_error(f"Error: {e} at line {line + 1}")
        raised_error = True
        return
def MOV(pars, line: int):
    global raised_error
    a, b = pars
    b = b.strip()
    if a in data and b in data:
        data[b] = get_all_data()[a]
    else:
        raise_error(f"Error: Nonexistent variable in MOV at line {line + 1}")
        raised_error = True
        return
def SLD(pars: str):
    global raised_error
    for par in pars:
        par = par.strip()
    global current_line
    try:
        current_line += return_interpreter_value(pars) - 1
    except Exception as e:
        raise_error(f"Error: {e} in line {current_line + 1}")
        raised_error = True
def SIF(pars: str):
    global raised_error
    for par in pars:
        par = par.strip()
    global current_line
    variable, value, line = pars
    if not int(get_all_data()[variable]) == int(value): return
    try:
        current_line += return_interpreter_value(pars) - 1
    except Exception as e:
        raise_error(f"Error: {e} in line {current_line + 1}")
        raised_error = True
def SOT(pars: str):
    global raised_error
    for par in pars:
        par = par.strip()
    global current_line
    variable, value, line = pars
    if int(get_all_data()[variable]) == int(value): return
    try:
        current_line += return_interpreter_value(line) - 1
    except Exception as e:
        raise_error(f"Error: {e} in line {current_line + 1}")
        raised_error = True
def INC(pars: str, line: int):
    global raised_error
    if is_int(str(pars).strip()):
        raise_error(f"Error: Cannot increment an integer at line {line + 1}")
        raised_error = True
        return
    try:
        if isReadingFunction:
            if function_data[pars]: function_data[pars] += 1
            else: data[pars] += 1
        else:
            data[pars] += 1
    except Exception as e:
        raise_error(f"Error: {e} at line {line + 1}")
        raised_error = True
        return
def DEC(pars: str, line: int):
    global raised_error
    if is_int(str(pars).strip()):
        raise_error(f"Error: Cannot increment an integer at line {line + 1}")
        raised_error = True
        return
    try:
        if isReadingFunction:
            if function_data[pars]: function_data[pars] -= 1
            else: data[pars] -= 1
        else:
            data[pars] -= 1
    except Exception as e:
        raise_error(f"Error: {e} at line {line + 1}")
        raised_error = True
        return

#endregion

finished = False
raised_error = False
def run_line(code: str, line_id: int):
    global finished
    global display
    global raised_error
    global isReadingFunction
    global isInNonReadFunction
    global current_line
    global line_at_before_function_call

    finished = False
    line = code.splitlines()[line_id].strip()
    try:
        if isInNonReadFunction:
            if line == ".endfunction":
                isInNonReadFunction = False
            return

        if line == ".endfunction":
            isReadingFunction = False
            isInNonReadFunction = False
            function_data.clear()
            current_line = line_at_before_function_call
            return
        if line.startswith(".function "):
            if not isReadingFunction:
                isInNonReadFunction = True
            return

        if line == "END":
            end()
            finished = True
            return
        elif line == "RESET":
            data.clear()
        elif line == "REDIS":
            display.clear()
            update_terminal("")
        elif line.startswith("SET "):
            SET(line[4:].strip().split(",", 1))
        elif line.startswith("GSET "):
            GSET(line[5:].strip().split(",", 1))
        elif line.startswith("DIS "):
            DIS(line[4:].strip().split(",", 1), line_id)
        elif line.startswith("OUT "):
            OUT(line[4:].strip().split(",", 1), line_id)
        elif line.startswith("MOV "):
            MOV(line[4:].strip().split(",", 1), line_id)
        elif line.startswith("SUB "):
            SUB(line[4:].strip().split())
        elif line.startswith("ADD "):
            ADD(line[4:].strip().split())
        elif line.startswith("MUP "):
            MUP(line[4:].strip().split())
        elif line.startswith("DIV "):
            DIV(line[4:].strip().split())
        elif line.startswith("INC "):
            INC(line[4:].strip(), line_id)
        elif line.startswith("DEC "):
            DEC(line[4:].strip(), line_id)
        elif line == "NEWL":
            display.append("\n")
        elif line.startswith("RAE "):
            raise_error(f'Error: "{line[4:].strip()}" at line {line_id + 1}')
            raised_error = True
            end()
            finished = True
            return
        elif line.startswith("SLD "):
            SLD(line[4:].strip())
        elif line.startswith("SIF "):
            SIF(line[4:].strip().split(",", 2))
        elif line.startswith("SOT "):
            SOT(line[4:].strip().split(",", 2))
        elif line.startswith("CALL "):
            function_name = line[5:].strip()
            code_lines = code.splitlines()
            try:
                line_index = code_lines.index(f".function {function_name}")
            except ValueError:
                raise_error(f'Error: Nonexistent function "{function_name}" at line {line_id + 1}.\n')
                raised_error = True
                return
            line_at_before_function_call = line_id
            isReadingFunction = True
            current_line = line_index
            return
        elif line.strip() == "" or line.strip().startswith(";"):
            pass
        else:
            raise_error(f"Error: Nonexistent command or incorrect capitalization in line {line_id + 1}\n")
            raised_error = True
            return

        if not raised_error:
            raise_error("")

    except Exception as e:
        add_error(f'Error: {e} at line {line_id + 1}\n', False)
def run():
    global data
    global display
    global current_line
    global finished
    code = code_entry.get("1.0", tk.END) #Means read the zeroth character from the first line ("1.0") until the end ("tk.END") 
    lines = code.splitlines()
    raised_error = False
    raise_error("")

    if not "END" in lines: update_terminal(""); raise_error("Error: Cannot halt code due to END Command not being inserted."); return


    if data_reset_type.get() == 1: data = {}; display = []
    if data_reset_type.get() == 2: data = {}
    if data_reset_type.get() == 3: display = []
    if data_reset_type.get() == 4: pass
    current_line = 0

    finished = False
    while current_line < len(code.splitlines()):
        if finished: finished = False; break
        try:
            run_line(code, current_line)
        except Exception as e:
            raise_error(f"ERROR: {e}")
        current_line += 1
    finished = False



edit_dropdown.add_option(option="Run Code", command=run)
edit_dropdown.add_option(option="Clear Terminal", command=lambda: update_terminal(""))
edit_dropdown.add_option(option="Clear Errors", command=lambda: raise_error(""))

run_button = ctk.CTkButton(root, text="Run Code", width=250, height=40, command=run)
run_button.place(x=30, y=530)

clear_terminal = ctk.CTkButton(root, text="Clear Terminal", width=250, height=40, command=lambda:update_terminal(""))
clear_terminal.place(x=30, y=580)

clear_errors = ctk.CTkButton(root, text="Clear Errors", width=250, height=40, command=lambda: raise_error(""))
clear_errors.place(x=30, y=630)


root.mainloop()
