from Models import MonHoc, GiangVien


class Lophoc ():
    def __init__(self, maLopH, maMh, maGV, siSi, tenlophoc, namhoc):  # contructor
        self.__maLopH = maLopH
        self.__maMH = maMh
        self.__maGV = maGV
        self.__SiSo = siSi
        self.__tenLH = tenlophoc
        self.__namHoc = namhoc

    # get Mã môn học
    def getMaLopH(self):
        return self.__maLopH
    
    # get Mã môn học
    def getMaMH(self):
        return self.__maMH

    #get mã giảng viên
    def getMaGV(self):
        return self.__maGV

    # set/get Sỉ số

    def setSiSo(self, ss):
        self.__SiSo = ss

    def getSiSo(self):
        return self.__SiSo

    # set/get tên lớp hoc

    def setTenLH(self, tenlh):
        self.__tenLH = tenlh

    def getTenLH(self):
        return self.__tenLH

 # set/get Năm học

    def setNamHoc(self, namhoc):
        self.__namHoc = namhoc

    def getNamHoc(self):
        return self.__namHoc

