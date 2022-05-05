import json
def read_file(filename):
    with open(filename, "r") as f:
        return f.read() 
        
def read_json(filename):
    with open(filename, "r") as f:
        return json.load(f)
