import gi

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .trisLabel import TrisLabel

from .generic_helpers import make_button, make_box
from .Necessary import Necessary

class TrisSummary(Necessary):
    def __init__(self, prop, idx):
        self.property = prop
        self.idx = idx
        self.parasite_data = None
        self.new_description_text = ""

        #First Label
        self.prop_desc = TrisLabel(prop)
        self.prop_desc.set_xalign(0)
        self.prop_desc.write(bgcolor=0x666666, monospace=True, pad=6)
        
        # First Button
        self.button_a = make_button(GimpUi.ICON_MENU_RIGHT, f"Button_a {prop}", type(self).introduce_hovernames, self)
        
        # Second Button
        self.button_b = make_button(GimpUi.ICON_DOCUMENT_SAVE, f"Button_b for saving: {prop}", None, self)

        # Box container
        div = make_box(True, 4, f"Div Left for{prop}")
        div.pack_start(self.prop_desc, True, True, 2)
        div.pack_end(self.button_a, False, False, 2)
        div.pack_end(self.button_b, False, False, 2)
        self.div = div
    
    def show(self):
        self.div.show()
        return self
    
    def hide(self):
        self.div.hide()
        return self
    
    def receive_data(self, para_data, new_desc):
        self.parasite_data = para_data
        self.new_description_text = new_desc
        self.update_desc()
        self.button_b.show()
    
    def get_button_toggle(self):
        return self.button_a
    
    def get_button_save(self):
        return self.button_b
    
    def update_desc(self, text = None):
        if not text:
            text = self.prop_desc.assemble_span(f"{self.property}:", size=120, bold=True, pad=2)
            text += self.prop_desc.assemble_span(self.new_description_text, bgcolor=0x45ba76, size=130, pad=3, monospace=True)
            self.prop_desc.set_markup(text)
        else:
            self.prop_desc.write(text=text, color=0x01030a, size=111)
    
    @staticmethod
    def introduce_hovernames(button, self):
        print("Called the method 'TrisSummary.introduce_hovernames', but is still incomplete.")
        print("INTRODUCE", self.idx, self.tool_widgets_ary[self.idx])
        twa = self.tool_widgets_ary
        if not twa[self.idx]:
            print("This methos is WIP: widget not yet implemented :(")
            return False
        print("OK - showing the wanted widget.")
        twa[self.idx].show()
        #To Do: hide any other ToolWidget
