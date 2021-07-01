from PIL import Image
import img2pdf

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

pages = ['title', 'page1', 'page2', 'page3', 'ending']
print(calc_booklet(pages))
#page1 = Image.open("page1.png")
#page2 = Image.open("page1.png")
#print("Composing...")
#compose_page(page1, page2, "test.png")

#with open("test.pdf", "wb") as file:
#    file.write(img2pdf.convert("test.png"))