#https://stackoverflow.com/questions/21566649/flask-button-run-python-without-refreshing-page

from flask import Flask, render_template, request, jsonify
import json
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from yt_dlp import YoutubeDL
import os
#from wand.image import Image
from wand.image import Image as wand
from fileinput import filename
import filetype
from ffmpeg import FFmpeg

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "static/output/"


plus, minus = "plus", "minus"
AVAILABLE_COMMANDS = {
    '+1': plus,
    '-1': minus
}
p1, p2, p3, p4 = "Benja", "Obreque", "Lukas", "Nico"
AVAILABLE_PLAYERS = {
    'p1': p1,
    'p2': p2,
    'p3': p3,
    'p4': p4
}

scores = {
    "p1" : [0, AVAILABLE_PLAYERS['p1']],
    "p2" : [0, AVAILABLE_PLAYERS['p2']],
    "p3" : [0, AVAILABLE_PLAYERS['p3']],
    "p4" : [0, AVAILABLE_PLAYERS['p4']],
}

# Dice el estado de la descarga de video. -1 no ha descargado nada, 0 error, 1 exito, 2 descargando
videostatus = -1

scores_json = dict()

@app.route('/', methods=['GET', 'POST'])
def execute():
    return render_template('index.html', currentpage="inicio")

@app.route('/ctrscores/', methods=['GET', 'POST'])
def execute_ctrscores():
    return render_template('ctrscores.html', currentpage="ctrscores", commands=AVAILABLE_COMMANDS, players=AVAILABLE_PLAYERS, scores=scores)

@app.route('/media/', methods=['GET', 'POST'])
def execute_videos():
    return render_template('media.html', currentpage="media", videostatus=videostatus)

@app.route('/media/<cmd>', methods=['GET', 'POST'])
def videos_command(cmd=None):
    global videostatus
    if cmd =="submit_video":
        URLS = [request.get_json()]
        if os.path.isfile('static/output/video.mp4'):
            os.remove('static/output/video.mp4')
        #URLS = ['https://www.youtube.com/watch?v=dQw4w9WgXcQ']
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': 'static/output/video.mp4'
        }
        with YoutubeDL(ydl_opts) as ydl:
            try:
                videostatus = 2
                ydl.download(URLS)
                videostatus = 1
            except:
                videostatus = 0
        return jsonify(videostatus = videostatus)
    elif cmd=="delete_video":
        if os.path.isfile('static/output/video.mp4'):
            os.remove('static/output/video.mp4')
        videostatus = -1
    elif cmd=="submit_file":
            uploaded_file = request.files.get("file")
            file_path = os.path.join("tmp/", uploaded_file.filename)

            if uploaded_file != None:
                uploaded_file.save(file_path)
                # Convert to jpeg
                if filetype.is_image(file_path):
                    with wand.Image(filename = file_path) as img:
                        img.convert("jpg")
                        img.save(filename="static/output/uploaded_img.jpg")
                # Convert to mp4
                if filetype.is_video(file_path):
                        ffmpeg = (
                        FFmpeg()
                        .option("y")
                        .input(file_path)
                        .output(
                            "static/output/uploaded_video.mp4",
                            {"codec:v": "libx264"},
                        )
                        )

                        ffmpeg.execute()
                
    elif cmd=="delete_file":
        if os.path.isfile('static/output/uploaded_video.mp4'):
                    os.remove('static/output/uploaded_video.mp4')
        if os.path.isfile('static/output/uploaded_img.jpg'):
            os.remove('static/output/uploaded_img.jpg')
            
    elif cmd=="update_buttons":
        if videostatus == 1 or videostatus == -1:
            return jsonify(icon="done", theclass="green", videostatus = videostatus)
        elif videostatus == 2:
            return jsonify(icon="sync", theclass="blue", videostatus = videostatus)
        elif videostatus == 0:
            return jsonify(icon="error", theclass="red")
        else:
            return jsonify(icon="error", theclass="red", videostatus = videostatus)
    return render_template('media.html', currentpage="media", videostatus=videostatus)

@app.route('/ctrscores/<cmd>')
def ctrscores_command(cmd=None):
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
                for label in scores_json:
                    scores[label] = scores_json[label]
        if cmd =='reset_scores':
            for label in scores:
                scores[label][0] = 0
            draw_banner(scores)

        if cmd =='update_scores':
            return jsonify(scores=scores)
    return render_template('ctrscores.html', commands=AVAILABLE_COMMANDS, players=AVAILABLE_PLAYERS, scores=scores)


def draw_banner(scores):
    # Gets images
    base = Image.open('static/images/banner_template.png').convert('RGBA')
    crown = Image.open('static/images/crown.png').convert('RGBA')
    aku = Image.open('static/images/AkuAku.png').convert('RGBA')

    # get a font
    fnt = ImageFont.truetype('fonts/Rockwell-Font/rockb.ttf', 60)

    # Scale Factors
    crown_factor = 0.15
    aku_factor = 0.23


    player_positions = {'p1': [120,40],
                        'p2': [650,40],
                        'p3': [120,150],
                        'p4': [650,150]}
    text_offsets = [10,20]
    crown_offsets = [90,25]

    # Resize images
    crown = crown.resize((int(crown.width * crown_factor), int(crown.height * crown_factor)))
    aku = aku.resize((int(aku.width * aku_factor), int(aku.height * aku_factor)))

    # Base and Aku
    canvas = base.copy()
    canvas.paste(aku,(420, 15),mask=aku)

    # get a drawing context
    d = ImageDraw.Draw(canvas)

    # Draw Scores gets the score_max (assumes >= 0)
    score_max = [-1,[]]
    for player in scores:
        if scores[player][0] > score_max[0] and scores[player][0] > 0:
            score_max[0] = scores[player][0]
            score_max[1] = [player]
        elif scores[player][0] == score_max[0] and scores[player][0] > 0:
            score_max[0] = scores[player][0]
            score_max[1].append(player)
        
        text_positions = np.array(player_positions[player]) - np.array(text_offsets)
        d.text((text_positions), scores[player][1].upper() + ": " + str(scores[player][0]), font=fnt, fill=(0,0,0,255))

    # draw the crown
    if (score_max[0] > 0):
        for player in score_max[1]:
            crown_position = list(np.array(player_positions[player]) - np.array(crown_offsets))
            canvas.paste(crown,crown_position,mask=crown)

    canvas.save('static/output/banner_scores.png')
