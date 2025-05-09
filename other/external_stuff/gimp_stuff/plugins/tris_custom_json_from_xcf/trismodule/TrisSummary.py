import gi

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .trisLabel import TrisLabel

from .generic_helpers import make_button, make_box, multipack
from .Necessary import Necessary

class TrisSummary(Necessary):
    def __init__(self, prop, idx):
        self.property = prop
        self.idx = idx
        self.parasite_data = None

        #First Label
        self.label_key = TrisLabel(prop)
        self.label_key.set_xalign(0)
        self.show_off_key()

        #Second Label
        self.label_value = TrisLabel(prop)
        self.label_value.set_xalign(0)
        self.label_value.write("----", bgcolor=0x666666, monospace=True, pad=6)

        # First Button
        self.button_a = make_button(GimpUi.ICON_MENU_RIGHT, f"Button_a {prop}", type(self).introduce_hovernames, self)
        
        # Second Button
        self.button_b = make_button(GimpUi.ICON_DOCUMENT_SAVE, f"Button_b for saving: {prop}", None, self)
        self.button_b.hide()

        # Box container
        div = make_box(True, 4, f"Div Left for{prop}")
        multipack(div, self.label_key, self.label_value, packing=True, spacing=2)
        multipack(div, self.button_a, self.button_b, from_end=True, packing=False, spacing=2)
        self.div = div

        #At first the save button is hidden
        self.button_b.hide()

        # (end TrisSummary init)
    
    def show(self):
        self.div.show()
        return self
    
    def hide(self):
        self.div.hide()
        return self
    
    def receive_data(self, para_data):
        self.parasite_data = para_data
        self.refresh_description()
        self.button_b.show()
    
    def get_button_a(self):
        return self.button_a
    
    def get_button_b(self):
        return self.button_b
    
    def show_off_key(self, is_bold = False):
        self.label_key.write(f"{self.property}:", color=0x989898, monospace=True, pad=1, bold=is_bold, size=110)
        return self
    
    def refresh_description(self, text = None):
        self.show_off_key(True)
        if not text:
            crazy_text = self.tool_widget_from_idx(self.idx).enum.get_corresponding(self.parasite_data)
            self.label_value.write(crazy_text, bgcolor=0x45ba76, size=116, pad=3, monospace=True)
        else:
            self.label_value.write(text=text, color=0x01030a, size=110, pad=3, monospace=True)
    
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
