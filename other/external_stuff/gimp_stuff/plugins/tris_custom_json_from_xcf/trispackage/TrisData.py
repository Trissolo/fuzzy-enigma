# import gi
# gi.require_version("Gimp", "3.0")
# from gi.repository.Gimp import Parasite as GimpPara


class TrisData():
    def __init__(self, length):
        self.length = length
        self.final = [None] * length
        self.proposed = self.final.copy()
        
        #self[1] = 892
        
    
    def __getitem__(self, index):
        return self.proposed[index]
        
    def __setitem__(self, index, newvalue):
        self.proposed[index] = newvalue
    
    def __len__(self):
        return len(self.proposed)
        
    def proposal_accepted(self):
        type(self).set_from_array(self.proposed, self.final)
        
    def proposal_rejected(self):
        type(self).set_from_array(self.final, self.proposed)
    
    def info(self):
        print(f"{self.final=}")
        print(f"{self.proposed=}")
    
    @staticmethod
    def set_from_array(source, target):
        target.clear()
        target.extend(source)









    def absorb_parasite(self, parasite):
        data = type(self).para_data_to_ary(parasite.get_data())
        self.set_from_array(data)
    
    
    @staticmethod
    def ary_to_bytes(data):
        return (" ".join([str(el) for el in data])).encode('ascii')

    @staticmethod
    def para_data_to_ary(data):
        res_string = str(object=bytes(data), encoding='ascii')
        return [int(x) for x in res_string.split(" ")]