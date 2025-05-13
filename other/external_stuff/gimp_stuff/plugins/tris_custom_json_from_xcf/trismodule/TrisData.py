class TrisData():
    def __init__(self):
        self._data = []
        self._max_length = 0
        self.emu_number = False
        self.emu_variable = False
        self.emu_condition = False
    
    @property
    def data(self):
        return self._data
    
    @property
    def max_length(self):
        """Getter for the max_length property."""
        return self._max_length

    @max_length.setter
    def max_length(self, value):
        """Setter for the max_length property."""
        if 0 < value < 4:
            self._max_length = value
        else:
            raise ValueError("OutOfRange Error. 'TrisData.max_length' must be between 1 and 3")

    def set_behavior(self, behavior):
        self.max_length = behavior
        self.emu_number = behavior == 1
        self.emu_variable = behavior == 2
        self.emu_condition = behavior == 3
        return self.reset()
    
    def reset(self):
        self.data.clear()
        for x in range(0, self.max_length): self.data.append(None)
        return self
    
    def has_a_number(self):
        return self.emu_number
    
    def has_a_varkind(self):
        return self.emu_variable
    
    def has_a_condition(self):
        return self.emu_condition
    
