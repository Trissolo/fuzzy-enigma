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
            cls._tool_widgets_ary = []
            cls._summary_widgets_ary = []
        else:
            print("'Necessary' Class already set.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @property
    def image(self):
        return type(self)._image
    
    def update_current_layer(self):
        print(f"{self} update_current_layer")
        sel_layers = self.image.get_selected_layers()
        assert type(sel_layers) is list and len(sel_layers) != 0, "No layer selected! Make sure that at least one layer exists in image!"
        Necessary._current_layer = sel_layers[0]

        #type(self)._current_layer = sel_layers[0]
        #return self.current_layer
    
    @property
    def current_layer(self):
        return Necessary._current_layer
        # return type(self)._current_layer
    
    # @current_layer.setter
    # def current_layer(self, value):
    #     print(f"{self} current_layer.setter")
    #     type(self)._current_layer = value
    
    @property
    def gamedata(self):
        # maybe... return Necessary._gamedata
        return type(self)._gamedata
    
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
    
    @staticmethod
    def encode_data(data):
        if type(data) is not list:
            data = [data]
        res = " ".join([str(el) for el in data])
        to_bytes = bytes(res.encode('utf-8'))
        return to_bytes
    
    @staticmethod
    def grab_parasite_data(parasite):
        res_string = bytes(parasite.get_data()).decode('utf-8')
        to_int_ary = [ int(x) for x in res_string.split(" ")]
        return to_int_ary[0] if len(to_int_ary) == 1 else to_int_ary
