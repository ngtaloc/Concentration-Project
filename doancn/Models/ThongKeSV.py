class TKSinhvienLophoc():
    def __init__(self, malophoc, tenlop, tenmh,  vang, sobuoi):
        self.__malophoc = malophoc
        self.__tenlop = tenlop
        self.__tenmh = tenmh
        self.__vang = vang
        self.__sobuoi = sobuoi

    # mã lớp học
    def getMaLopHoc(self):
        return self.__malophoc

    # tên lớp học
    def setTenLop(self, tenlh):
        self.__tenlop=tenlh

    def getTenLop(self):
        return self.__tenlop


    #tên Môn học
    def setTenMH(self, tenmh):
        self.__tenmh=tenmh

    def getTenMH(self):
        return self.__tenmh

    # tên Tổng vắng
    def setTongVang(self, vang):
        self.__vang=vang

    def getTongVang(self):
        return self.__vang

    # tên Tổng số buổi học
    def setSobuoi(self, sobuoi):
        self.__sobuoi=sobuoi

    def getSobuoi(self):
        return self.__sobuoi



