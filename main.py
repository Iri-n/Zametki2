from tkinter import *
from tkinter import ttk
import uuid
from datetime import datetime
import json

global my_data_list
my_data_list = []

root = Tk()
root.title('Заметки')
root.geometry("700x680")
root.configure(bg='LightBlue')

input_frame = LabelFrame(root, text='О заметке:', bg="lightgray", font=('Consolas', 14))
input_frame.grid(row=0, column=0, rowspan=5, columnspan=4)

Label(input_frame, anchor="w", width=24,
      height=1, relief="ridge", text="ID",
      font=('Consolas', 14)).grid(row=1, column=0)

Label(input_frame, anchor="w", width=24,
      height=1, relief="ridge", text="Дата",
      font=('Consolas', 14)).grid(row=2, column=0)

Label(input_frame, anchor="w", width=24,
      height=1, relief="ridge", text="Название заметки",
      font=('Consolas', 14)).grid(row=3, column=0)

Label(input_frame, anchor="w", width=24,
      height=1, relief="ridge", text="Заметка",
      font=('Consolas', 14)).grid(row=4, column=0)

id_value = StringVar()
id_value.set(uuid.uuid4())

id_date = datetime.now()

crm_id = Label(input_frame, anchor="w", height=1,
               relief="ridge", textvariable=id_value, font=('Consolas', 14))
crm_id.grid(row=1, column=1)

crm_date = Entry(input_frame, width=36, borderwidth=2, fg="black", font=('Consolas', 14))
crm_date.grid(row=2, column=1, columnspan=2)
crm_date.insert(0, id_date.strftime("%m/%d/%Y, %H:%M:%S"))

crm_name = Entry(input_frame, width=36, borderwidth=2, fg="black", font=('Consolas', 14))
crm_name.grid(row=3, column=1, columnspan=2)

crm_note = Entry(input_frame, width=36, borderwidth=2, fg="black", font=('Consolas', 14))
crm_note.grid(row=4, column=1, columnspan=2, sticky=NW)

trv = ttk.Treeview(root, columns=(1, 2, 3, 4), show="headings", height="16")
trv.grid(row=11, column=0, rowspan=16, columnspan=4)

trv.heading(1, text="ID", anchor="center")
trv.heading(2, text="Название заметки", anchor="center")
trv.heading(3, text="Дата", anchor="center")
trv.heading(4, text="Заметка", anchor="center")

trv.column("#1", anchor="w", width=270, stretch=True)
trv.column("#2", anchor="w", width=140, stretch=False)
trv.column("#3", anchor="w", width=140, stretch=False)
trv.column("#4", anchor="w", width=140, stretch=False)


def load_json_from_file():
    global my_data_list
    with open("notes.json", "r") as file_handler:
        my_data_list = json.load(file_handler)
    file_handler.close
    print('file has been read and closed')


def save_json_to_file():
    global my_data_list
    with open("notes.json", "w") as file_handler:
        json.dump(my_data_list, file_handler, indent=4)
    file_handler.close
    print('file has been written to and closed')


def remove_all_data_from_trv():
    for item in trv.get_children():
        trv.delete(item)


def load_trv_with_json():
    global my_data_list

    remove_all_data_from_trv()

    rowIndex = 1

    for key in my_data_list:
        n_id_value = key["id"]
        name = key["name"]
        date = key["date"]
        note = key["note"]

        trv.insert('', index='end', iid=rowIndex, text="",
                   values=(n_id_value, name, date, note))
        rowIndex = rowIndex + 1

def clear_all_fields():
    crm_name.delete(0, END)
    crm_date.delete(0, END)
    crm_note.delete(0, END)
    crm_id.configure(text="")
    crm_name.focus_set()
    id_value.set(uuid.uuid4())
    change_background_color("#FFFFFF")



def find_row_in_my_data_list(n_id_value):
    global my_data_list
    row = 0
    found = False

    for rec in my_data_list:
        if rec["id"] == n_id_value:
            found = True
            break
        row = row + 1

    if (found == True):
        return (row)

    return (-1)



def change_background_color(new_color):
    crm_name.config(bg=new_color)
    crm_date.config(bg=new_color)
    crm_note.config(bg=new_color)



def change_enabled_state(state):
    if state == 'Edit':
        btnUpdate["state"] = "normal"
        btnDelete["state"] = "normal"
        btnAdd["state"] = "disabled"
    elif state == 'Cancel':
        btnUpdate["state"] = "disabled"
        btnDelete["state"] = "disabled"
        btnAdd["state"] = "disabled"
    else:
        btnUpdate["state"] = "disabled"
        btnDelete["state"] = "disabled"
        btnAdd["state"] = "normal"



def load_edit_field_with_row_data(_tuple):
    if len(_tuple) == 0:
        return;

    id_value.set(_tuple[0]);
    crm_name.delete(0, END)
    crm_name.insert(0, _tuple[1])
    crm_date.delete(0, END)
    crm_date.insert(0, _tuple[2])
    crm_note.delete(0, END)
    crm_note.insert(0, _tuple[3])



def cancel():
    clear_all_fields()
    change_enabled_state('New')



def print_all_entries():
    global my_data_list

    for rec in my_data_list:
        print(rec)

    crm_name.focus_set();



def add_entry():
    n_id_value = id_value.get()
    name = crm_name.get()
    date = crm_date.get()
    text = crm_note.get()

    if len(name) == 0:
        change_background_color("#FFB2AE")
        return

    process_request('_INSERT_', n_id_value, name, date, text)



def update_entry():
    n_id_value = id_value.get()
    name = crm_name.get()
    date = crm_date.get()
    note = crm_note.get()

    if len(name) == 0:
        change_background_color("#FFB2AE")
        return

    process_request('_UPDATE_', n_id_value, name, date, note)



def delete_entry():
    n_id_value = id_value.get()
    process_request('_DELETE_', n_id_value, None, None, None)



def process_request(command_type, n_id_value, name, date, note):
    global my_data_list

    if command_type == "_UPDATE_":
        row = find_row_in_my_data_list(n_id_value)
        if row >= 0:
            dict = {"id": n_id_value, "name": name,
                    "date": date, "note": note}
            my_data_list[row] = dict

    elif command_type == "_INSERT_":
        dict = {"id": n_id_value, "name": name,
                "date": date, "note": note}
        my_data_list.append(dict)

    elif command_type == "_DELETE_":
        row = find_row_in_my_data_list(n_id_value)
        if row >= 0:
            del my_data_list[row];

    save_json_to_file();
    load_trv_with_json();
    clear_all_fields();



def MouseButtonUpCallBack(event):
    currentRowIndex = trv.selection()[0]
    lastTuple = (trv.item(currentRowIndex, 'values'))
    load_edit_field_with_row_data(lastTuple)

    change_enabled_state('Edit')



trv.bind("<ButtonRelease>", MouseButtonUpCallBack)



ButtonFrame = LabelFrame(root, text='', bg="lightgray", font=('Consolas', 14))
ButtonFrame.grid(row=5, column=0, columnspan=6)


btnShow = Button(ButtonFrame, text="Print", padx=20, pady=10, command=print_all_entries)
btnShow.pack(side=LEFT)

btnAdd = Button(ButtonFrame, text="Add", padx=20, pady=10, command=add_entry)
btnAdd.pack(side=LEFT)

btnUpdate = Button(ButtonFrame, text="Update", padx=20, pady=10, command=update_entry)
btnUpdate.pack(side=LEFT)

btnDelete = Button(ButtonFrame, text="Delete", padx=20, pady=10, command=delete_entry)
btnDelete.pack(side=LEFT)

btnClear = Button(ButtonFrame, text="Cancel", padx=18, pady=10, command=cancel)
btnClear.pack(side=LEFT)

btnExit = Button(ButtonFrame, text="Exit", padx=20, pady=10, command=root.quit)
btnExit.pack(side=LEFT)


load_json_from_file()
load_trv_with_json()

root.mainloop()
