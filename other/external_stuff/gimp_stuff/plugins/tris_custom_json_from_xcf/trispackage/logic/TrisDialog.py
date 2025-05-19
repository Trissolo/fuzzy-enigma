#from trispackage.logic.LayerManager import LayerManager
from .LayerManager import LayerManager
#from .TrisData import TrisData

class TrisDialog(LayerManager):
    def __init__(self, image):
        super().__init__(image=image)
        from trispackage import TrisData
        # first of all set the image
        #self.layer = callable_layer_manager_instance
        #self.layer.set_image_globally(image)

        print(f"TrisDialog's {self.layer =}")
        #print(f'\nTrisDialog here!\n {self.layer.get_name() =}')
        
        #self.summary_ary = []

        # for _ in range(5):
        #print(f"**** TESTING TrisDATA ****")#.get_parasite_list()}")
        data_holder = TrisData.Condition()
        #data_holder.layer = callable_layer_manager_instance
        print(f"This time is an instance of TrisData: {data_holder.layer.get_parasite_list()}")
        #data_holder.info()
        #data_holder.get_image_name()
        #     self.summary_ary.append(data_holder)
        