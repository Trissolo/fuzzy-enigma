# import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

# gi.require_version("GimpUi", "3.0")
# from gi.repository import GimpUi

# gi.require_version("Gtk", "3.0")
# from gi.repository import Gtk


class Necessary():
    _image = None
    _current_layer = None
    _gamedata = None
    _ready = False
    _current_layer = None

    @classmethod
    def setup(cls, image, gamedata):
        if not cls._ready:
            cls._ready = True
            cls._image = image
            cls._gamedata = gamedata
            print("Necessary set-up!")
        else:
            print("Necessary already set.")

    def __init__(self, **kwargs):
        self.update_current_layer()
        notab = '@'*11
        print(f"{notab} Necessary init called, now callng super()__init__(**kwargs) - super: {super().__init__}{notab}")
        super().__init__(**kwargs)
    
    @property
    def image(self):
        return type(self)._image
    
    def update_current_layer(self):
        sel_layers = self.image.get_selected_layers()
        assert type(sel_layers) is list and len(sel_layers) != 0, "No layer selected! Make sure that at least one layer exists in image!"
        type(self)._current_layer = sel_layers[0]
        return self.current_layer
    @property
    def current_layer(self):
        return type(self)._current_layer
    
    @property
    def gamedata(self):
        return self._gamedata  
