from flask import render_template
from flask import send_file
from app import app
import pathlib
import json
from os import listdir
from os.path import isfile, join

curDir = pathlib.Path(__file__).parent.absolute()


@app.route('/')
@app.route('/index')
def index():
    with open(str(curDir) + r'\main.json') as json_file:
        data = json.load(json_file)
        print(data['stats'])
    return  render_template('index.html', title='Smart Birdhouse', data=data['stats'])

@app.route('/videos')
def findvideofiles():
    onlyfiles = [f for f in listdir(str(curDir) + r'\videos') if isfile(join((str(curDir) + r'\videos'), f))]
    print(onlyfiles)
    return render_template('videos.html', files=onlyfiles)


@app.route('/videos/<path:filepath>')
def getvideodata(filepath):
    return send_file(str(curDir) + r'\videos\\' + filepath)

@app.route('/audio')
def findaudiofiles():
    onlyfiles = [f for f in listdir(str(curDir) + r'\audio') if isfile(join((str(curDir) + r'\audio'), f))]
    print(onlyfiles)
    return render_template('audio.html', files=onlyfiles)


@app.route('/audio/<path:filepath>')
def getaudiodata(filepath):
    return send_file(str(curDir) + r'\audio\\' + filepath)

@app.route('/stats')
def findstatfiles():
    onlyfiles = [f for f in listdir(str(curDir) + r'\stats') if isfile(join((str(curDir) + r'\stats'), f))]
    print(onlyfiles)
    return render_template('stats.html', files=onlyfiles)


@app.route('/stats/<path:filepath>')
def getstatdata(filepath):
    jsonFilePath = str(curDir) + r'\stats\\' + str(filepath)
    with open(jsonFilePath) as jsonFile:
        jsonData = json.load(jsonFile)
    return render_template('statDisplay.html', data=jsonData['stats'])