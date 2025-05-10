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
    def __init__(self, prop, idx):
        self.idx = idx
        self.property = prop

        self._enums = []
        self.actual_varkind = 0

        self.data_for_parasite = None
        self._populate_enums()
        self.div = Gtk.Box.new(Gtk.Orientation.VERTICAL, spacing=0)

        print("ToolSuffix TEST", self.enum.get_all(1))
        self._build_radio_buttons()

    def _populate_enums(self):
        for idx, elem in enumerate(["BOOL", "CRUMBLE", "NIBBLE", "BYTE"]):
            self._enums.append(TrisEnum(self.gamedata[elem], f"Names for {elem} variables"))

    @property
    def enum(self):
        return self._enums[self.actual_varkind]

    def _build_radio_buttons(self):
        #radioFrame = GimpUi.IntRadioFrame.new(["A", "B", "C"])
        #self.div.pack_start(radioFrame, False, False, 0)
        #radioFrame.show()

        hbox = make_box(is_horizontal=True, spacing=1, name="Radio Buttons Container")
        hbox.set_homogeneous(True)

        prev = None
        for idx, var_kind in enumerate(["BOOL", "CRUMBLE", "NIBBLE", "BYTE"]):
            button = Gtk.RadioButton.new_from_widget(prev)
            button.set_label(f"{var_kind} ({idx})")
            button.value = idx
            button.connect("toggled", self.on_button_toggled)
            hbox.pack_start(button, False, False, 0)
            button.show()
            prev = button
        multipack(self.div, hbox, from_end=False, packing=True, spacing=2)
        hbox.show()
    def on_button_toggled(self, button):
        #print(self, sep="\n")
        if button.get_active():
            self.set_actual_varkind(button.value)
        else:
            print("This 'else' us useless - old value was:", button.value)
    def set_actual_varkind(self, value = 0):
        self.actual_varkind = value
        print("Set:", self.actual_varkind)
    def show(self):
        self.div.show()