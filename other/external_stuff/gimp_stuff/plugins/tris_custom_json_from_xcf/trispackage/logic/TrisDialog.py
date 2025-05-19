from .LayerManager import LayerManager
from .TrisSummary import TrisSummary
from ..splitted_gamedata.gamedata_grabber import thingProps_dataSize

class TrisDialog(LayerManager):
    def __init__(self, image):
        super().__init__(image=image)
        self.gui_widget = []
        #from trispackage import TrisData

        # Test layer stuff...
        print(f"TrisDialog's {self.layer.get_name() =}")
        print(self.update_layer())

        for elem in thingProps_dataSize.keys():
            self.gui_widget.append(TrisSummary(elem, None))
