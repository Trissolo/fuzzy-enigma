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
        self.set_name("THE TrisDialog!")
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Done (Save [not yet implemented])", Gtk.ResponseType.OK)
        #special properties
        self.tris_manager = tris_manager
        self.tool_widgets_ary = []
        self.summary_widgets_ary = []
        #containers
        left_box, right_box = self.generate_containers()
        #populate
        for idx, prop in enumerate(tris_manager.gamedata["thingProps"]):
            summary_widget = self.generate_summary_widget(prop, idx)
            left_box.pack_start(summary_widget, True, True, 0)
            self.summary_widgets_ary.append(summary_widget)

            tool_widget = self.generate_tool_widget(prop, idx)
            self.tool_widgets_ary.append(tool_widget)
            right_box.pack_start(tool_widget, True, True, 0)
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
    def hide_all_widget_tools(self):
        for elem in self.tool_widgets_ary:
            elem.hide()
        return self
    @staticmethod
    def tool_show_test(button):
        div = button.get_parent()
        main_dialog = div.get_ancestor(TrisDialog)
        main_dialog.hide_all_widget_tools()
        main_dialog.tool_widgets_ary[div.idx].show()
        return True
    
    def generate_summary_widget(self, param, idx):
        div = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 4)
        div.set_name(f"Div {param}")
        div.idx = idx
        label = Gtk.Label.new(f"[Prop #{param} label]")
        button_change = GimpUi.Button.new_with_label(f"confirm change")
        button_show = GimpUi.Button.new_with_label(f"Select prop {param}")
        button_show.set_name(f"Button_show {param}")
        button_show.connect('clicked', type(self).tool_show_test)
        for child in [label, button_change, button_show]:
             child.show()
             div.pack_start(child, True, False, 4)
        div.show()
        return div
            #toggle_prop_tools_button = GimpUi.Button.new_with_label(f"Prop-{param} ->")
            #toggle_prop_tools_button.idx = idx
            #toggle_prop_tools_button.connect('clicked', self.show_tool_widget, self.tool_widgets_ary)
            #toggle_prop_tools_button.show()
            #return toggle_prop_tools_button
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
    