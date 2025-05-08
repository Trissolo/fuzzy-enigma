import gi

#gi.require_version("Gimp", "3.0")
#from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .TrisEnum import TrisEnum
from .generic_helpers import make_listbox, make_box, make_button

class hovernamesChooser():
    def __init__(self, prop, idx, trisDialog):
        self.trisDialog = trisDialog
        #self.tris_manager = trisDialog.tris_manager
        self.idx = idx
        self.property = prop
        self.enum = TrisEnum(self.trisDialog.gamedata['onHoverNames'], "Things names (on_pointer_over")
        # Value to save in thr parasite
        self.pending_value_for_parasite = None
        # new text for the descr label
        self.pending_new_description = None
        self.lettererichieste = "a"

        # "div"
        self.div = Gtk.Box.new(Gtk.Orientation.VERTICAL, spacing=0)
        self.div.set_hexpand(True)

        #searchWidget
        searcWidget = Gtk.SearchEntry()
        searcWidget.show()    
        searcWidget.connect("search-changed", self.on_search_activated, self)

        # ListBox:
        listbox = make_listbox(self.enum.tlist)
        listbox.set_sort_func(self.sort_func, None, False)
        listbox.set_filter_func(self.tris_filter_func, self, False)
        listbox.connect("row-activated", self.on_row_activated_grid, self)
        #scrolled
        scrolled = Gtk.ScrolledWindow.new(None, None)
        scrolled.add(listbox)
        scrolled.set_hexpand(True)

        #top container
        self.pending_label = Gtk.Label.new("----")
        self.pending_label.show()
        self.confirm_button = make_button(GimpUi.ICON_MENU_LEFT, "Confirm HoverName Button")# GimpUi.Button.new_from_icon_name(GimpUi.ICON_MENU_LEFT, 1) #Gtk.Button.new_with_label("Click Me")
        self.confirm_button.connect("clicked", self.on_confirm_clicked, self)

        # reset option!
        self.clear_pending_option()

        tcont = make_box(True, 0)##Gtk.Box.new(Gtk.Orientation.HORIZONTAL, spacing=0)
        tcont.pack_start(self.pending_label, True, True, 2)
        tcont.pack_end(self.confirm_button, False, False, 2)
        tcont.show()

        self.listbox = listbox
        self.scrolled = scrolled

        self.div.pack_start(tcont, False, False, 1)
        self.div.pack_start(searcWidget, False, False, 1)
        self.div.pack_start(scrolled, True, True, 1)
    def show(self):
        self.div.show()
        self.listbox.show()
        self.scrolled.show()
    def hide(self):
        self.div.hide()
    @staticmethod
    def sort_func(row_1, row_2, data, notify_destroy):
        return row_1.data.lower() > row_2.data.lower()
    @staticmethod
    def on_search_activated(searchentry, self):
        self.lettererichieste = searchentry.get_text()
        print(self.lettererichieste)
        self.listbox.invalidate_filter()
    @staticmethod
    def tris_filter_func(row, self, notify_destroy):
        return True if self.lettererichieste.lower() in row.data.lower() else False
    @staticmethod
    def on_row_activated_grid(listbox_widget, row, self):
        num, text = self.enum.get_all(row.data)
        self.pending_label.set_text(f"{text} [{num}]")
        self.set_pending(num, text)
        self.confirm_button.show()
    def clear_pending_option(self):
        self.confirm_button.hide()
        self.set_pending()
        self.pending_label.set_text("----")
        return self
    @staticmethod
    def on_confirm_clicked(button, self):
        data = self.get_for_para()
        desc = self.get_new_description()
        print(f"Data to save: {data}, data to update: {desc}")
        merged_stoca = f"{self.property}: {data} ({desc})"
        summary_widget = self.trisDialog.summary_widget_from_idx(self.idx)
        summary_widget.prop_desc.write(merged_stoca, bgcolor=0x666666, monospace=True, pad=6)
        # TO DO: add Parasite!
        self.confirm_button.hide()
        self.clear_pending_option()
        self.hide() #.tool_widget_from_idx
        return self
    def get_button(self):
        return self.confirm_button
    def set_pending(self, num=None, val=None):
        self.pending_value_for_parasite = num
        self.pending_new_description = val
        return self
    def get_for_para(self):
        return self.pending_value_for_parasite
    def get_new_description(self):
        return self.pending_new_description

'''       
        

        
       
        
        listbox.set_hexpand(True)
        #set_hexpand(True)

        self.listbox = listbox

        

        hn_grid.attach(searcWidget, 6, 0, 2, 1)
        hn_grid.attach(scrolled, 6, 1, 2, 3)
        hn_grid.show_all()
        self.hn_grid = hn_grid

    def get_grid(self):
        return self.hn_grid
    @staticmethod
    def tb_ba_action(button, self):
        print("TrisChooser: Not yet implemented save parasite", self.tris_enum.get_all(2))
        print(self.current_layer.get_name(), "<--")
    
    @staticmethod
    def on_search_activated(searchentry, self):
        self.lettererichieste = searchentry.get_text()
        self.listbox.invalidate_filter()
    
    
    
    
    
    
    
    @property
    def current_layer(self):
        return self.trisParent.current_layer
    
    @staticmethod
    def toggle_btn_handler(button, self):
        container = self.box
        if container.get_visible():
            container.hide()
            button.set_label(f"⚫ {self.json_prop}") #"🕳️"
        else:
            container.show()
            button.set_label(f"🟠 {self.json_prop}") # 👁️") #"🟠"
        print(self.current_layer.get_name())
    
    def insert(self, *args):
        for w in args:
            self.box.pack_start(w, False, False, 1)
        return self
'''
