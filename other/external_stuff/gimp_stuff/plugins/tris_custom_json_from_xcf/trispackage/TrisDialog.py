from trispackage import callable_layer_manager_instance, TrisData

class TrisDialog():
    def __init__(self, image):
        # first of all set the image
        self.layer = callable_layer_manager_instance
        self.layer.set_image_globally(image)

        print(f"TrisDialog's {self.layer() =}")
        print(f'\nTrisDialog here!\n {self.layer().get_name() =}')
        
        self.summary_ary = []

        # for _ in range(5):
        data_holder = TrisData(3)
        data_holder.layer = callable_layer_manager_instance
        print(f"This time is an instance of TrisData: {data_holder.layer().get_image().get_name()}")
        #     self.summary_ary.append(data_holder)
        