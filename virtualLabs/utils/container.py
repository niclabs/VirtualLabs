class Container:
    """ Class that encapsulates the behaviour behind a dictionary with unique ids that must be automatically generated
    if none is give.
    Attributes:
        next_id(int): Next available id to assign
        dic(dict): Dictionary relating id and object
    """
    def __init__(self):
        self.next_id = 0
        self.dic = {}

    def add_element_with_id(self, elem, elem_id):
        """ Adds an element with an assigned id. Updates next_id as necessary.
        :param elem: Element to add
        :param elem_id: Id of the element to assign
        """
        if elem_id not in self.dic:
            self.dic[elem_id] = elem
            self.next_id = elem_id + 1
        else:
            raise ValueError('Ids must be unique')

    def add_element(self, elem):
        """ Adds an element without id
        :param elem: Element to add
        """
        self.add_element_with_id(elem, self.next_id)

    def __contains__(self, item):
        """
        :param item: Item to check
        :return: Whether the element exists or not
        """
        return item in self.dic

    def get_ids(self):
        """
        :return: All ids assigned
        """
        return self.dic.keys()

    def get_dict(self):
        """
        :return: Dictionary with items and ids
        """
        return self.dic