class MonHoc():

    def __init__(self, maMH, tenMH, soTC):  # contructor
        self.__maMH = maMH
        self.__tenMH = tenMH
        self.__soTC = soTC

    # set Tên môn học
    def setTenMH(self, tenmh):
        self.__tenMH = tenmh

    # get Tên Môn học
    def getTenMH(self):
        return self.__tenMH

    # set số tín chỉ
    def setSoTC(self, sotc):
        self.__soTC = sotc

    # get số tín chỉ
    def getSoTC(self):
        return self.__soTC

    # get Mã môn học
    def getMaMH(self):
        return self.__maMH
