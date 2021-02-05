class TKLHSinhvien():
    def __init__(self, masv, tensv, malop, gioitinh, vang):
        self.__masv = masv
        self.__tensv = tensv
        self.__malop = malop
        self.__gioitinh = gioitinh
        self.__vang = vang

    # mã sinh viên
    def getmaSV(self):
        return self.__masv

    # tên sinh viên
    def setTenSV(self, tensv):
        self.__tensv=tensv

    def getTenSV(self):
        return self.__tensv



    # mã lớp
    def setmalop(self, malop):
        self.__malop = malop

    def getmalop(self):
        return self.__malop

    #  giới tính
    def setgioitinh(self, gt):
        self.__gioitinh = gt

    def getgioitinh(self):
        return self.__gioitinh

    # Tổng Vắng
    def setVang(self, vang):
        self.__vang = vang

    def getVang(self):
        return self.__vang

