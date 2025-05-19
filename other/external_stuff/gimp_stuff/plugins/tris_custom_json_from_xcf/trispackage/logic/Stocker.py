import sys
import json
#from os import listdir
#complete_path= f"{sys.path[0]}/"
#qqqu = sys.path[0]

# wanted dir path, as string
#folder_path = f"{sys.path[0]}{GLib.DIR_SEPARATOR_S}splitted_gamedata{GLib.DIR_SEPARATOR_S}"

# list of filenames, as string
#dir_content = listdir(folder_path)
#print(*dir_content, sep="\n")
#print(complete_path)

bools = None
wanted_file = "bool_names.json"
with open(f"{sys.path[0]}/splitted_gamedata/{wanted_file}") as json_file:
    bools = json.load(json_file)
'''
class Stocker():
    data_ary = []
    summary_ary = []
    tool_ary = []
    
    @classmethod
    def build_and_fill(cls):
        gr =  ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
        ita = [*"ABCDE"]
        nums = range(5)
'''