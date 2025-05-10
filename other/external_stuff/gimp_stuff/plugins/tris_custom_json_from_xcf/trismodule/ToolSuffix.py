import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

# gi.require_version("GimpUi", "3.0")
# from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .TrisEnum import TrisEnum
from .Necessary import Necessary

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

    def _populate_enums(self):
        for idx, elem in enumerate(["BOOL", "CRUMBLE", "NIBBLE", "BYTE"]):
            self._enums.append(TrisEnum(self.gamedata[elem], f"Names for {elem} variables"))

    @property
    def enum(self):
        return self._enums[self.actual_varkind]
    