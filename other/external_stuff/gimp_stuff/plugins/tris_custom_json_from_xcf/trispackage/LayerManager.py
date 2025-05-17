from .SharedContainer import tris_container

# class LayerManager():
#     image = None
#     _layer = None
#     container = tris_container
#     @classmethod
#     def setup(cls, image):
#         cls.image = image
#     @classmethod
#     def update_layer(cls):
#         temp_list = cls.image.get_selected_layers()
#         assert type(temp_list) is list and len(temp_list) != 0, "No layer selected! Make sure that at least one layer exists in image!"
#         cls._layer = temp_list[0]
#         # selected_layers = cls._image.get_selected_layers()
#         # cls._current_layer = selected_layers[0]

class _LayerManager():
    def __init__(self):
        self.image = None
        #self._layer = None
        #self.layer = None
        self.tris_container = tris_container
        print("LayerManager not yet initialized")
    
    def set_image(self, image):
        self.image = image
        self.update_layer()
        print("LayerManager INITIALIZED")

    # @property
    # def layer(self):
    #     return self._layer
    
    # @layer.setter
    # def layer(self, value):
    #      self._layer = value

    def update_layer(self):
            self.layer = self.image.get_selected_layers()[0]
            self.check_parasites()
            return self.layer
    
    def check_parasites(self):
         print("\nChecking data...")
         print(f"{len(self.tris_container.summary_widgets) = }")


layer_manager = _LayerManager()
