def elenca_figli(widget, lev = 1, idx = 0, lc = 1, hastrai = False, sp = "    ", hook = "╰╴", vpipe = "│"):
            if hasattr(widget, 'get_children'):
                gra = "└─" if (lc - idx) == 1 else "├─"
                indent = f"{sp * lev}" if not hastrai else f"{sp * (lev-1)}{vpipe}"
                print(f"{indent}{gra}{widget.get_name()}😫")
                chi = widget.get_children()
                lc = len(chi)
                for idx, elem in enumerate(chi):
                    elenca_figli(elem, lev + 1, idx, lc,((lc - idx) == 0), sp, hook, vpipe)
            else:
                print(f"{sp * (lev + 1)}└─{widget.get_name()}")

def build_node(name = "Some node"):
     return _Node(name)

class _Node:
    def __init__(self, name, neighbours = set()):
        self.name = name
        self.neighbours = neighbours
        self.isContainer = False
        self.level = 0
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def isContainer(self):
        return self._isContainer
    
    @isContainer.setter
    def isContainer(self, value):
        self._isContainer = value
    
    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value
        
#__all__ = ["build_node", "elenca_figli"]
