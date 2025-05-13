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
        self.set_from_array([None] * self.max_length)
        return self
    
    def has_a_number(self):
        return self.emu_number
    
    def has_a_varkind(self):
        return self.emu_variable
    
    def has_a_condition(self):
        return self.emu_condition
    
    def set_from_array(self, array):
        self.data.clear()
        self.data.extend(array)
        return self
    def set_at_zero(self, value):
        self.data[0] = value
        return self
    
    def set_at_one(self, value):
        if not self.has_a_number:
            self.data[1] = value
            return self
        
    def set_at_two(self, value):
        if self.has_a_condition:
            self.data[2] = value
            return self
    
    def get_at_zero(self):
        return self.data[0]
    
    def get_at_one(self):
        if not self.has_a_number:
            return self.data[1] 
        
    def get_at_two(self):
        if self.has_a_condition:
            return self.data[2]
    
    def is_valid(self):
        return not None in self.data
    
    @staticmethod
    def encode_utf8(data):
        #if type(data) is not list:
         #   data = [data]
        res = " ".join([str(el) for el in data])
        to_bytes = bytes(res.encode('utf-8'))
        return to_bytes
    
