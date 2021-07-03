import json
import tkinter 

with open("lng/list.json") as file: lng_list = json.loads(file.read())

def select_lng(lng_selector_var, lng_window):
    try:
        with open("settings.json") as file: settings = json.loads(file.read())
    except FileNotFoundError: settings = {}
    settings["language"] = lng_list[lng_selector_var.get()]
    with open("settings.json", "w") as file: file.write(json.dumps(settings))
    lng_window.destroy()

def ask_language_changed(value, lng_label, lng_window):
    with open("lng/"+lng_list[value]+".json") as file: text = json.loads(file.read())["choose_language"]
    lng_label["text"] = text
    lng_window.title(text)

def ask_language():
    lng_names = [i for i in lng_list.keys()]

    lng_window = tkinter.Tk()
    lng_label = tkinter.Label(lng_window, text="Choose language:")
    lng_selector_var = tkinter.StringVar(lng_window); lng_selector_var.set("English")
    lng_selector = tkinter.OptionMenu(lng_window, lng_selector_var, *lng_names, command=lambda value: ask_language_changed(value, lng_label, lng_window))
    lng_ok_button = tkinter.Button(lng_window, text="Ok", command=lambda: select_lng(lng_selector_var, lng_window))

    lng_label.pack()
    lng_selector.pack()
    lng_ok_button.pack()
    lng_window.protocol("WM_DELETE_WINDOW", lambda: 0)
    lng_window.geometry("250x100")
    lng_window.title("Choose language")
    lng_window.mainloop()