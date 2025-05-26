import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

# gi.require_version("GimpUi", "3.0")
# from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class LeftSummary():
    def __init__(self):
        self.div = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        