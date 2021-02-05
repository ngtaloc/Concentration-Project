class Diemdanh():
    def __init__(self, malophoc, masv,  ngaydd, vang, ghichu):
        self.__malophoc = malophoc
        self.__masv = masv
        self.__ngaydd = ngaydd
        self.__vang = vang
        self.__ghichu = ghichu

    # mã sinh viên
    def getmalophoc(self):
        return self.__malophoc

    # mã sinh viên
    def getmaSV(self):
        return self.__masv

    # tên sinh viên
    def setNgaydd(self, ngaydd):
        self.__ngaydd=ngaydd

    def getNgaydd(self):
        return self.__ngaydd


    # Vắng
    def setVang(self, vang):
        self.__vang = vang

    def getVang(self):
        return self.__vang

    # Ghi chú
    def setGhichu(self, gc):
        self.__ghichu = gc

    def getGhichu(self):
        return self.__ghichu


