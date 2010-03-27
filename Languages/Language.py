class RehearseTuple():
    def __init__(self, name, answer, table, scoretable):
        self.__name = name
        self.__answer = answer
        self.__table = table
        self.__scoretable = scoretable
        
        
    @property
    def name(self):
        return self.__name

    @property
    def answer(self):
        return self.__answer
    
    @property
    def table(self):
        return self.__table
    
    @property
    def scoretable(self):
        return self.__scoretable
