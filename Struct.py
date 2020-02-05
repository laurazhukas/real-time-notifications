# class used to convert dict returned from MongoDB into struct object
class Struct :
    def __init__(self, **entries):
        self.__dict__.update(entries)
