import gi

#gi.require_version("Gimp", "3.0")
#from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .TrisEnum import TrisEnum

class hovernamesChooser():
    def __init__(self, prop, idx, trisDialog):
        self.trisDialog = trisDialog
        self.tris_manager = trisDialog.tris_manager
        self.idx = idx
        self.property = prop
        self.enum = TrisEnum(self.tris_manager.gamedata['onHoverNames'], "Things names (on_pointer_over")
        # "div"
        div = Gtk.Box.new(Gtk.Orientation.VERTICAL, spacing=0)
        #div.set_homogeneous(False)
        div.set_hexpand(True)
        
        print("DIV VHEXPAND", div.get_vexpand())
        self.div = div
        #searchWidget
        searcWidget = Gtk.SearchEntry()
        searcWidget.show()
        self.lettererichieste = "a"
        searcWidget.connect("search-changed", self.on_search_activated, self)

        # ListBox:
        listbox = Gtk.ListBox()
        listbox.set_name("Listbox")
        listbox.show()
        # populate the ListBox
        for item in self.enum.tlist:
            #print(f"Enum! {item}")
            option = Gtk.ListBoxRow.new()
            option.data = item
            orc_label = Gtk.Label.new(item)
            option.add(orc_label)
            orc_label.show()
            option.show()
            option.set_name(f"option {item}")
            listbox.add(option)
        listbox.set_sort_func(self.sort_func, None, False)
        listbox.set_filter_func(self.tris_filter_func, self, False)
        listbox.connect("row-activated", self.on_row_activated_grid, self)
        scrolled = Gtk.ScrolledWindow.new(None, None)
        scrolled.add(listbox)
        scrolled.set_hexpand(True)
        #scrolled.set_max_content_height(800)
        #print("**************************scrolled.get_max_content_height()", scrolled.get_max_content_height())
        self.listbox = listbox
        self.scrolled = scrolled
        div.pack_start(searcWidget, False, False, 1)
        div.pack_start(scrolled, True, True, 1)
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
        print(f"Selected: {text} -> idx: {num}")

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
