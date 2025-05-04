import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

# gi.require_version("GimpUi", "3.0")
# from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def makeEventboxForWidget(widget, on_click_handler, *custom_args):
    eventbox = Gtk.EventBox()
    eventbox.set_name(f"EventBox for {widget.get_name()}")
    #
    # def minimun_handler(evbox, event):
    #     pass
    #
    if callable(on_click_handler):
        eventbox.connect("button-press-event", on_click_handler, *custom_args) #type(self).on_click_handler)
    eventbox.add(widget)
    #eventbox.show()
    return eventbox

def make_listbox(option_list):
    listbox = Gtk.ListBox()
    listbox.set_name("Listbox")
    listbox.show()
    # populate the ListBox
    for item in option_list:
        optn_label = Gtk.Label.new(item)
        optn_label.show()
        option = Gtk.ListBoxRow.new()
        option.set_name(f"option {item}")
        option.data = item
        option.add(optn_label)
        option.show()
        listbox.add(option)
    return listbox
    #listbox.set_sort_func(self.sort_func, None, False)
    #listbox.set_filter_func(self.tris_filter_func, self, False)
    #listbox.connect("row-activated", self.on_row_activated_grid, self)
