import json
class Environment:
    def __init__(self,path):
        with open(path) as f:
            self.packages=json.load(f)
    def get_packages(self):
        return self.packages
