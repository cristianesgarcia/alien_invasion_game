class Test:

    def __init__(self):
        self.__x = 10
    
    @property
    def x(self):
        """Get the current value of x"""
        return self.__x

myTest = Test()
print(myTest._Test__x)