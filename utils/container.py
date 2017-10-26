class Container:
    def __init__(self):
        self.next_id = 0
        self.dic = {}

    def add_element_with_id(self, elem, elem_id):
        if elem_id not in self.dic:
            self.dic[elem_id] = elem
            self.next_id = elem_id + 1
        else:
            raise ValueError('Ids must be unique')




    def add_element(self, elem):
        self.add_element_with_id(elem, self.next_id)

    def __contains__(self, item):
        return item in self.dic