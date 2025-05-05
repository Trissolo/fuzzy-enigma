import gi

#gi.require_version("Gimp", "3.0")
#from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .hovernameschooser import hovernamesChooser


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

        #top bar
        top_div = self.make_top_bar()
        left_box.pack_start(top_div, False, False, 4)

        
        #populate
        for idx, prop in enumerate(tris_manager.gamedata["thingProps"]):
            summary_widget = self.generate_summary_widget(prop, idx)
            left_box.pack_start(summary_widget, False, False, 0)
            self.summary_widgets_ary.append(summary_widget)
            assert hasattr(TrisDialog, f"tool_widget_for_{prop}"), f"Method {f'tool_widget_for_{prop}'} inexistent. Please add it to TrisDialog class."
            tool_widget = getattr(TrisDialog, f"tool_widget_for_{prop}")(self, prop, idx, summary_widget)
            #tool_widget = self.generate_tool_widget(prop, idx, summary_widget)
            to_append = tool_widget.div if hasattr(tool_widget, "div") else tool_widget
            self.tool_widgets_ary.append(tool_widget)
            right_box.pack_start(to_append, True, True, 0)
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
    def generate_tool_widget(self, param, idx, summary_widget):
        return Gtk.Label.new(f"(Prop #{param} label[{idx}])")
    def hide_all_widget_tools(self):
        for elem in self.tool_widgets_ary:
            elem.hide()
        return self
    @staticmethod
    def tool_show_test(button):
        div = button.get_parent()
        main_dialog = div.get_ancestor(TrisDialog)
        #main_dialog.hide_all_widget_tools()
        #main_dialog.tool_widgets_ary[div.idx].show()
        main_dialog.hide_all_widget_tools().tool_widgets_ary[div.idx].show()
        return True
    
    def generate_summary_widget(self, param, idx):
        div = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 4)
        div.set_name(f"Div {param}")
        #div.set_halign(Gtk.Align.END) #CENTER) #.END)   #.START)
        #print("Newly create box align:", div.get_halign())
        div.idx = idx
        label = Gtk.Label.new(f"[Prop #{param} label]")
        #button_change = GimpUi.Button.new_from_icon_name(GimpUi.ICON_SHAPE_CIRCLE, 1) #GimpUi.Button.new_with_label(f"confirm change")
        button_show = GimpUi.Button.new_from_icon_name(GimpUi.ICON_EDIT_REDO, 1) #GimpUi.Button.new_with_label(f"Select prop {param}")
        button_show.set_name(f"Button_show {param}")
        button_show.connect('clicked', type(self).tool_show_test)
        for child in [label, button_show]:
             child.show()
             div.pack_start(child, False, False, 4)
        div.show()
        return div
            #toggle_prop_tools_button = GimpUi.Button.new_with_label(f"Prop-{param} ->")
            #toggle_prop_tools_button.idx = idx
            #toggle_prop_tools_button.connect('clicked', self.show_tool_widget, self.tool_widgets_ary)
            #toggle_prop_tools_button.show()
            #return toggle_prop_tools_button
    def generate_containers(self):
        temp_sp = 4
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=temp_sp)
        left_box.set_name("Summary Box")
        left_box.show()

        right_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=temp_sp)
        right_box.set_name("Tools Box")
        right_box.show()
        
        ulteriore = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=temp_sp)
        ulteriore.set_name("Ulteriore")
        ulteriore.show()
        ulteriore.pack_start(left_box, False, True, temp_sp)
        ulteriore.pack_start(right_box, True, True, temp_sp)

        self.get_content_area().pack_start(ulteriore, True, True, temp_sp)
        self.get_content_area().set_name("Dialog Content Area")
        self.left_box = left_box
        self.right_box = right_box
        return left_box, right_box
    def tool_widget_from_idx(self, index):
        return self.tool_widgets_ary[index]
    def summary_widget_from_idx(self, index):
        return self.summary_widgets_ary[index]
    def tool_widget_for_hoverName(self, prop, idx, summary_widget):
        return hovernamesChooser(prop, idx, self)
        #return self.generate_tool_widget(prop, idx, summary_widget)
    def tool_widget_for_suffix(self, prop, idx, summary_widget):
        return self.generate_tool_widget(prop, idx, summary_widget)
    def tool_widget_for_skipCondition(self, prop, idx, summary_widget):
        return self.generate_tool_widget(prop, idx, summary_widget)
    def tool_widget_for_animation(self, prop, idx, summary_widget):
        return self.generate_tool_widget(prop, idx, summary_widget)
    def tool_widget_for_noInteraction(self, prop, idx, summary_widget):
        return self.generate_tool_widget(prop, idx, summary_widget)
    def make_top_bar(self):
        update_button = GimpUi.Button.new_from_icon_name(GimpUi.ICON_VIEW_REFRESH, 1) #Gtk.Button.new_with_label("Click Me")
        update_button.set_name("Update Layer")
        update_button.show()
        update_button.connect("clicked", self.update_button_action, self)
        image_name = Gtk.Label.new(f"<{self.tris_manager.image.get_name()}>")
        image_name.set_name("Descr Image Name")
        image_name.show()
        top_div = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 4)
        top_div.set_name("Div Top Bar")
        top_div.pack_start(update_button, False, False, 0)
        top_div.pack_start(image_name, True, True, 0)
        #top_div.set_center_widget(image_name)
        top_div.show()
        self.update_button = update_button
        self.image_name = image_name
        return top_div
    @staticmethod
    def update_button_action(button, self):
        self.tris_manager.update_current_layer()
        self.image_name.set_text(self.tris_manager.current_layer.get_name())


    