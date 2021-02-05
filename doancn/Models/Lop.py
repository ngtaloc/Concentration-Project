class Lop():

    def __init__(self, malop, tenlop):  # contructor
        self.__malop = malop
        self.__tenlop = tenlop

    # set Tên lớp
    def setTenlop(self, tenlop):
        self.__tenlop = tenlop

    # get Tên lớp
    def getTenLop(self):
        return self.__tenlop

    # get mã lớp
    def getMalop(self):
        return self.__malop
