from flask import render_template, send_file, Response, redirect
from app import app
import pathlib
import json
import sys
import os
from os import listdir
from os.path import isfile, join
import subprocess
from subprocess import check_output
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


curDir = pathlib.Path(__file__).parent.absolute()
from environment import Environment
e = Environment()
ip = check_output(['hostname','-I']).decode("utf-8")

@app.route('/')
@app.route('/index')
def index():
    
    return  render_template('index.html', title='Smart Birdhouse', data=e, ip=ip)

@app.route('/videos')
def findvideofiles():
    onlyfiles = [f for f in listdir(str(curDir) + r'/videos') if isfile(join((str(curDir) + r'/videos'), f))]
    print(onlyfiles)
    return render_template('videos.html', files=onlyfiles)


@app.route('/videos/<path:filepath>')
def getvideodata(filepath):
    return send_file(str(curDir) + r'/videos/' + filepath)

@app.route('/audio')
def findaudiofiles():
    onlyfiles = [f for f in listdir(str(curDir) + r'/audio') if isfile(join((str(curDir) + r'/audio'), f))]
    print(onlyfiles)
    return render_template('audio.html', files=onlyfiles)


@app.route('/audio/<path:filepath>')
def getaudiodata(filepath):
    return send_file(str(curDir) + r'/audio/' + filepath)

@app.route('/stats')
def findstatfiles():
    onlyfiles = [f for f in listdir(str(curDir) + r'/stats') if isfile(join((str(curDir) + r'/stats'), f))]
    print(onlyfiles)
    return render_template('stats.html', files=onlyfiles)


@app.route('/stats/<path:filepath>')
def getstatdata(filepath):
    jsonFilePath = str(curDir) + r'/stats/' + str(filepath)
    with open(jsonFilePath) as jsonFile:
        jsonData = json.load(jsonFile)
    return render_template('statDisplay.html', data=jsonData['stats'])

@app.route('/download/<path:filepath>')
def downloadData(filepath):
    if str(filepath).find(".json"):
        dataFilePath = str(curDir) + r'/stats/' + str(filepath)
    elif str(filepath).find(".mp4"):
        dataFilePath = str(curDir) + r'/videos/' + str(filepath)
    elif str(filepath).find(".mp3"):
        dataFilePath = str(curDir) + r'/audio/' + str(filepath)

    return Response(dataFilePath, headers={"Content-disposition":"attachment; filename="+filepath})

@app.route('/clearDirectory')
def clrDir():
    rc = subprocess.call("app/clrDir.sh")
    return redirect('/')
    
