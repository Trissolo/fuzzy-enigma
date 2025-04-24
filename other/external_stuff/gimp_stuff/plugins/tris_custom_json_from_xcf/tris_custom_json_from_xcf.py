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
#from gimpfu.gui.dialog import Dialog 
#print("gimpfu.gui", teimp)



# constants:
class CONSTS:
    FILE_NAME = GLib.path_get_basename(__file__).removesuffix(".py")


class PropWidgetManager():
    pass


class ExtFrame(Gtk.Frame):
    colors = ["#f7e26b", "#eb8931", "#ccc", "#3939c8"] #["#111", "#81c784", "#333", "#777"]
    @staticmethod
    def customDestroy(widget):
        print("customDestroy:", widget.porconame)
    @staticmethod
    def first_button_clicked(widget, self):
        print("Click", self.bool_test)
        self.bool_test = not self.bool_test
        self.write_prop(self.bool_test)
        #print("customDestroy:", widget.porconame)   
    @staticmethod
    def toggle_visibility(widget, container, raw_name):
        if container.get_visible():
            container.hide()
            widget.set_label(f"{raw_name} ⚫") #"🕳️"
        else:
            container.show()
            widget.set_label(f"{raw_name} 👁️")
    def __init__(self, json_prop):#, optional_label = None):
        super().__init__()
        self.json_prop = json_prop
        self.box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)
        nextWidget = self.btn_as = GimpUi.Button.new()
        nextWidget.set_label(json_prop + " (toggle)")
        nextWidget.connect("clicked", type(self).toggle_visibility, self.box, self.json_prop)
        nextWidget.show()
        self.set_label_widget(nextWidget)
        self.json_key = Gtk.Label.new(f"Prop: {json_prop}???")
        self.json_key.set_use_markup(True)
        self.json_value = Gtk.Label.new("Value ???")
        self.json_value.set_use_markup(True)
        self.btn_as = GimpUi.Button.new_from_icon_name("edit-delete", 1) #"document-properties", 1)
        self.btn_as.connect("clicked", type(self).first_button_clicked, self)
        self.bool_test = True
        self.add(self.box)
        self.insert(self.json_key)
        self.insert(self.json_value)
        self.insert(self.btn_as)
        self.show_all()
        print(json_prop, len(self.get_children()), self.json_value.get_visible())
    def insert(self, widget):
        self.box.pack_start(widget, False, False, 1)
        return self      
    def write_prop(self, value_is_set = True):
        cols = type(self).colors
        fgc, bgc = (cols[0], cols[1]) if value_is_set else (cols[2], cols[3])
        self.json_key.set_markup(f'<span background="{bgc}" foreground="{fgc}"> {self.json_prop} </span>:') # <i>[0, 4]</i>')
        return self
    
    def add_paned_test(self):     
            searcWidget = Gtk.SearchEntry()
            searcWidget.show()
            
            def on_search_activated(searchentry, self):
                t = searchentry.get_text()
                self.lettererichieste = t
                self.listbox.invalidate_filter()
                #print(f"SearchEntry text: {t if len(t) != 0 else '---'}")
            
            searcWidget.connect("search-changed", on_search_activated, self)
            paned = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
            paned.pack1(searcWidget, False, False)
            paned.show()
            self.insert(paned)

            scrolled = Gtk.ScrolledWindow.new(None, None)
            paned.pack2(scrolled, False, False)

            listbox = Gtk.ListBox()
            scrolled.add(listbox)

            #paned.pack2(listbox, False, False)
            self.lettererichieste = "e"

            for item in ["gene", "elevator", "thought", "patience", "explanation", "chemistry", "movie", "excitement"]: #items:
                listbox_element = Gtk.ListBoxRow.new()
                listbox_element.data = item
                listbox_element.add(Gtk.Label(label = item))
                listbox.add(listbox_element)
            
            def sort_func(row_1, row_2, data, notify_destroy):
                return row_1.data.lower() > row_2.data.lower()
            
            listbox.set_sort_func(sort_func, None, False)

            def another_filter_func(row, data, notify_destroy):
                return True if data.lettererichieste in row.data else False
            
            listbox.set_filter_func(another_filter_func, self, False)

            self.listbox = listbox

            def on_row_activated(listbox_widget, row, instance):
                instance.json_value.set_markup(f'<i>{row.data}</i>')
                #print("Option", row.data, instance.lettererichieste)

            listbox.connect("row-activated", on_row_activated, self)







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
        from myutils import elenca_figli


        # a sort of "__init__" method:
        self.basic_setup(image)


        # initialize Gtk!
        GimpUi.init(CONSTS.FILE_NAME)

        #draft for dialog!
        dialogazzo = dialogazzo = GimpUi.Dialog.new()
        dialogazzo.add_button("Done", Gtk.ResponseType.OK)
        

        new_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 2)
        new_box.set_name("menu container")

        btn_update_layer = GimpUi.Button.new()
        btn_update_layer.set_name("Button Update-Layer")
        btn_update_layer.set_label("Capture Layer!")
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

        #elenca_figli(dialogazzo)
        test = ExtFrame("Hovered_name") ##, "HoverName")
        test.write_prop()
        test.add_paned_test()
        main_container.pack_start(test, False, False, 1)

        print("SELF!!!", self, "\nTYPE:", type(self))

        dialogazzo.show_all()
        dialogazzo.run()


        # We have reached the end of the procedure: let's return "Success"
        return self.procedure_is_complete(procedure)  #procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(AdventureGameNook.__gtype__, sys.argv)

