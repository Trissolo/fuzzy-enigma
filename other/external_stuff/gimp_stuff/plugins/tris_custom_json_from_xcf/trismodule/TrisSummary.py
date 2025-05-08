import gi

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .trisLabel import TrisLabel

from .generic_helpers import make_button, make_box
from .Necessary import Necessary

class TrisSummary(Necessary):
    def __init__(self, prop, idx, trisDialog):
        self.trisDialog = trisDialog
        self.property = prop
        self.idx = idx

        #First Label
        self.prop_desc = TrisLabel(prop)
        self.prop_desc.set_xalign(0)
        self.prop_desc.write(bgcolor=0x666666, monospace=True, pad=6)
        
        #First Button
        self.button_a = make_button(GimpUi.ICON_EDIT_REDO, f"button_a {prop}", type(self).introduce_hovernames, self)

        # Box container
        div = make_box(True, 4, f"Div Left for{prop}")
        div.pack_start(self.prop_desc, True, True, 2)
        div.pack_end(self.button_a, False, False, 2)
        self.div = div
    
    def show(self):
        self.div.show()
        return self
    
    def hide(self):
        self.div.hide()
        return self
    
    @staticmethod
    def button_a_on_click(button, self):
        print("button_a Clicked")
        self.trisDialog.hide_all_widget_tools().tool_widgets_ary[self.idx].show()
        return True
    
    def get_button_toggle(self):
        return self.button_a
    
    @staticmethod
    def introduce_hovernames(button, self):
        print("INTRODUCE", self.idx, self.trisDialog.tool_widgets_ary[self.idx])
        self.trisDialog.tool_widgets_ary[self.idx].show()
    # def ultimate_action(self):
    #     tool_widget = self.trisDialog.tool_widget_from_idx(self.idx)
    #     data = tool_widget.get_for_para()
    #     desc = tool_widget.get_new_description()
    #     print(f"Data to save: {data}, data to update: {desc}")
    #     merged_stoca = f"{self.property}: {data} ({desc})"
    #     self.prop_desc.write(merged_stoca, bgcolor=0x666666, monospace=True, pad=6)