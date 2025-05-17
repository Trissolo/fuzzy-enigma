class LayerManager():
    def __init__(self):
        self.image = None
        self.summary_ary = []
        print("LayerManager not yet initialized")
    
    def set_image(self, image):
        self.image = image
        self.layer = image.get_selected_layers()[0] # or 'self.layer = None' in '__init__'? I'm not sure, yet
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
         print(f"{len(self.summary_ary) = }")
