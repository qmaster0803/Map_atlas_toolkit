from PIL import Image, ImageFont, ImageDraw
import img2pdf
import tkinter
import tkinter.ttk
import tkinter.filedialog
import os
import json
import lang_choose

lng_dict = {}

def create_title_page(text):
    img = Image.new("RGB", (1606, 2454), color="white")
    draw = ImageDraw.Draw(img)

    fontsize = 1
    font = ImageFont.truetype("LiberationSans-Regular.ttf", fontsize)
    while(draw.textsize(text, font)[0] < 1300 and draw.textsize(text, font)[1] < 2000):
        fontsize += 1
        font = ImageFont.truetype("LiberationSans-Regular.ttf", fontsize)

    textsize = draw.textsize(text, font)
    correct_y = int(fontsize/7)
    draw.text((int((1606-textsize[0])/2), int((2454-textsize[1])/2)-correct_y), text, align="center", font=font, fill="black")
    return img

def create_ending_page():
    img = Image.new("RGB", (1606, 2454), color="white")
    return img

def create_empty_page():
    img = Image.new("RGB", (1606, 2454), color="white")
    return img

def compose_page(page_left, page_right, output_path):
    pattern = Image.open("preloaded/A4_atlas_pattern.png")
    page_left = page_left.resize((1606, 2454))
    page_right = page_right.resize((1606, 2454))
    pattern.paste(page_left, (220, 220))
    pattern.paste(page_right, (2267, 220))
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

def find_pages(path):
    files = os.listdir(path)
    output = []
    for file in files:
        if(os.path.splitext(file)[1].lower() in [".png"] and os.path.splitext(file)[0].isnumeric()):
            output.append(file)
    return output

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
        tkinter.messagebox.showinfo(lng_dict["check_done"], lng_dict["directory_contains"].format(pages=len(find_pages(path))))

#for Ctrl+A in entries
def select_all(widget):
    widget.select_range(0, 'end')
    widget.icursor('end')

def process(window, path_entry, map_name_entry, frequencies_list_var, region_codes_var):
    if(not path_entry.get()): tkinter.messagebox.showerror(lng_dict["error"], lng_dict["nothing_to_process"]); return
    save_path = tkinter.filedialog.asksaveasfilename(filetypes=(("PDF document", "*.pdf"),))
    if(not save_path): tkinter.messagebox.showinfo("", lng_dict["aborted_by_user"]); return

    pages = find_pages(path_entry.get())
    for i, page in enumerate(pages):
        pages[i] = int(os.path.splitext(page)[0])
    pages.sort()
    pages.insert(0, "title")
    pages.append("ending")
    pages = calc_booklet(pages)
    os.makedirs("output", exist_ok=True)

    progress_window = tkinter.Toplevel(window, height=100, width=200)
    progress_label = tkinter.Label(progress_window, text=lng_dict["processing"])
    progressbar = tkinter.ttk.Progressbar(progress_window, orient=tkinter.HORIZONTAL, length=300, mode="determinate")

    progress_label.grid(row=0, column=0)
    progressbar.grid(row=1, column=0)
    progress_window.update()

    output_images = []
    done_count = 0
    for list_num, atlas_list in enumerate(pages):
        for i, page in enumerate(atlas_list):
            if(page == "title"):
                atlas_list[i] = create_title_page(map_name_entry.get())
            elif(page == "ending"):
                atlas_list[i] = create_ending_page()
            elif(page == "empty"):
                atlas_list[i] = create_empty_page()
            else:
                atlas_list[i] = Image.open(os.path.join(path_entry.get(), str(page)+'.png'))
            done_count += 1
            progressbar["value"] = done_count/(len(pages)*2)*100
            progress_window.update()
        output_images.append("output/"+str(list_num)+".png")
        compose_page(atlas_list[0], atlas_list[1], "output/"+str(list_num)+".png")

    progress_label["text"] = lng_dict["processing_pdf"]
    progress_window.update()
    with open(save_path, "wb") as pdf_file:
        pdf_file.write(img2pdf.convert(output_images))

    progress_window.destroy()
    tkinter.messagebox.showinfo("", lng_dict["done"])

if(__name__ == "__main__"):
    try:
        with open("settings.json") as file: settings = json.loads(file.read())
    except FileNotFoundError:
        lang_choose.ask_language()
        with open("settings.json") as file: settings = json.loads(file.read())
    with open("lng/"+settings["language"]+".json") as file: lng_dict = json.loads(file.read())

    window = tkinter.Tk()
    window.geometry("490x240")
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
    parts_separator3 = tkinter.ttk.Separator(window, orient="horizontal")

    start_button = tkinter.Button(window, text=lng_dict["start"], command=lambda: process(window, path_entry, map_name_entry, frequencies_list_var, region_codes_var))

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
    #attachments_frame start
    frequencies_list_chkbtn.grid(row=0, column=0)
    region_codes_chkbtn.grid(row=0, column=1)
    #attachments_frame end
    parts_separator3.grid(row=8, column=0, columnspan=3, sticky="EW", pady=(10, 10))
    start_button.grid(row=9, column=0, columnspan=3, sticky="EW")

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