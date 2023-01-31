#Import required modules from Pillow package
from PIL import Image, ImageDraw, ImageFont

# get an image
base = Image.open('static/images/banner_template.png').convert('RGBA')
crown = Image.open('static/images/crown.png').convert('RGBA')
aku = Image.open('static/images/AkuAku.png').convert('RGBA')

factor = 0.15
crown = crown.resize((int(crown.width * factor), int(crown.height * factor)))
factor = 0.25
aku = aku.resize((int(aku.width * factor), int(aku.height * factor)))


canvas = base.copy()
canvas.paste(crown,(120 - 90, 40 - 25),mask=crown)

canvas.paste(aku,(450, 40 - 25),mask=aku)
#base.copy(crown)

# make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', base.size, (255,255,255,0))

# get a font
fnt = ImageFont.truetype('fonts/Rockwell-Font/rockb.ttf', 60)

# get a drawing context
d = ImageDraw.Draw(txt)

# draw text, half opacity
d.text((120 - 10, 40 - 20), "BENJA: 5", font=fnt, fill=(0,0,0,255))
d.text((650 - 10, 40 - 20), "OBREQUE: 3", font=fnt, fill=(0,0,0,255))
d.text((120 - 10, 150 - 20), "LUKAS: 2", font=fnt, fill=(0,0,0,255))
d.text((650 - 10, 150-  20), "NICO: 4", font=fnt, fill=(0,0,0,255))

# draw text, full opacity
#d.text((14,60), "Point", font=fnt, fill=(0,0,0,255))
out = Image.alpha_composite(canvas, txt)

#Show image
out.show()