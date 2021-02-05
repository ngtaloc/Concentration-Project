class Sinhvien():
    def __init__(self, masv, tensv,  gioitinh, diachi, vang):
        self.__masv = masv
        self.__tensv = tensv
        #self.__malop = maLop
        self.__gioitinh = gioitinh
        self.__diachi = diachi
        self.__vang = vang

    # mã sinh viên
    def getmaSV(self):
        return self.__masv

    # tên sinh viên
    def setTenSV(self, tensv):
        self.__tensv=tensv

    def getTenSV(self):
        return self.__tensv



    # tên địa chỉ
    def setdiachi(self, diachi):
        self.__diachi = diachi

    def getdiachi(self):
        return self.__diachi

    # tên giới tính
    def setgioitinh(self, gt):
        self.__gioitinh = gt

    def getgioitinh(self):
        return self.__gioitinh

    # Vắng
    def setVang(self, vang):
        self.__vang = vang

    def getVang(self):
        return self.__vang

