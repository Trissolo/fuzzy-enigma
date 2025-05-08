import gi

#gi.require_version("Gimp", "3.0")
#from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .hovernameschooser import hovernamesChooser
from .TrisSummary import TrisSummary
from .trisLabel import TrisLabel
from .generic_helpers import make_box, make_button
from .Necessary import Necessary

class TrisDialog(Necessary, GimpUi.Dialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_border_width(10)
        self.set_name("THE TrisDialog!")
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Done (Save [not yet implemented])", Gtk.ResponseType.OK)

        #top bar
        top_div = self.make_top_bar()
        self.get_content_area().pack_start(top_div, False, False, 4)

        #containers
        left_box, right_box = self.generate_containers()

        #populate
        for idx, prop in enumerate(self.gamedata["thingProps"]):
            summary_widget = TrisSummary(prop, idx)
            left_box.pack_start(summary_widget.div, False, False, 0)
            self.summary_widgets_ary[idx]=summary_widget
        
        #hardcoded test!
        temp_tool_widget = hovernamesChooser("hovernames", 0, self)
        self.tool_widgets_ary[0] = temp_tool_widget
        print("Confirm Button", temp_tool_widget.get_button())
        right_box.pack_start(temp_tool_widget.div, True, True, 0)
        
    # def hide_all_widget_tools(self):
    #     for elem in self.tool_widgets_ary:
    #         elem.hide()
    #     return self
    
    def generate_summary_widget(self, param, idx):
        return TrisSummary(param, idx, self)
       
    def generate_containers(self):
        temp_sp = 4

        left_box = make_box(False, temp_sp, "Summary Box")
        right_box = make_box(True, temp_sp, "Tools Box")   
        ulteriore = make_box(True, temp_sp, "Ulteriore")

        ulteriore.pack_start(left_box, False, True, temp_sp)
        ulteriore.pack_start(right_box, True, True, temp_sp)

        self.get_content_area().pack_start(ulteriore, True, True, temp_sp)
        self.get_content_area().set_name("Dialog Content Area")

        self.left_box = left_box
        self.right_box = right_box
        return left_box, right_box
    
    
    
    
    def make_top_bar(self):
        update_button = make_button(GimpUi.ICON_VIEW_REFRESH, "Update Layer", self.update_button_action, self)
        #update_button.connect("clicked", self.update_button_action, self)

        label_for_image_name = TrisLabel(f"<{self.image.get_name()}>")
        label_for_image_name.set_name("Descr Image Name")
        label_for_image_name.show()

        top_div = make_box(True, 4, "Div Top Bar")

        top_div.pack_start(update_button, False, False, 0)
        top_div.pack_start(label_for_image_name, True, True, 0)

        self.update_button = update_button
        self.label_for_image_name = label_for_image_name
        return top_div
    
    @staticmethod
    def update_button_action(button, self):
        self.update_current_layer()
        self.label_for_image_name.set_text(self.current_layer.get_name(), bgcolor=0x656598, pad=6)
