from tkinter import *
from tkinter import ttk
import uuid

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

crm_id = Label(input_frame, anchor="w", height=1,
               relief="ridge", textvariable=id_value, font=('Consolas', 14))
crm_id.grid(row=1, column=1)

crm_date = Entry(input_frame, width=36, borderwidth=2, fg="black", font=('Consolas', 14))
crm_date.grid(row=2, column=1, columnspan=2)

crm_name = Entry(input_frame, width=36, borderwidth=2, fg="black", font=('Consolas', 14))
crm_name.grid(row=3, column=1, columnspan=2)

crm_note = Entry(input_frame, width=36, borderwidth=2, fg="black", font=('Consolas', 14))
crm_note.grid(row=4, column=1, columnspan=2, sticky=NW)

root.mainloop()
