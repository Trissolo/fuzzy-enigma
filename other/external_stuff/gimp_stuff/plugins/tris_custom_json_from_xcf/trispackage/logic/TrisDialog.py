from .LayerManager import LayerManager
from .TrisSummary import TrisSummary
from ..splitted_gamedata.gamedata_grabber import thingProps_dataSize

class TrisDialog(LayerManager):
    def __init__(self, image):
        super().__init__(image=image)
        self.gui_widget = []

        # Test layer stuff...
        print(f"TrisDialog's {self.layer.get_name() =}")
        print(self.update_layer())

        for jproperty in thingProps_dataSize.keys():
            self.gui_widget.append(TrisSummary(jproperty, []))
        
