import gi

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .trisLabel import TrisLabel
#from .TrisDialog import TrisDialog

class TrisSummary():
    def __init__(self, prop, idx, trisDialog):
        self.trisDialog = trisDialog
        self.property = prop
        self.idx = idx
        self.prop_desc = TrisLabel(prop) #Gtk.Label.new(f"(Prop #{prop} label[{idx}])")
        self.prop_desc.set_xalign(0)
        self.prop_desc.write(bgcolor=0x666666, monospace=True, pad=6)
        #qwelabel = TrisLabel("aa")
        self.div = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 4)

        div = self.div
        div.set_name(f"Div Left for{prop}")
        div.show()
        button_show = GimpUi.Button.new_from_icon_name(GimpUi.ICON_EDIT_REDO, 1)
        button_show.set_name(f"Button_show {prop}")
        button_show.show()
        button_show.connect('clicked', type(self).button_show_on_click, self)
        div.pack_start(self.prop_desc, True, True, 2)
        div.pack_end(button_show, False, False, 2)
        self.button_show = button_show
    def show(self):
        self.div.show()
        return self
    def hide(self):
        self.div.hide()
        return self
    @staticmethod
    def button_show_on_click(button, self):
        print("Button_show Clicked")
        self.trisDialog.hide_all_widget_tools().tool_widgets_ary[self.idx].show()
        return True

'''

        
        #div.set_halign(Gtk.Align.END) #CENTER) #.END)   #.START)
        #print("Newly create box align:", div.get_halign())
        div.idx = idx
        label = Gtk.Label.new(f"[Prop #{param} label]")
        #button_change = GimpUi.Button.new_from_icon_name(GimpUi.ICON_SHAPE_CIRCLE, 1) #GimpUi.Button.new_with_label(f"confirm change")
         #GimpUi.Button.new_with_label(f"Select prop {param}")
        button_show.set_name(f"Button_show {param}")
        button_show.connect('clicked', type(self).button_show_on_click)
        for child in [label, button_show]:
             child.show()
             div.pack_start(child, False, False, 4)
        div.show()
        return div
'''