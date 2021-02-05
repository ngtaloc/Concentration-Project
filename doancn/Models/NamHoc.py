class namHoc():
    def __init__(self, maNam, namhoc):  # contructor
        self.__maNam = maNam
        self.__namHoc = namhoc

    # get Mã môn học
    def getMaNamhoc(self):
        return self.__maNam

    def setNamHoc(self, namhoc):
        self.__namHoc = namhoc

    def getNamHoc(self):
        return self.__namHoc
