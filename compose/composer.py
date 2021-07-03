from PIL import Image
import img2pdf
import tkinter
import tkinter.ttk
import tkinter.filedialog
import os
import json
import lang_choose

lng_dict = {}

def compose_page(page_left, page_right, output_path):
    pattern = Image.open("A4_atlas_pattern.png")
    page1 = page1.resize((1606, 2454))
    page2 = page2.resize((1606, 2454))
    pattern.paste(page1, (220, 220))
    pattern.paste(page2, (2267, 220))
    pattern.mode = "RGB"
    pattern.save(output_path)

def calc_booklet(pages):
    inverted_list = True
    output_list = []

    #additional empty pages
    if(len(pages)%2 != 0): pages.insert(-1, 'empty')
    if(len(pages)%4):
        pages.insert(-1, 'empty')
        pages.insert(-1, 'empty')
    
    for page_num in range(int(len(pages)/2)):
        if(inverted_list): current_list = [pages[(page_num+1)*-1], pages[page_num]]
        else: current_list = [pages[page_num], pages[(page_num+1)*-1]]
        inverted_list = not inverted_list
        output_list.append(current_list)
    return output_list

def select_path():
    new_path = tkinter.filedialog.askdirectory()
    if(new_path):
        path_entry.delete(0, 'end')
        path_entry.insert(0, new_path)

def check_path():
    path = path_entry.get()
    if(not path):
        tkinter.messagebox.showerror(lng_dict["error"], lng_dict["nothing_to_check"])
    else:
        files = os.listdir(path)
        counter = 0
        for file in files:
            if(os.path.splitext(file)[1].lower() in [".png"] and os.path.splitext(file)[0].isnumeric()):
                counter += 1
        tkinter.messagebox.showinfo(lng_dict["check_done"], lng_dict["directory_contains"].format(pages=counter))

#for Ctrl+A in entries
def select_all(widget):
    widget.select_range(0, 'end')
    widget.icursor('end')

#def process():

if(__name__ == "__main__"):
    try:
        with open("settings.json") as file: settings = json.loads(file.read())
    except FileNotFoundError:
        lang_choose.ask_language()
        with open("settings.json") as file: settings = json.loads(file.read())
    with open("lng/"+settings["language"]+".json") as file: lng_dict = json.loads(file.read())

    window = tkinter.Tk()
    window.geometry("490x190")
    path_label = tkinter.Label(window, text=lng_dict["path_to_pages"])
    path_entry = tkinter.Entry(window, width=40)
    path_button = tkinter.Button(window, text=lng_dict["select"], command=select_path)
    path_check_button = tkinter.Button(window, text=lng_dict["check"], command=check_path)
    parts_separator1 = tkinter.ttk.Separator(window, orient="horizontal")

    map_name_label = tkinter.Label(window, text=lng_dict["map_name"])
    map_name_entry = tkinter.Entry(window, width=60)
    parts_separator2 = tkinter.ttk.Separator(window, orient="horizontal")

    frequencies_list_var = tkinter.BooleanVar(); frequencies_list_var.set(0)
    region_codes_var = tkinter.BooleanVar(); region_codes_var.set(0)

    attachments_label = tkinter.Label(text=lng_dict["attachments"])
    attachments_frame = tkinter.Frame(window)
    frequencies_list_chkbtn = tkinter.Checkbutton(attachments_frame, text=lng_dict["attachment_HAM_radio"], variable=frequencies_list_var, onvalue=True, offvalue=False)
    region_codes_chkbtn = tkinter.Checkbutton(attachments_frame, text=lng_dict["attachment_region_codes"], variable=region_codes_var, onvalue=True, offvalue=False)

    path_label.grid(row=0, column=0, columnspan=2)
    path_entry.grid(row=1, column=0)
    path_button.grid(row=1, column=1, sticky="EW")
    path_check_button.grid(row=1, column=2, sticky="EW")
    parts_separator1.grid(row=2, column=0, columnspan=3, sticky="EW", pady=(10, 10))
    map_name_label.grid(row=3, column=0, columnspan=3)
    map_name_entry.grid(row=4, column=0, columnspan=3)
    parts_separator2.grid(row=5, column=0, columnspan=3, sticky="EW", pady=(10, 10))
    attachments_label.grid(row=6, column=0, columnspan=3)
    attachments_frame.grid(row=7, column=0, columnspan=3)

    frequencies_list_chkbtn.grid(row=0, column=0)
    region_codes_chkbtn.grid(row=0, column=1)

    path_entry.bind("<Control-KeyRelease-a>", lambda event: select_all(event.widget))
    map_name_entry.bind("<Control-KeyRelease-a>", lambda event: select_all(event.widget))

    window.mainloop()

#pages = ['title', 'page1', 'page2', 'page3', 'page4', 'page5', 'ending']
#print(calc_booklet(pages))
#page1 = Image.open("page1.png")
#page2 = Image.open("page1.png")
#print("Composing...")
#compose_page(page1, page2, "test.png")

#with open("test.pdf", "wb") as file:
#    file.write(img2pdf.convert("test.png"))