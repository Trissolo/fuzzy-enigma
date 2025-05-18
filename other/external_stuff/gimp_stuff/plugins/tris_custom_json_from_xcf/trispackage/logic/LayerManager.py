class _LayerManager():
    image = None
    layer = None

    # @property
    # def layer(self):
    #     return self._layer
    
    # @layer.setter
    # def layer(self, value):
    #      self._layer = value

    @classmethod
    def setup(cls, image):
         cls.image = image
         cls.update_layer()
    @classmethod
    def update_layer(cls):
        cls.layer = cls.image.get_selected_layers()[0]
    
    # instance things:
    # def __init__(self):
    #     print("LayerManager instance created")

    def update(self):
        print("A LayerManager's instance is updating layer")
        type(self).update_layer()

    def __call__(self):
        return type(self).layer
    
    def set_image_globally(self, image):
        type(self).setup(image)


callable_layer_manager_instance = _LayerManager()
