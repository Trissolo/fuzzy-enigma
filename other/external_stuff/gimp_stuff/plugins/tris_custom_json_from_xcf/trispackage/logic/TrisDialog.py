from .LayerManager import LayerManager
from .TrisSummary import TrisSummary
from ..splitted_gamedata.gamedata_grabber import thingProps_dataSize, names
import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class TrisDialog(LayerManager):
    def __init__(self, image):
        super().__init__(image=image)
        self.gui_widget = []

        # Test layer stuff...
        print(f"TrisDialog's {self.layer.get_name() =}")
        print(self.update_layer())

        for jproperty in thingProps_dataSize.keys():
            self.gui_widget.append(TrisSummary(jproperty, names["hover_names_ary"]))
        
        print("\nREFRESHING:")
        for widget in self.gui_widget:
            widget.refresh()
        
    def make_dialog(self):
        dialog = GimpUi.Dialog.new()
        dialog.set_title('Test_update_button')
        dialog.set_border_width(10)
        dialog.set_name("THE TrisDialog!")
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Done (Save [not yet implemented])", Gtk.ResponseType.OK)
        
