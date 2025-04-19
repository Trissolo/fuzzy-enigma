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

# just fou sys.argv
import sys

import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

# Glib is used mostly for GLib.Error()
# or utility functions like:
# GLib.build_pathv(GLib.DIR_SEPARATOR_S, [GLib.get_home_dir(), "my_file_name.txt"])
from gi.repository import GLib

# GObject is for GObject.ParamFlags:
# G_PARAM_READABLE: 1
# G_PARAM_WRITABLE: 2
# G_PARAM_READWRITE: 3 # -> Alias for: G_PARAM_READABLE | G_PARAM_WRITABLE
from gi.repository import GObject

# I/O and files
from gi.repository import Gio



# other custom imports
import json
#import os

#print("---------")

# constants:
class CONSTS:
    FILE_NAME = GLib.path_get_basename(__file__).removesuffix(".py") # "tris_base_simple" # GLib.path_get_basename(__file__).removesuffix(".py")
    TEXT = "QWE"
    OTHER = "FOO_NEW!"
    ARGU_TEST_BOOL = "tris_test_bool"
    ARGU_TEXT = "tris_user_text"
    ARGU_INTEGER = "tris_user_integer"
    ARGU_FOLDER = "tris_user_folder"



""" # Helper class
class Tris_Helper:
    message = ""
    prefix = "\n"
    #def_mes_han = Gimp.message_get_handler()

    @classmethod
    def reset_message(cls):
        cls.message = ""
        return cls

    @classmethod
    def add_message(cls, chunk="", prepend_prefix=True):
        cls.message += f"{cls.prefix}{chunk}" if prepend_prefix else chunk
        return cls

    @classmethod
    def show_message(cls):
        Gimp.message(cls.message)
        return cls """


# our plugin class
class AdventureGameNook(Gimp.PlugIn):
    # container = {}

    # procedure(s) name in Procedure Browser. Note that this string value CANNOT have underscores, only hyphens/dashes
    def do_query_procedures(self):
        return ["tris-custom-json-from-xcf"] #CONSTS.ID_IN_PLUGIN_BROWSER]


    def do_set_i18n(self, name):
        return False


    #def do_quit(self):
    #    #This method is internally bugged :(
    #    print("Buggggged")
    #    return True


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

        """
        procedure.add_string_argument(
            CONSTS.ARGU_TEXT,
            "Text",
            None,
            "Hello World!...",
            GObject.ParamFlags.READWRITE,
        )

        procedure.add_boolean_argument(
            CONSTS.ARGU_TEST_BOOL,
            "Generic BOOLean",
            "This option is a BOOL (default: false)",
            False,
            GObject.ParamFlags.READWRITE,
        )

        procedure.add_int_argument ( # GimpProcedure* procedure,
            CONSTS.ARGU_INTEGER, # const gchar* name,
            "An integer number:", # const gchar* nick,
            "(The room number)", # const gchar* blurb,
            0, # gint min,
            255, # gint max,
            0, # gint value,
            GObject.ParamFlags.READWRITE # GParamFlags flags
        )
        
        procedure.add_file_argument(
            # GimpProcedure* procedure,
            CONSTS.ARGU_FOLDER,  # const gchar* name,
            "Destination folder for .png",  # const gchar* nick,
            None,  # const gchar* blurb,
            Gimp.FileChooserAction.SELECT_FOLDER,  # GimpFileChooserAction action,
            True,  # gboolean none_ok,
            None,  # GFile* default_file,
            GObject.ParamFlags.READWRITE,  # GParamFlags flags
        )
        """
        return procedure


    def procedure_is_complete(self, prcd):
        #Gimp.PDBStatusType
        #       .EXECUTION_ERROR # == 0
        #       .CALLING_ERROR # == 1
        #       .PASS_THROUGH # Pass through == 2
        #       .SUCCESS # Success == 3
        #       .CANCEL # User cancel == 4
        print("** Json procedure complete! :D **")
        return prcd.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())
    

    def get_gamedata_from_json_file(self):
        crazy_thing = __file__.removesuffix(GLib.path_get_basename(__file__))
        data = None
        with open(f'{crazy_thing}gamedata.json') as json_file:
            data = json.load(json_file)

            # Print the type of data variable
            print("Type:", type(data))

            # Print the data of dictionary
            print("\nbools:", data['bools'])
            print("\ntype:", data['bools'])
            print("\n element:", data['bools'][2])
        return data
    

    def update_layer(self):
        self.current_layer = self.image.get_selected_layers()[0]
        return self.current_layer


    def run(self, procedure, run_mode, image, drawables, config, run_data):
        #print(f"Args:, \nprocedure: {procedure},\nrun_mode: {run_mode},\nimage: {image},\ndrawables: {drawables},\nconfig: {config},\nrun_data: {run_data}")
        # just for debug: not required for the plugin purpose 
        Gimp.message_set_handler(Gimp.MessageHandlerType.CONSOLE) # MESSAGE_BOX = 0, CONSOLE = 1, ERROR_CONSOLE = 2

        # quick bail
        if len(image.get_layers()) == 0 or image.get_xcf_file() is None:
            print("Quitting because there are no layers, or the image is not saved to disk...")
            return self.procedure_is_complete(procedure)
        
        self.image = image

        self.current_layer = None
        
        self.update_layer()

        print(f"Filename: {image.get_xcf_file().get_basename().removesuffix('.xcf')}")

        tempgamedata = self.get_gamedata_from_json_file()

        print("TGD", tempgamedata['OnHoverNames'])

        #print("No JSON yet")
        
        #import json

        # Opening JSON file
        """ with open('gamedata.json') as json_file:
            data = json.load(json_file)

            # Print the type of data variable
            print("Type:", type(data))

            # Print the data of dictionary
            print("\nbools:", data['bools'])
            print("\ntype:", data['bools'])
            print("\n element:", data['bools'][2]) """


        



        # Any plug-in that provides a user interface should call this function
        # (It’s a convention to use the name of the executable and _not_ the PDB procedure name)
        GimpUi.init(CONSTS.FILE_NAME)




        # At this point, all is ok: return Success
        return self.procedure_is_complete(procedure)  #procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(AdventureGameNook.__gtype__, sys.argv)

