import gi

#gi.require_version("Gimp", "3.0")
#from gi.repository import Gimp

#gi.require_version("GimpUi", "3.0")
#from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def test():
    print('Isolated stuff here')

def util_eventbox_for_widget(widget, on_click_handler, *custom_args):
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

class TrisLabel(Gtk.Label):
    def __init__(self, text = "My TrisLabel"):
        super().__init__()
        self.set_use_markup(True)
        self.set_name("La TrisLABEL (my extended Gtk.Label -> the click-enabled Widget)")
        self.last_entered_raw_text = ""
        self.set_default_text(text)
        self.show()
    
    def set_default_text(self, text):
        self.default_text = text
    
    def write(self, text = None, color=None, bgcolor=None, size=100, pad=0, padleft=0, padright=0, monospace=False, italic=False, bold = False):
        if text is None: text = self.default_text
        self.last_entered_raw_text = text
        self.set_markup(type(self).assemble_span(text, color, bgcolor, size, pad, padleft, padright, monospace, italic, bold))
    
    @classmethod
    def assemble_span(cls, text, color=None, bgcolor=None, size=100, pad=0, padleft=0, padright=0, monospace=False, italic=False, bold=False):
        color = f'color="#{cls.int_to_hex_string(color)}"' if type(color) == int else ""
        bgcolor = f'bgcolor="#{cls.int_to_hex_string(bgcolor)}"' if type(bgcolor) == int else ""
        size = f'size="{size}%"' if type(size) == int else ""
        pad = " " * pad
        padleft = " " * padleft
        padright = " " * padright
        if italic: text = f"<i>{text}</i>"
        if bold: text = f"<b>{text}</b>"
        if monospace: text = f"<tt>{text}</tt>"
        return f"<span {color} {bgcolor} {size}>{pad}{padleft}{text}{padright}{pad}</span>"  
    
    @staticmethod
    def int_to_hex_string(num):
        return str(hex(num)).removeprefix("0x").zfill(6)
    
    _special_chars = {True: "🟡", False: "⚫"}

    def get_special(self, key = None):
        return type(self)._special_chars.get(key, "🚫")
    


