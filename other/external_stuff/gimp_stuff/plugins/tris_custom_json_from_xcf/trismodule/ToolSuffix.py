import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .TrisEnum import TrisEnum
from .Necessary import Necessary
from .generic_helpers import make_button, make_box, multipack

class ToolSuffix(Necessary):
    vars_names = ["BOOL", "CRUMBLE", "NIBBLE", "BYTE"]
    def __init__(self, prop, idx):
        self.idx = idx
        self.property = prop

        self._enums = []
        self.actual_varkind = 0

        self.data_for_parasite = []
        self._populate_enums()
        self.lettererichieste = "a"
        self.div = Gtk.Box.new(Gtk.Orientation.VERTICAL, spacing=0)
        self.div.set_hexpand(True)

        print("ToolSuffix TEST", self.enum.get_all(1))
        self._build_radio_buttons()

        #searchWidget
        searchWidget = Gtk.SearchEntry()
        searchWidget.show()    
        searchWidget.connect("search-changed", self.on_search_activated)
        self.searchWidget = searchWidget

        # ListBox:
        listbox = Gtk.ListBox()
        listbox.set_name("Listbox Varnames")
        listbox.show()
        self.listbox = listbox

        # populate the ListBox
        for idx, names_ary in enumerate(self._enums):
            for item in names_ary.tlist:
                optn_label = Gtk.Label.new(item)
                optn_label.show()
                option = Gtk.ListBoxRow.new()
                option.set_name(f"option {item}")
                option.data = item
                option.kind = idx
                option.add(optn_label)
                option.show()
                listbox.add(option)

        listbox.set_sort_func(self.sort_listbox, None, False)
        listbox.set_filter_func(self.tris_filter_func, False)
        #listbox.connect("row-activated", self.on_row_activated_grid)

        #scrolled
        scrolled = Gtk.ScrolledWindow.new(None, None)
        scrolled.add(listbox)
        scrolled.set_hexpand(True)
        scrolled.show()

        self.div.pack_start(searchWidget, False, False, 1)
        self.div.pack_start(scrolled, True, True, 1)

    def on_search_activated(self, searchentry):
        self.lettererichieste = searchentry.get_text()
        print(self.lettererichieste)
        self.listbox.invalidate_filter()

    @staticmethod
    def sort_listbox(row_1, row_2, data, notify_destroy):
        return row_1.data.lower() > row_2.data.lower()
    
    def tris_filter_func(self, row, notify_destroy):
        return True if row.kind == self.actual_varkind and self.lettererichieste.lower() in row.data.lower() else False

    def _populate_enums(self):
        for idx, elem in enumerate(type(self).vars_names):
            self._enums.append(TrisEnum(self.gamedata[elem], f"Names for {elem} variables"))

    @property
    def enum(self):
        return self._enums[self.actual_varkind]

    def _build_radio_buttons(self):
        radio_container = make_box(is_horizontal=True, spacing=0, name="Radio Buttons Container")
        radio_container.set_homogeneous(True)

        prev = None
        for idx, var_kind in enumerate(type(self).vars_names):
            button = Gtk.RadioButton.new_from_widget(prev)
            button.set_label(f"{var_kind.capitalize()} ({idx})")
            button.set_name(var_kind)
            button.value = idx
            button.connect("toggled", self.on_button_toggled)
            radio_container.pack_start(button, False, False, 0)
            button.show()
            prev = button
        self.div.pack_start(radio_container, False, False, 0)
        
        # Directly emit the 'toggled' signal
        radio_container.get_children()[0].emit("toggled")
        radio_container.show()
        # _build_radio_buttons END
    
    def on_button_toggled(self, button):
        if button.get_active():
            self.set_actual_varkind(button.value)
            self.listbox.invalidate_filter()
            self.searchWidget.set_text("")
            self.searchWidget.emit("search-changed")
    
    def set_actual_varkind(self, value = 0):
        self.actual_varkind = value
        self.data_for_parasite.clear()
        self.data_for_parasite.append(value)
        self.data_for_parasite.append(None)
        print(f"\n***\nset_actual_varkind():\nactual_varkind = {self.actual_varkind} ({type(self).vars_names[value]})\nPara data array: {self.data_for_parasite}\n***\n")
    
    def show(self):
        self.div.show()