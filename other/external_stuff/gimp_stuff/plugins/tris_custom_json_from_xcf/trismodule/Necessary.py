# import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

# gi.require_version("GimpUi", "3.0")
# from gi.repository import GimpUi

# gi.require_version("Gtk", "3.0")
# from gi.repository import Gtk


class Necessary():
    def __init__(self, gimp_image, gamedata, **kwargs):
        self._image = gimp_image
        self._gamedata = gamedata
        self.update_current_layer()
        notab = '@'*11
        print(f"{notab} Necessary init called, now callng super()__init__(**kwargs) - super: {super().__init__}{notab}")
        super().__init__(**kwargs)
    
    @property
    def image(self):
        return self._image
    def update_current_layer(self):
        sel_layers = self.image.get_selected_layers()
        assert sel_layers is not None or len(sel_layers) != 0, "No layer selected! Make sure that at least one layer exists in image!"
        self._current_layer = sel_layers[0]
        return self.current_layer
    @property
    def current_layer(self):
        return self._current_layer 
    @property
    def gamedata(self):
        return self._gamedata  
