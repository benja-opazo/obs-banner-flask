#Import required modules from Pillow package
from PIL import Image, ImageDraw, ImageFont

# get an image
base = Image.open('banner_template.png').convert('RGBA')

# make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', base.size, (255,255,255,0))

# get a font
fnt = ImageFont.truetype('fonts/Rockwell-Font/rockb.ttf', 40)

# get a drawing context
d = ImageDraw.Draw(txt)

# draw text, half opacity
d.text((14,14), "Tutorials", font=fnt, fill=(0,0,0,255))

# draw text, full opacity
d.text((14,60), "Point", font=fnt, fill=(0,0,0,255))
out = Image.alpha_composite(base, txt)

#Show image
out.show()