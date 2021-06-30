from PIL import Image
import img2pdf

pattern = Image.open("A4_atlas_pattern.png")

page1 = Image.open("page1.png")

page1 = page1.resize((4586, 7007))
pattern.paste(page1, (630, 630))

pattern.mode = "RGB"

pattern.save("test.png")

with open("test.pdf", "wb") as file:
	file.write(img2pdf.convert("test.png"))