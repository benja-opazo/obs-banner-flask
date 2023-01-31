#https://stackoverflow.com/questions/21566649/flask-button-run-python-without-refreshing-page

from flask import Flask, render_template, request
import json
from PIL import Image, ImageDraw, ImageFont
app = Flask(__name__)


plus, minus = "plus", "minus"
AVAILABLE_COMMANDS = {
    '+1': plus,
    '-1': minus
}
p1, p2, p3, p4, p5, p6 = "Benja", "Obreque", "Lukas", "Nico", "Jorge", "Peters"
AVAILABLE_PLAYERS = {
    'p1': p1,
    'p2': p2,
    'p3': p3,
    'p4': p4,
    'p5': p5,
    'p6': p6,
}

scores = {
    "p1" : [0, AVAILABLE_PLAYERS['p1']],
    "p2" : [0, AVAILABLE_PLAYERS['p2']],
    "p3" : [0, AVAILABLE_PLAYERS['p3']],
    "p4" : [0, AVAILABLE_PLAYERS['p4']],
    "p5" : [0, AVAILABLE_PLAYERS['p5']],
    "p6" : [0, AVAILABLE_PLAYERS['p6']],
}

scores_json = dict()

@app.route('/', methods=['GET', 'POST'])
def execute():
    return render_template('index.html', commands=AVAILABLE_COMMANDS, players=AVAILABLE_PLAYERS, scores=scores)

@app.route('/<cmd>')
def command(cmd=None):
    if cmd.find('-') > 0:
        score_delta, player = cmd.split('-')
        if (score_delta == 'plus'):
            scores[player][0] += 1
        elif (score_delta == 'minus'):
            scores[player][0] -= 1
        else:
            pass
    else:
        if cmd == 'render_scores':
            # Serializing json
            json_object = json.dumps(scores, indent=4)
            # Writing to sample.json
            with open("score.json", "w") as outfile:
                outfile.write(json_object)
        if cmd == 'draw_banner':
            draw_banner(scores)
        if cmd == 'load_scores':
            with open("score.json", "r") as openfile:
                scores_json = json.load(openfile)
                #print(scores_json)
                for label in scores_json:
                    scores[label] = scores_json[label]
        if cmd =='reset_scores':
            for label in scores:
                scores[label][0] = 0

    #response = scores
    return render_template('index.html', commands=AVAILABLE_COMMANDS, players=AVAILABLE_PLAYERS, scores=scores)
    #return response, 200, {'Content-Type': 'text/plain'}


def draw_banner(scores):
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
    d.text((120 - 10, 40 - 20), scores['p1'][1].upper() + ": " + str(scores['p1'][0]), font=fnt, fill=(0,0,0,255))
    d.text((650 - 10, 40 - 20), scores['p2'][1].upper() + ": " + str(scores['p2'][0]), font=fnt, fill=(0,0,0,255))
    d.text((120 - 10, 150 - 20), scores['p3'][1].upper() + ": " + str(scores['p3'][0]), font=fnt, fill=(0,0,0,255))
    d.text((650 - 10, 150-  20), scores['p4'][1].upper() + ": " + str(scores['p4'][0]), font=fnt, fill=(0,0,0,255))

    # draw text, full opacity
    #d.text((14,60), "Point", font=fnt, fill=(0,0,0,255))
    out = Image.alpha_composite(canvas, txt)

    #Show image
    #out.show()
    out.save('static/images/banner_scores.png')
