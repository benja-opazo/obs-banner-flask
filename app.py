from flask import Flask, render_template, request
app = Flask(__name__)

scores = {
    "p1" : 0,
    "p2" : 0,
    "p3" : 0,
    "p4" : 0,
}

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('p1') == '+1':
            scores['p1'] += 1
        elif request.form.get('p1') == '-1':
            scores['p1'] -= 1
        elif  request.form.get('action2') == 'VALUE2':
            pass # do something else
        else:
            pass # unknown
        print(scores)
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")