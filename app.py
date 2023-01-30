#https://stackoverflow.com/questions/21566649/flask-button-run-python-without-refreshing-page

from flask import Flask, render_template, request
app = Flask(__name__)


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
    'p4': p4,
}

scores = {
    "p1" : 0,
    "p2" : 0,
    "p3" : 0,
    "p4" : 0,
}

@app.route('/')
def execute():
    return render_template('index.html', commands=AVAILABLE_COMMANDS, players=AVAILABLE_PLAYERS)

@app.route('/<cmd>')
def command(cmd=None):
    if cmd.find('-'):
        score_delta, player = cmd.split('-')
        if (score_delta == 'plus'):
            scores[player] += 1
        elif (score_delta == 'minus'):
            scores[player] -= 1
        else:
            pass 

    print(scores)
    response = scores
    return response, 200, {'Content-Type': 'text/plain'}