import gi

#gi.require_version("Gimp", "3.0")
#from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

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
    
class PorcusDialog(GimpUi.Dialog):
    def __init__(self):
        super().__init__()
        self.set_border_width(10)
        
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        left_box.show()
        right_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        right_box.show()
        
        #self.get_content_area().pack_start(left_box, True, True, 4)
        #self.get_content_area().pack_start(right_box, True, True, 4)
        ulteriore = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        ulteriore.show()
        self.get_content_area().pack_start(ulteriore, True, True, 4)
        ulteriore.pack_start(left_box, True, True, 4)
        ulteriore.pack_start(right_box, True, True, 4)
        
        widget_list = []
        self.widget_list = widget_list
        
        for idx in range(4):
            toggle_prop_tools_button = GimpUi.Button.new_with_label(f"PR{idx} ->")
            toggle_prop_tools_button.idx = idx
            toggle_prop_tools_button.connect('clicked', self.show_right_widget, widget_list)
            left_box.pack_start(toggle_prop_tools_button, True, True, 0)
            toggle_prop_tools_button.show()
            right_w = Gtk.Label.new(f"[Prop #{idx} label]")
            widget_list.append(right_w)
            right_box.pack_start(right_w, True, True, 0)
    @staticmethod
    def show_right_widget(button , wlist):
        for elem in wlist:
            elem.hide()
        wlist[button.idx].show()

#dialogazzo = PorcusDialog()
#dialogazzo.show_all()
#dialogazzo.run()
#dialogazzo.destroy()


