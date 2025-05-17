class _SharedContainer():
    def __init__(self):
        self.summary_widgets = []
        self.tool_widgets = []
        self.tris_data = []

    def add_summary(self, elem):
        self.summary_widgets.append(elem)

    def get_summary_by_idx(self, idx):
        return self.summary_widgets[idx]
    
    
    def add_tool(self, elem):
        self.tool_widgets.append(elem)
    
    def get_tool_by_idx(self, idx):
        return self.tool_widgets[idx]
    
    
    def add_tris_data(self, elem):
        self.tris_data.append(elem)
    
    def get_tris_data_by_idx(self, idx):
        return self.tris_data[idx]

tris_container = _SharedContainer()
