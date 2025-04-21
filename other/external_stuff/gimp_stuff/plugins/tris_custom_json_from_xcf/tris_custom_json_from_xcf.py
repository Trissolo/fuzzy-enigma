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

print("** Starting Json procedure **")

# constants:
class CONSTS:
    FILE_NAME = GLib.path_get_basename(__file__).removesuffix(".py")
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
        return ["tris-custom-json-from-xcf"]


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


    def procedure_is_complete(self, prcdr):
        #Gimp.PDBStatusType
        #       .EXECUTION_ERROR # == 0
        #       .CALLING_ERROR # == 1
        #       .PASS_THROUGH # Pass through == 2
        #       .SUCCESS # Success == 3
        #       .CANCEL # User cancel == 4
        print("** Json procedure complete! :D **")
        return prcdr.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())
    
    def elenca_figli(self, widget, lev = 1, idx = 0, lc = 1, hastrai = False, sp = "    ", hook = "╰╴", vpipe = "│"):
            if hasattr(widget, 'get_children'):
                gra = "└─" if (lc - idx) == 1 else "├─"
                indent = f"{sp * lev}" if not hastrai else f"{sp * (lev-1)}{vpipe}"
                print(f"{indent}{gra}{widget.get_name()}")
                chi = widget.get_children()
                lc = len(chi)
                for idx, elem in enumerate(chi):
                    self.elenca_figli(elem, lev + 1, idx, lc,((lc - idx) == 0), sp, hook, vpipe)
            else:
                print(f"{sp * (lev + 1)}└─{widget.get_name()}")
    

    def get_gamedata_from_json_file(self):
        my_path = GLib.build_pathv(GLib.DIR_SEPARATOR_S, [GLib.path_get_dirname(__file__), "gamedata.json"])   
        data = None
        with open(my_path) as json_file:
            data = json.load(json_file)

            # Test: Print the data of dictionary
            #print("\nTop level content:", data.keys())
            #print("\nGame Vars:", data['vars'].keys())
        return data
    
    def change_directory_as(self):
        GLib.chdir(GLib.path_get_dirname(__file__))
        GLib.chdir("../..")
        return GLib.get_current_dir()
    

    def update_layer(self):
        self.current_layer = self.image.get_selected_layers()[0]
        return self.current_layer
    

    @staticmethod
    def test_static_method(some_param = "some_param"):
        print(some_param)
        return some_param
    

    @staticmethod
    def btn_update_layer_onclick(button, self):
        print("Clicked:", button.get_name())
        print(self.layer_dict["stoca"])
        temp_layer = self.update_layer() #self.current_layer
        some_bool, ox, oy = temp_layer.get_offsets()
        ret_str = f"name: {temp_layer.get_name()}\nx: {ox}\ny: {oy}\nwidth: {temp_layer.get_width()}\nheight: {temp_layer.get_height()}"
        self.info_label.set_text(ret_str)
    
    
    def basic_setup(self, image):
        self.image = image
        self.current_layer = None   
        self.update_layer()
        self.common_data = self.get_gamedata_from_json_file()
        self.layer_dict = {"stoca": "zzo"}
    
    def build_main_dialog():
        dialog = GimpUi.Dialog.new()
        dialog.add_button("OK", Gtk.ResponseType.OK)


    def run(self, procedure, run_mode, image, drawables, config, run_data):
        # just for debug: not required for the plugin purpose 
        Gimp.message_set_handler(Gimp.MessageHandlerType.CONSOLE) # MESSAGE_BOX = 0, CONSOLE = 1, ERROR_CONSOLE = 2

        # quick bail
        if len(image.get_layers()) == 0 or image.get_xcf_file() is None:
            print("Quitting because there are no layers, or the image is not saved to disk...")
            return self.procedure_is_complete(procedure)
        
        #set current dir:
        print("Curr path dec:", self.change_directory_as())
        #import myutils
        #myutils.printing()
        from myutils import build_node as myu_build_node
        from myutils import elenca_figli as elenca_figli
        azz_node = myu_build_node("Riazz") #myutils.build_node("azz")
        azz_node.level = 3
        print(azz_node.name)
        #print("Wcche", myutils._Node)

        # a sort of "__init__" method:
        self.basic_setup(image)


        # Any plug-in that provides a user interface should call this function
        # (It’s a convention to use the name of the executable and _not_ the PDB procedure name)
        GimpUi.init(CONSTS.FILE_NAME)

        #draft for dialog!
        dialogazzo = dialogazzo = GimpUi.Dialog.new()
        dialogazzo.add_button("Done", Gtk.ResponseType.OK)
        

        new_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 2)
        new_box.set_name("menu container")

        btn_update_layer = GimpUi.Button.new()
        btn_update_layer.set_name("Button Update-Layer")
        btn_update_layer.set_label("Upd. Layer")
        btn_update_layer.connect('clicked', self.btn_update_layer_onclick, self)

        new_box.pack_start(btn_update_layer, False, False, 1)


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
        self.info_label = info_label
        '''
        info_label.set_use_markup(True)
        info_label.set_markup('<span foreground="#5687ff" size="x-large">skipCondition</span>: <i>[0, 4]</i>')
        info_label.set_markup('<span foreground="#464646"><tt>skipCondition</tt></span>: <span background="#569a58"><i>[0, 4]</i></span>')
        '''

        new_box.pack_start(info_frame, False, False, 1)


        main_container = dialogazzo.get_content_area()
        main_container.set_name("MAIN_CONTAINER (BOX)")
        main_container.pack_start(new_box, False, False, 1)

        elenca_figli(dialogazzo)

        print("SELF!!!", self, "\nTYPE:", type(self))
        dialogazzo.show_all()
        dialogazzo.run()


        # We have reached the end of the procedure: let's return "Success"
        return self.procedure_is_complete(procedure)  #procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(AdventureGameNook.__gtype__, sys.argv)

