from trispackage import LayerManager, TrisData

class TrisDialog(LayerManager):
    def __init__(self, image):
        super().__init__(image)
        self.summary_ary = []
        #self.update_layer()

        for _ in range(5):
            data_holder = TrisData(3)
            self.summary_ary.append(data_holder)
        
        print(f'\nTrisDialog here!\n {self.image.get_name() =}')