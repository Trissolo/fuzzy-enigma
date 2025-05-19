class LayerManager():
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
         cls.layer = None
         cls.update()
    @classmethod
    def update(cls):
        cls.layer = cls.image.get_selected_layers()[0]
    # @classmethod
    # def provide_layer(cls):
    #     return cls.layer
    
    # instance things:
    def __init__(self, image):
        if image is not None:
            self.set_image_globally(image)

    @property
    def layer(self):
        return LayerManager.layer #provide_layer()

    #def __call__(self):
    #    return type(self).layer
    
    def set_image_globally(self, image):
        LayerManager.setup(image)


#callable_layer_manager_instance = _LayerManager()
