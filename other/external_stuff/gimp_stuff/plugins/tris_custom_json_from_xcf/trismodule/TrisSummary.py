import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .trisLabel import TrisLabel

from .generic_helpers import make_button, make_box, multipack
from .Necessary import Necessary

class TrisSummary(Necessary):
    def __init__(self, prop, idx):
        self.property = prop
        self.idx = idx
        self.parasite_data = None

        #First Label
        self.label_key = TrisLabel(f"{prop}:")
        self.label_key.set_xalign(0)
        self._show_off_json_key()

        #Second Label (current value)
        self.label_value = TrisLabel("----")
        self.label_value.set_xalign(0)
        #self.label_value.write(None, bgcolor=0x666666, monospace=True, pad=6)

        # First Button (open tools)
        self.button_a = make_button(GimpUi.ICON_MENU_RIGHT, f"Button_a {prop}", self.manifest_tool_widget)
        
        # Second Button (save the changes)
        self.button_b = make_button(GimpUi.ICON_DOCUMENT_SAVE, f"Button_b for saving: {prop}", self.save_prop_in_parasite)
        self.button_b.hide()

        # Box container
        div = make_box(True, 4, f"Div Left for{prop}")
        multipack(div, self.label_key, self.label_value, packing=True, spacing=2)
        multipack(div, self.button_a, self.button_b, from_end=True, packing=False, spacing=2)
        self.div = div

        #At first the save button is hidden
        self.button_b.hide()
        
        # (end TrisSummary init)
    
    def show(self):
        self.div.show()
        return self
    
    def hide(self):
        self.div.hide()
        return self
    
    def _show_off_json_key(self, use_bold = False, use_italic = False):
        self.label_key.write(text=None, color=0x989898, monospace=True, bold=use_bold, italic=use_italic, size=110)
        return self
    
    def _show_off_json_value(self, text = None, highlight = False):
        self.label_value.write(text=text, bgcolor=0x45ba76, size=116, pad=1, monospace=True) if highlight else self.label_value.write(text, size=116, pad=2, monospace=True)
        return self
    
    def labels_no_data(self):
        self._show_off_json_key()
        self._show_off_json_value()
        return self
    
    def labels_existing_data(self, text):
        self._show_off_json_key(use_bold=True)
        self._show_off_json_value(text)
        return self
    
    def labels_potential_data(self, text):
        self._show_off_json_key(use_italic=True)
        self._show_off_json_value(text, highlight=True)
        return self

    def receive_data(self, para_data):
        self.parasite_data = para_data
        parsed_text = self.parse_parasite_data(para_data)
        self.labels_potential_data(parsed_text)
        self.button_b.show()
        return self
    def hide_all_tools(self):
        for tool_widget in self.tool_widgets_ary:
            tool_widget.hide()
        return self
    def manifest_tool_widget(self, button):
        self.hide_all_tools()
        self.tool_widget_from_idx(self.idx).show()

    def introduce_hovernames(self, button):
        print("Called the method 'TrisSummary.introduce_hovernames', but is still incomplete.")
        print("INTRODUCE", self.idx, self.tool_widgets_ary[self.idx])
        twa = self.tool_widgets_ary
        if not twa[self.idx]:
            print("This method is WIP: widget not yet implemented :(")
            return False
        print("OK - showing the wanted widget.")
        twa[self.idx].show()
        #To Do: hide any other ToolWidget

    def refresh(self, parasite_list = None):
        para = self.current_layer.get_parasite(self.property)
        if para is None:
            self.labels_no_data()
        else:
            data = Necessary.grab_parasite_data(para)
            parsed_text = self.parse_parasite_data(data)
            self.labels_existing_data(parsed_text)
    def save_xcf(self):
        file = self.image.get_xcf_file()
        Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, self.image, self.image.get_xcf_file(), None)
        self.image.is_dirty()
        self.image.clean_all()
        return self
    def remove_parasite(self):
        if self.property in self.current_layer.get_parasite_list():
            print('(Removing old para...)')
            self.current_layer.detach_parasite(self.property)
        return self
    def add_parasite(self):
        print(f"Widget {self.property} writing '{self.parasite_data}'")
        d = Necessary.encode_data(self.parasite_data)#Gimp.PARASITE_PERSISTENT
        p = Gimp.Parasite.new(name=self.property, flags=Gimp.PARASITE_PERSISTENT, data=d)
        self.current_layer.attach_parasite(p)
        print(f"Parasite called '{p.get_name()}' has been attached")
        print(len(self.current_layer.get_parasite_list()))
        #self.save_xcf()
    def save_prop_in_parasite(self, button):
        print("Saving THIS:", self.parasite_data, self.parasite_data is not None)
        self.remove_parasite()
        self.add_parasite()
        self.button_b.hide()
    
    def parse_parasite_data(self, data):
        result = None
        if type(data) is int:
            result = self.gamedata["onHoverNames"][data]
        else:
            value_text = self.tool_widget_from_idx(self.idx).enum.get_corresponding(data[1])
            kind_text = ["BOOL", "CRUMBLE", "NIBBLE", "BYTE"][data[0]]
            result = f"{value_text} ({kind_text.capitalize()} #{data[1]})"
            if len(data) == 3:
                result = f"if {result} == {data[2]}"
        return result

        
    def set_labels_from_data(self):
        data = self.parasite_data
        if data is None:
            self.show_off_json_key()
            self.show_off_json_value()
            return True
        self.show_off_json_key(True)
        if data is int:
            self.show_off_json_value(self.gamedata["onHoverNames"][data], highlight=True)
            return
        var_value = self.tool_widget_from_idx(self.idx).enum.get_corresponding(data[1])
        var_kind = ["BOOL", "CRUMBLE", "NIBBLE", "BYTE"][data[0]]
        result = f"{var_value} ({var_kind}: {data[1]})"
        if len(data) == 3:
                result = f"if {result} == {data[2]}"
        self.show_off_json_value(result, highlight=True)
        return True

    # def determine_data(self, data = None):
    #     if data is None and self.parasite_data is None:
    #         return "----"
    #     data = self.parasite_data
    #     #assert data is not None, f"Message from Summart{self.property.capitalize()}: 'self.parasite_data' not yet assigned"
    #     result = None
    #     props_strings = self.gamedata["thingProps"]
    #     is_array = self.property == props_strings[1] or self.property == props_strings[2]
    #     if is_array:
    #         enustoca = self.tool_widget_from_idx(self.idx).enum
    #         var_value = enustoca.get_corresponding(data[1])
    #         var_kind = ["BOOL", "CRUMBLE", "NIBBLE", "BYTE"][data[0]]
    #         result = f"{var_value} ({var_kind}: {data[1]})"
    #         if len(data) == 3:
    #             result = f"if {result} == {data[2]}"
    #     else:
    #         result = self.gamedata["onHoverNames"][data]
    #     return result

