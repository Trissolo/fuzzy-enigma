from .LayerManager import LayerManager
from .TrisSummary import TrisSummary
from ..splitted_gamedata.gamedata_grabber import thingProps_dataSize, names

class TrisDialog(LayerManager):
    def __init__(self, image):
        super().__init__(image=image)
        self.gui_widget = []

        # Test layer stuff...
        print(f"TrisDialog's {self.layer.get_name() =}")
        print(self.update_layer())

        for jproperty in thingProps_dataSize.keys():
            self.gui_widget.append(TrisSummary(jproperty, names["hover_names_ary"]))
        
        print("\nREFRESHING:")
        for widget in self.gui_widget:
            widget.refresh()
        
