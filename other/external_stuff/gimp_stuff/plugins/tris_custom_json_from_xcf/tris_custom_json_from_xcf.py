#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   GIMP - The GNU Image Manipulation Program
#   Copyright (C) 1995 Spencer Kimball and Peter Mattis
#
#   *** Based on: ***
#   https://testing.docs.gimp.org/3.0/en/gimp-using-python-plug-in-tutorial.html
#   gimp-tutorial-plug-in.py
#   sample plug-in to illustrate the Python plug-in writing tutorial
#   Copyright (C) 2023 Jacob Boerema
#
#   (ensure the script is executable)

# just for sys.argv
import sys

import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Glib is used mostly for GLib.Error()
# or utility functions like:
# GLib.build_pathv(GLib.DIR_SEPARATOR_S, [GLib.get_home_dir(), "my_file_name.txt"])
from gi.repository import GLib

# GObject is for GObject.ParamFlags:
# G_PARAM_READABLE: 1
# G_PARAM_WRITABLE: 2
# G_PARAM_READWRITE: 3 # -> Alias for: G_PARAM_READABLE | G_PARAM_WRITABLE
from gi.repository import GObject

# I/O and files, e.g., new_file = Gio.File.new_for_path("/home/USER/Graphics/my_picture.xcf")
#from gi.repository import Gio


# other custom imports
import json
#import os


# constants:
class CONSTS:
    FILE_NAME = GLib.path_get_basename(__file__).removesuffix(".py")


# our plugin class
class AdventureGameNook(Gimp.PlugIn):
    # procedure(s) name in Procedure Browser. Note that this string value CANNOT have underscores, only hyphens/dashes
    def do_query_procedures(self):
        return ["tris-custom-json-from-xcf"]


    def do_set_i18n(self, name):
        return False


    # The ImageProcedure (mostly hardcoded strings)
    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(
            self, name, Gimp.PDBProcType.PLUGIN, self.run, None
        )

        procedure.set_image_types("*")

        procedure.set_menu_label("[Tris] 🔩🌺 Room Editor and JSON generator")

        procedure.add_menu_path("<Image>/Filters/[[Tris]]/")

        procedure.set_documentation(
            "[Tris] Basically, a Room editor for adventure games.",
            "A complex plugin (GIMP 3.0). WIP",
            name,
        )

        procedure.set_attribution("Tris", "---", "2025")

        return procedure


    def procedure_is_complete(self, prcdr):
        #Gimp.PDBStatusType
        #       .EXECUTION_ERROR # == 0
        #       .CALLING_ERROR # == 1
        #       .PASS_THROUGH # Pass through == 2
        #       .SUCCESS # Success == 3
        #       .CANCEL # User cancel == 4
        print("** Json procedure complete! :D **")
        return prcdr.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())
    
    
    # load json
    def get_gamedata_from_json_file(self):
        my_path = GLib.build_pathv(GLib.DIR_SEPARATOR_S, [GLib.path_get_dirname(__file__), "gamedata.json"])   
        data = None
        with open(my_path) as json_file:
            data = json.load(json_file)

            # Test: Print the data of dictionary
            #print("\nTop level content:", data.keys())
            #print("\nGame Vars:", data['vars'].keys())
        return data
    
    def set_working_directory(self):
        GLib.chdir(GLib.path_get_dirname(__file__))
        GLib.chdir("../..")
        return GLib.get_current_dir()
    
    # Pseudo-TrisManager methods! Here!

    def update_layer(self):
        self.current_layer = self.image.get_selected_layers()[0]
        return self.current_layer
    
    def get_layer_parasite(self):
        parassites = self.current_layer.get_parasite_list()
        return parassites
    
    
    def add_to_manager(self, prop, wid):
        self.tris_widget[prop] = wid
        return self
    

    # All static methods are signal handlers
    @staticmethod
    def btn_update_layer_onclick(button, self):
        #print(self.layer_dict["stoca"])
        temp_layer = self.update_layer() #self.current_layer
        print("CAPTURED:", temp_layer.get_name())
        some_bool, ox, oy = temp_layer.get_offsets()
        ret_str = f"name: {temp_layer.get_name()}\nx: {ox}\ny: {oy}\nwidth: {temp_layer.get_width()}\nheight: {temp_layer.get_height()}"
        self.info_label.set_text(ret_str)
    
    # CRUCIAL SETUP
    def basic_setup(self, image, TrisEnum):
        self.image = image
        self.current_layer = None
        self.update_layer()
        self.shared_game_data = self.get_gamedata_from_json_file()
        print("🔻 Summary:")
        print('', "self.image", "self.current_layer", "self.update_layer()", sep='\n 🔸')
        print(" 🔸self.shared_game_data [Parsed 'gamedata.json' file]")
        print("", "self.bool_enum", "self.crumble_enum", "self.nibble_enum", "self.byte_enum", "self.onHoverNames_enum", sep='\n 🔸')
        # set properties for:
        #["BOOL", "CRUMBLE", "NIBBLE", "BYTE", "onHoverNames", "thingKind"]
        self.bool_enum = TrisEnum(self.BOOL, "The names of the gameBools")
        self.crumble_enum = TrisEnum(self.CRUMBLE, "The names of the gameCrumbles")
        self.nibble_enum = TrisEnum(self.NIBBLE, "The names of the gameNibbles")
        self.byte_enum = TrisEnum(self.BYTE, "The names of the gameBytes")
        self.onHoverNames_enum = TrisEnum(self.onHoverNames, "Things descriptions")

        future_thingKind = {}
        for elem in self.shared_game_data["thingKind"]: future_thingKind[elem["key"]] = elem["val"]
        self.thingKind = future_thingKind
        print("\n 🔸self.thingKind:")
        #for elem in self.thingKind: print(f"'{elem}'")
        for elem in self.shared_game_data["thingKind"]: print(f"{elem["key"]} ({elem["comment"]})" )

        # widget holder!
        self.tris_widget = {}
        print("\n 🔸self.tris_widget")
        print(" 🔸PROPS:\"self.shared_game_data['thingProps']", *self.shared_game_data['thingProps'], sep='"\n"', end='"' )
        print("\n\n🔺EOSummary\n")

    
    @property
    def BOOL(self):
        return self.shared_game_data["BOOL"]
    
    @property
    def CRUMBLE(self):
        return self.shared_game_data["CRUMBLE"]
    
    @property
    def NIBBLE(self):
        return self.shared_game_data["NIBBLE"]
    
    @property
    def BYTE(self):
        return self.shared_game_data["BYTE"]
    
    @property
    def onHoverNames(self):
        return self.shared_game_data["onHoverNames"]
        


    
    def build_main_dialog():
        dialog = GimpUi.Dialog.new()
        dialog.add_button("OK", Gtk.ResponseType.OK)


    def run(self, procedure, run_mode, image, drawables, config, run_data):
        print("** Starting Json procedure **")
        # just for debug: not required for the plugin purpose 
        Gimp.message_set_handler(Gimp.MessageHandlerType.CONSOLE) # MESSAGE_BOX = 0, CONSOLE = 1, ERROR_CONSOLE = 2

        # quick bail
        if len(image.get_layers()) == 0 or image.get_xcf_file() is None:
            print("Quitting because there are no layers, or the image is not saved to disk...")
            return self.procedure_is_complete(procedure)
        
        #set current dir:
        #print("Curr path dec:", self.set_working_directory())
        
        # an unnecessary utility
        #from myutils import elenca_figli

        # mandatory things:
        from myutils import TrisEnum

        from myutils import TrisFrame

        # Set 'trisParent' in any custom class that needs to reference the 'current_layer'!
        #TrisFrame.set_trisParent(self)


        # a sort of "__init__" method:
        self.basic_setup(image, TrisEnum)

        # initialize Gtk!
        GimpUi.init(CONSTS.FILE_NAME)

        #draft for dialog!
        dialogazzo = dialogazzo = GimpUi.Dialog.new()
        dialogazzo.add_button("Done", Gtk.ResponseType.OK)
        

        new_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 2)
        new_box.set_name("menu container")

        btn_update_layer = Gtk.Button.new_with_mnemonic("_Update current Layer!")#GimpUi.Button.new()
        btn_update_layer.set_name("Button Update-Layer")
        #btn_update_layer.set_label("Capture Layer!")
        btn_update_layer.connect('clicked', self.btn_update_layer_onclick, self)

        new_box.pack_end(btn_update_layer, False, False, 1)


        info_frame = GimpUi.Frame.new("Questa è la label del Frame")
        info_frame.set_name("Layer-info Frame")

        tempval = 6
        info_frame.set_margin_start(tempval)
        info_frame.set_margin_end(tempval)

        info_frame.set_margin_top(tempval)
        info_frame.set_margin_bottom(tempval)

        #sub label
        info_label = info_frame.get_label_widget()
        info_label.set_name("Layer-info Frame")

        #ascaxxo
        # a reachable reference for this Label, because the contained text is updated over time:
        #self.info_label = info_label
        '''
        info_label.set_use_markup(True)
        info_label.set_markup('<span foreground="#5687ff" size="x-large">skipCondition</span>: <i>[0, 4]</i>')
        info_label.set_markup('<span foreground="#464646"><tt>skipCondition</tt></span>: <span background="#569a58"><i>[0, 4]</i></span>')
        '''

        new_box.pack_start(info_frame, False, False, 1)


        main_container = dialogazzo.get_content_area()
        main_container.set_name("MAIN_CONTAINER (BOX)")
        main_container.pack_start(new_box, False, False, 1)

        test = TrisFrame("Hovered_name", self)
        test.write_prop()
        test.add_paned_test()
        main_container.pack_start(test, False, False, 1)


        print("TrisWidget", self.tris_widget)
        print("Test Random Enum:", self.onHoverNames_enum.get_list())

        #dialogazzo.show_all()
        #dialogazzo.run()

        print("Checking:")
        for elem in [self.bool_enum, self.crumble_enum, self.nibble_enum, self.byte_enum, self.onHoverNames_enum]:
            print(elem)



        # We have reached the end of the procedure: let's return "Success"
        return self.procedure_is_complete(procedure)  #procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(AdventureGameNook.__gtype__, sys.argv)

