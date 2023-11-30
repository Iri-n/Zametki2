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





ButtonFrame = LabelFrame(root, text='', bg="lightgray", font=('Consolas', 14))
ButtonFrame.grid(row=5, column=0, columnspan=6)


btnShow = Button(ButtonFrame, text="Print", padx=20, pady=10)
btnShow.pack(side=LEFT)

btnAdd = Button(ButtonFrame, text="Add", padx=20, pady=10)
btnAdd.pack(side=LEFT)

btnUpdate = Button(ButtonFrame, text="Update", padx=20, pady=10)
btnUpdate.pack(side=LEFT)

btnDelete = Button(ButtonFrame, text="Delete", padx=20, pady=10)
btnDelete.pack(side=LEFT)

btnClear = Button(ButtonFrame, text="Cancel", padx=18, pady=10)
btnClear.pack(side=LEFT)

btnExit = Button(ButtonFrame, text="Exit", padx=20, pady=10)
btnExit.pack(side=LEFT)


load_json_from_file()
load_trv_with_json()

root.mainloop()
