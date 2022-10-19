class DataObject:
    def __init__(self):
        self.data = {}

    def set(self, field, value):
        self.data[field] = value

    def get(self, field):
        self.data.get(field)