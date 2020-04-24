from environment import Environment
import json
import pathlib

e = Environment()

class jsonParser:
    def __init__(self):
        self.JSONfilename = ""
        self.path=str(pathlib.Path(__file__).parent.absolute())+"/app/stats/"
    def createJSON(self, timespec):

        #TODO:String parsing for timestamp format
        self.JSONfilename = timespec
        stats = {"stats":[{timespec:{"temperature":e.temperature, "humidity":e.humidity, "pressure":e.pressure, "altitude":e.altitude}}]}
        
        with open(self.path + self.JSONfilename+".json", 'w') as f:
            json.dump(stats, f, indent=4)

    def updateJSON(self, timespec):
        with open(self.path+self.JSONfilename+".json") as f:
            data = json.load(f)
        temp = data['stats']
        stats = {timespec:{"temperature":e.temperature, "humidity":e.humidity, "pressure":e.pressure, "altitude":e.altitude}}
        temp.append(stats)
        data['stats'] = temp
        with open(self.path+self.JSONfilename+".json",'w') as f:
            json.dump(data, f, indent=4)
