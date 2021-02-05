class Giangvien():

    def __init__(self, maGV, tenGV):  # contructor
        self.__maGV = maGV
        self.__tenGV = tenGV
        self.__TDN = ""
        self.__MK = ""

    # get mã giảng viên
    def getMaGV(self):
        return self.__maGV

    # set/get Tên Giảng viên
    def setTenGV(self, tengv):
        self.__tenGV = tengv

    def getTenGV(self):
        return self.__tenGV

    # set/get Tên đăng nhập
    def setTDN(self, tdn):
        self.__TDN = tdn

    def getTDN(self):
        return self.__TDN

    # set/get Mật khẩu
    def setMK(self, mk):
        self.__TDN = mk

    def getMK(self):
        return self.__MK