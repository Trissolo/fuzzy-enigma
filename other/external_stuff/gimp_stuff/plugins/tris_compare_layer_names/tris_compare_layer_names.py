#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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

# 
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Just for colors:
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk




# other custom imports
#import json
#import os

#print("---------")

# constants:
class CONSTS:
    # Note that this string value CANNOT have underscores, only hyphens/dashes
    FILE_NAME = "tris_compare_layer_names" #GLib.path_get_basename(__file__).removesuffix(".py") # "tris_base_simple" # GLib.path_get_basename(__file__).removesuffix(".py")
    
    ID_IN_PLUGIN_BROWSER = "tris-compare-layer-names"
    TEXT = "QWE"
    OTHER = "FOO_NEW!"
    ARGU_TEST_BOOL = "tris_test_bool"
    ARGU_TEXT = "tris_user_text"
    ARGU_INTEGER = "tris_user_integer"
    ARGU_FOLDER = "tris_user_folder"



# Helper class
class Tris_Helper:
    message = ""
    prefix = "\n"
    #def_mes_han = Gimp.message_get_handler()

    @staticmethod
    def build_widget(parent, label = None):
        w = GimpUi.Dialog.new()
        return w
    
    @staticmethod
    def add_widget_to_box(wdg, parent): #, name = None):
        parent.pack_start(wdg, False, False, 1)
        wdg.show()
        return wdg
    
    staticmethod
    def build_box():
        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 2)
        box.show()
        return box

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
        return cls


# our plugin class
class TrisPluginCompareLayerNames(Gimp.PlugIn):
    # container = {}

    # procedure(s) name in Procedure Browser. Note that this string value CANNOT have underscores, only hyphens/dashes
    def do_query_procedures(self):
        return [CONSTS.ID_IN_PLUGIN_BROWSER]


    def do_set_i18n(self, name):
        return False


    #def do_quit(self):
    #    #This method is internally bugged :(
    #    print("Buggged")
    #    return True


    # The ImageProcedure (mostly hardcoded strings)
    def do_create_procedure(self, name):
        print(f"+++ Passed name from 'query_procedures': '{name}' +++")
        
        procedure = Gimp.ImageProcedure.new(
            self, name, Gimp.PDBProcType.PLUGIN, self.run, None #Tris_Helper
        )

        procedure.set_image_types("*")

        procedure.set_menu_label("[Tris] Compare layer names")

        procedure.add_menu_path("<Image>/Filters/[[Tris]]/")

        procedure.set_documentation(
            "[Tris] Basic Plugin. Check the uniqueness of the layer names in multiple files.",
            "For GIMP 3.0",
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


    def end_of_the_procedure(self, procedure):
        #self.def_mes_han = Gimp.message_get_handler()
        Gimp.message_set_handler(Gimp.MessageHandlerType.CONSOLE) # MESSAGE_BOX = 0, CONSOLE = 1, ERROR_CONSOLE = 2
        print("Handler reset. Success!\nDone!")
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())
    
    def generate_layer_names_set(self, image, sep = "_"):
        names_set = set()
        for layer in image.get_layers():
            name = layer.get_name()
            names_set.add(name if name.count(sep) == 0 else name.split(sep)[0])
        return names_set
    
    def compare_set(self, cmp_image, actual_image):
        print(f"Comparing {cmp_image.get_name()} with {actual_image.get_name()}")
        cur_set = self.generate_layer_names_set(actual_image)
        other_set = self.generate_layer_names_set(cmp_image)
        
        resu_set = cur_set.intersection(other_set)
        len_resu = len(resu_set)
        return resu_set, len_resu
    
    def to_new_dialog(self, child, cust = False):
        #child = GimpUi.ImageComboBox.new(lambda current_img, unwanted_img = image: current_img is not unwanted_img)

        dialog_azzo = GimpUi.Dialog.new()
        dialog_azzo.add_button("_Select and compare" if cust else "Ok", Gtk.ResponseType.OK)
        #dialog_azzo.add_buttons("gimp-tool-heal", 42, "Close", Gtk.ResponseType.CLOSE)
        dialog_azzo.get_content_area().add(child)
        child.show()
        #print(f"DebuG: child get_destroy_with_parent: {child.get_destroy_with_parent()}")
        return dialog_azzo


    def run(self, procedure, run_mode, image, drawables, config, run_data):
        # just for debug: not required for the plugin purpose 
        Gimp.message_set_handler(Gimp.MessageHandlerType.CONSOLE) # MESSAGE_BOX = 0, CONSOLE = 1, ERROR_CONSOLE = 2

        # Any plug-in that provides a user interface should call this function
        # (It’s a convention to use the name of the executable and _not_ the PDB procedure name)
        GimpUi.init(CONSTS.FILE_NAME)

        print("Executing: ", CONSTS.FILE_NAME)

        currently_open_images = Gimp.get_images()
        # now let's remove the current image:
        currently_open_images.remove(image)


        tot_images = len(currently_open_images)

        # quick bail
        if tot_images == 0:
            print("Nothing to do. Exiting... ;)", tot_images)
            return self.end_of_the_procedure(procedure)
        
        #there is at least another image to compare to:
        to_compare = None

        if tot_images == 1:
            print("************** Only one **************")
            to_compare = currently_open_images[0]
        else:
            #TO DO - make dialog to select the other image
            to_compare = currently_open_images[0]
            im_co_box = GimpUi.ImageComboBox.new(lambda current_img, unwanted_img = image: current_img is not unwanted_img)
            sel_dialog = self.to_new_dialog(im_co_box, True)
            sel_dialog.run()

            sel_success, sedl_id = im_co_box.get_active()
            if sel_success:
                to_compare = Gimp.Image.get_by_id(sedl_id)
                print(f"Ok, a selection exists: ➡️➡️➡️   {to_compare.get_name()}")
            else:
                print("🤦merd🤦")
            
            sel_dialog.destroy()
                
            #print("############## GET_ACTIVE!:", im_co_box.get_active())
            #print("############## GET_Model!:", im_co_box.get_model())
            #aaa, bbb = im_co_box.get_active()
            #print("get_active VARS:", aaa, bbb) #im_co_box.get_active_id(bbb))
            #pordi = im_co_box.get_model().get_value(im_co_box.get_active_iter(), 1)
            #model = im_co_box.get_model()
            #print(model, type(model), aaa, bbb)
            #print("ATL@@@@@@@@@@@@@@@@-------->", pordi)
            #print(f"***** ***** idx: {bbb} ***** ***** Sel NAME: {im_co_box.get_model()[bbb][1]}")

            #for row in im_co_box.get_model():
            #    if bbb == row[0]:
            #        print("✔️", row[1], "bbb gius:", bbb)
            #    else:
            #        print("row[0]", row[0], "row:", type(row[0]),"bbb:", type(bbb))
            #        print("❌ No!")
            
            # the previous line is a placeholder!
        
        # compare
        overlapped_names, amount = self.compare_set(to_compare, image)

        hint_mess = ""
        dup_layers = []
        if amount != 0:
            hint_mess += f"Overlaps: {amount}\n"
            for elem in overlapped_names:
                hint_mess += f"{elem}\n"
        else:
            hint_mess += f"NO Overlaps :)\n"
        
        test_hint = GimpUi.HintBox.new(hint_mess)
        if amount != 0:
            test_hint.get_children()[0].set_from_icon_name("gimp-tool-heal", 12)
        
        hint_dialog = self.to_new_dialog(test_hint)
        hint_dialog.run()
        hint_dialog.destroy()


        #debug result:
        decor = "*" * 8
        print(f"{decor} Result {decor}\n Overlaps: {amount}\n {overlapped_names}\n{decor} Done processing {decor}")

        #optional: select layers
        #image.set_selected_layers([layers])

        '''
        #reference for dialog:
        
        ##GimpUi.init("qwe")
        dialogazzo = GimpUi.Dialog.new()
        test = GimpUi.HintBox.new("*** FRFqwe ***\nRiqwe2222222")
        test.set_size_request(300, 200) # hmm...
        dialogazzo.get_content_area().add(test)

        hint_immy = test.get_children()[0]
        hint_immy.set_from_icon_name("gimp-tool-heal", 12) #GimpUi.ICON_GRAVITY_EAST   #"gimp-controller", 6)
        test.show()
        dialogazzo.run()
        '''

        # At this point, all is ok: return Success
        return self.end_of_the_procedure(procedure) #procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(TrisPluginCompareLayerNames.__gtype__, sys.argv)



""" colA = Gdk.RGBA(0.5, 0, 0.5)
colB = Gdk.RGBA(0.9, 9, 0.0)

GimpUi.init("plug_in_binary")
dialogazzo = GimpUi.Dialog.new()
dialogazzo.add_button("Maybe_OK", Gtk.ResponseType.OK)
dialogazzo.add_button("Boh! Fatto", Gtk.ResponseType.APPLY)
dialogazzo.add_button("_Cancel", Gtk.ResponseType.CANCEL)


dialog_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 2)
dialogazzo.get_content_area().add(dialog_box)
dialog_box.show()

labels = ["A", "B", "z"]
result_set = set()

view = Gtk.TextView()
view.set_wrap_mode(Gtk.WrapMode.WORD)
view.set_editable(False)
buffer = view.get_buffer()

def set_to_string(argset):
    complete = "| "
    for elem in argset:
        complete += f"{elem} - "
    #complete += " |"
    return (complete[:len(complete) - 1]) + " |"

def test_clicked(self):
    idx = self.idx
    print(f"clicked: {pulsante.get_label()} -> Value: {idx}")
    if idx in result_set:
        result_set.remove(idx)
        self.override_background_color(Gtk.StateFlags.NORMAL, colA)
    else:
        result_set.add(idx)
        self.override_background_color(Gtk.StateFlags.NORMAL, colB)
    
    buffer.set_text(set_to_string(result_set), -1)
    print(result_set)
    return result_set

for idx, name in enumerate(labels):

    pulsante = GimpUi.Button.new_with_label(name)
    pulsante.idx = idx
    pulsante.set_size_request(80, 60)
    dialog_box.pack_start(pulsante, False, False, 1)
    pulsante.connect('clicked', test_clicked)
    
    pulsante.override_background_color(Gtk.StateFlags.NORMAL, colA)
    pulsante.show()

dialog_box.add(view)
view.show()
#dialogazzo.run()

print("Fatto" if dialogazzo.run() else "Unca!") """
