
#from os import listdir
#complete_path= f"{sys.path[0]}/"
#qqqu = sys.path[0]

# wanted dir path, as string
#folder_path = f"{sys.path[0]}{GLib.DIR_SEPARATOR_S}splitted_gamedata{GLib.DIR_SEPARATOR_S}"

# list of filenames, as string
#dir_content = listdir(folder_path)
#print(*dir_content, sep="\n")
#print(complete_path)
def _grab_file_hardcoded():
    import sys
    import json
    base_dir = f"{sys.path[0]}/splitted_gamedata/"
    vars = []

    for varkind in ["bool_names", "crumble_names", "nibble_names", "byte_names"]:
        with open(f"{base_dir}{varkind}.json") as json_file:
            vars.append(json.load(json_file))
        
    hover_names = None
    with open(f"{base_dir}hover_names.json") as json_file:
        hover_names = json.load(json_file)
    
    return vars, hover_names

var_ary, hover_names_ary = _grab_file_hardcoded()

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