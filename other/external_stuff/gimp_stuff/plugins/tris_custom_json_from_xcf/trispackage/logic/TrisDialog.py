from .LayerManager import LayerManager

class TrisDialog(LayerManager):
    def __init__(self, image):
        super().__init__(image=image)
        from trispackage import TrisData

        # Test layer stuff...
        print(f"TrisDialog's {self.layer.get_name() =}")
        print(self.update_layer())

        # for _ in range(5):
        #     
        data_holder = TrisData.Condition()