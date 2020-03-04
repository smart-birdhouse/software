from environment import Environment
import json

e = Environment()

class jsonParser:
    def __init__(self):
        self.JSONfilename = ""

    def createJSON(self, timespec):

        #TODO:String parsing for timestamp format
        self.JSONfilename = "bla"
        stats = {"stats":[{"temperature":e.temperature, "humidity":e.humidity, "pressure":e.pressure, "altitude":e.altitude, "timestamp":timespec}]}
        
        with open(self.JSONfilename+".json", 'w') as f:
            json.dump(stats, f, indent=4)

    def updateJSON(self, timespec):
        data = json.load(self.JSONfilename+".json")
        temp = data['stats']

        stats = {"stats":[{"temperature":e.temperature, "humidity":e.humidity, "pressure":e.pressure, "altitude":e.altitude, "timestamp":timespec}]}
        temp.append(stats)
        with open(self.JSONfilename+".JSON".'w') as f:
            json.dump(stats, f, indent=4)
