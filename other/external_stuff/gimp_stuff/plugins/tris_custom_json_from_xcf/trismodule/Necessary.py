# import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

# gi.require_version("GimpUi", "3.0")
# from gi.repository import GimpUi

# gi.require_version("Gtk", "3.0")
# from gi.repository import Gtk


class Necessary():
    _ready = False
    _image = None
    _current_layer = None
    _gamedata = None
    _tool_widgets_ary = None
    _summary_widgets_ary = None

    @classmethod
    def setup(cls, image, gamedata):
        if not cls._ready:
            cls._ready = True
            cls._image = image
            cls._gamedata = gamedata
            length = len(gamedata["thingProps"])
            cls._tool_widgets_ary = [None] * length
            cls._summary_widgets_ary = [None] * length
            print(f"Necessary set-up!\n(Empty slots: [{length}])\n")
        else:
            print("Necessary already set.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @property
    def image(self):
        return type(self)._image
    
    def update_current_layer(self):
        sel_layers = self.image.get_selected_layers()
        assert type(sel_layers) is list and len(sel_layers) != 0, "No layer selected! Make sure that at least one layer exists in image!"
        #type(self)._current_layer = sel_layers[0]
        self.current_layer = sel_layers[0]
        return self.current_layer
    
    @property
    def current_layer(self):
        return type(self)._current_layer
    
    @current_layer.setter
    def current_layer(self, value):
        print("Instance is setting the current_layer")
        type(self)._current_layer = value
    
    @property
    def gamedata(self):
        return self._gamedata
    
    @property
    def tool_widgets_ary(self):
        return type(self)._tool_widgets_ary
    
    @property
    def summary_widgets_ary(self):
        return type(self)._summary_widgets_ary
    
    def tool_widget_from_idx(self, index):
        return self.tool_widgets_ary[index]
    
    def summary_widget_from_idx(self, index):
        return self.summary_widgets_ary[index]
