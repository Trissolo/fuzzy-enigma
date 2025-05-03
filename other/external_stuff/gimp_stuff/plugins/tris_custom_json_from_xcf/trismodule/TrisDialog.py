import gi

#gi.require_version("Gimp", "3.0")
#from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class TrisDialog(GimpUi.Dialog):
    def __init__(self, tris_manager):
        super().__init__(self)
        self.set_border_width(10)
        self.tris_manager = tris_manager
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Done (Save)", Gtk.ResponseType.OK)
        
        left_box, right_box = self.generate_containers()

        self.widget_list = []
        
        for idx, prop in enumerate(tris_manager.gamedata["thingProps"]):
            summary_widget = self.generate_summary_widget(prop, idx)
            left_box.pack_start(summary_widget, True, True, 0)
            
            right_w = self.generate_tool_widget(prop, idx)
            self.widget_list.append(right_w)
            right_box.pack_start(right_w, True, True, 0)
        #test separator:
        #temp_sep = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
        #print(temp_sep.get_visible())
        #temp_sep.show()
        #left_box.pack_start(temp_sep, False, True, 0)
        # end PorcusDialog's __init__

    @staticmethod
    def show_tool_widget(button , wlist):
        for elem in wlist:
            elem.hide()
        wlist[button.idx].show()
    def generate_tool_widget(self, param, idx):
        return Gtk.Label.new(f"[Prop #{param} label]")
    def generate_summary_widget(self, param, idx):
            toggle_prop_tools_button = GimpUi.Button.new_with_label(f"Prop-{param} ->")
            toggle_prop_tools_button.idx = idx
            toggle_prop_tools_button.connect('clicked', self.show_tool_widget, self.widget_list)
            toggle_prop_tools_button.show()
            return toggle_prop_tools_button
    def generate_containers(self):
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        left_box.set_name("Summary Box")
        left_box.show()

        right_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        right_box.set_name("Tools Box")
        right_box.show()
        
        ulteriore = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        ulteriore.set_name("Ulteriore")
        ulteriore.show()
        ulteriore.pack_start(left_box, True, True, 4)
        ulteriore.pack_start(right_box, True, True, 4)

        self.get_content_area().pack_start(ulteriore, True, True, 4)
        self.get_content_area().set_name("Dialog Content Area")
        return left_box, right_box
    