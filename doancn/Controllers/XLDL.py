from PyQt5.QtWidgets import QMessageBox

import DataConn as DT
from Models import Lop as L , MonHoc as MH, SinhVien as SV , LopHoc , NamHoc, ThongKeLH as tklh, ThongKeSV as tksv, GiangVien as gv


class xldl_NamHoc():
    @staticmethod
    def layDSNamHoc():
        try:
            danhSach = []
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()
            cur.execute("select * from NamHoc")
            for row in cur:
                danhSach.append(NamHoc.namHoc(row[0], row[1]))  # maNam, namhoc
            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()


class xldl_lop():
    @staticmethod
    def layDSLop():
        try:
            danhSach = []
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()
            cur.execute("select * from Lop")
            for row in cur:
                danhSach.append(L.Lop(row[0], row[1]))  # malop, tenlop
            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()


class xldl_MonHoc():
    @staticmethod
    def layDSMonHoc():
        try:
            danhSach = []
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()
            cur.execute("select * from Monhoc")

            for row in cur:

                danhSach.append(MH.MonHoc(row[0], row[1], row[2]))  # maMH, tenMH, soTC
            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()


class xldl_LopHoc():
    @staticmethod
    def layDSLopHoc(namhoc):
        try:
            danhSach = []
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()
            cur.execute("select maLopHoc , lophoc.maMH, maGV, siso ,maLopHoc+' '+tenMH as tenlophoc , nam from Monhoc, LopHoc where Monhoc.maMH=LopHoc.maMH and nam='"+namhoc+"'")
            print(cur)
            for row in cur:

                danhSach.append(LopHoc.Lophoc(row[0], row[1], row[2], row[3], row[4], row[5])) # maLopH, maMh, maGV, siSi, tenlophoc, namhoc)
            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()

    def layDSLopHoc_nam_gv(namhoc, magv):
        try:
            danhSach = []
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()
            cur.execute("select maLopHoc , lophoc.maMH, maGV, siso ,maLopHoc+' '+tenMH as tenlophoc , nam from Monhoc, LopHoc where Monhoc.maMH=LopHoc.maMH and nam='"+namhoc+"' and maGV='"+magv+"'")
            print(cur)
            for row in cur:

                danhSach.append(LopHoc.Lophoc(row[0], row[1], row[2], row[3], row[4], row[5])) # maLopH, maMh, maGV, siSi, tenlophoc, namhoc)
            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()

    def layThonTinLopHoc(malophoc):
        try:
            danhSach = []
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()
            cur.execute("SELECT TenLop, tenMH, tenGiangvien, SiSo FROM (LopHoc INNER JOIN Giangvien ON LopHoc.maGV=Giangvien.maGiangvien) inner join Monhoc on LopHoc.maMH=Monhoc.maMH WHERE maLopHoc='"+malophoc+"'")
            print(cur)

            for row in cur:
                danhSach.append(row[0]) # malop
                danhSach.append(row[1]) # ten lop
                danhSach.append(row[2]) # Tên gv
                danhSach.append(row[3]) #  siso
            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()

class xldl_SinhVien():
    @staticmethod
    def layDSsinhVien(malophoc, ngaydd):
        try:
            danhSach = []
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()

            #cur.execute("select sv.masv, tensv, gioitinh, diachi, dd.vang, dd.maLopHoc, ngayDD from sinhvien as sv inner join  DiemDanh as dd on sv.masv=dd.maSV where maLopHoc='"+malophoc+"'")
            query=("select sv.masv, tensv, gioitinh, diachi, "
                        "(select dd.vang from sinhvien as sv1 inner join  DiemDanh as dd on sv1.masv=dd.maSV where maLopHoc='"+malophoc+"' and ngayDD ='"+ngaydd+"' and dd.maSV=sv.masv)as vang "
                        "from sinhvien as sv inner join  CTlopHoc as ct on sv.masv=ct.maSV where maLopHoc='"+malophoc+"'")
            cur.execute(query)
            print(query)
            print(cur)
            for row in cur:

                vang = 'Vắng'
                if row[4]:
                    vang = 'Có'
                danhSach.append(SV.Sinhvien(row[0], row[1], row[2], row[3], vang)) # masv, tensv,  gioitinh, diachi, vắng
                #danhSach.append(dd.Diemdanh(row[5], row[0], row[6], row[4])) #malophoc, masv,  ngaydd, vang

            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()

    def layThonTinSinhVien(masv):
        try:
            danhSach = []
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()
            cur.execute("select masv, tensv, gioitinh, diachi from SinhVien where masv='"+masv+"'")
            print(cur)
            for row in cur:
                danhSach.append(row[0])  # masv
                danhSach.append(row[1])  # ten sv
                danhSach.append(row[2])  # gioi tinh
                danhSach.append(row[3])  # dia chi
            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()

class xldl_QLSinhVienLopHoc():
    @staticmethod
    def layDSsinhVien(malophoc):#lấy danh sách sinh viên theo mã lớp học (IS434A)
        try:
            danhSach = []
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()
            query=("select sv.masv, tensv, gioitinh, diachi from sinhvien as sv inner join  CTlopHoc as ct on sv.masv=ct.maSV where maLopHoc='"+malophoc+"'")
            cur.execute(query)
            for row in cur:
                danhSach.append(SV.Sinhvien(row[0], row[1], row[2], row[3], '')) # masv, tensv,  gioitinh, diachi, vắng
                #danhSach.append(dd.Diemdanh(row[5], row[0], row[6], row[4])) #malophoc, masv,  ngaydd, vang
            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()

    def layDSsinhVienLop(malop): # lấy ds sinh viên theo lớp (TPM2)
        try:
            danhSach = []
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()
            query=("select masv, tensv, gioitinh, diachi from sinhvien where maLop='"+malop+"'")
            cur.execute(query)
            for row in cur:
                danhSach.append(SV.Sinhvien(row[0], row[1], row[2], row[3], '')) # masv, tensv,  gioitinh, diachi, vắng

            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()

    def TimSV(tim): # lấy ds sinh viên theo lớp (TPM2)
        try:
            danhSach = []
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()
            query=("select masv, tensv, gioitinh, diachi from sinhvien where maLop like N'%"+tim+"%' or tensv like N'%"+tim+"%' or masv like N'%"+tim+"%'")
            cur.execute(query)
            for row in cur:
                danhSach.append(SV.Sinhvien(row[0], row[1], row[2], row[3], '')) # masv, tensv,  gioitinh, diachi, vắng

            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()


class xldl_ThongKe():
    @staticmethod
    def layDSsinhVien_lopHoc(malophoc):#lấy danh sách sinh viên theo mã lớp học (IS434A)
        try:
            danhSach = []
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()
            query=("select sv.masv, tensv, maLop, gioitinh , SUM(CASE WHEN vang=1 THEN 0 ELSE 1 END) AS TONG "
                   "from sinhvien as sv RIGHT join  DiemDanh as ct on sv.masv=ct.maSV "
                   "where maLopHoc='"+malophoc+"' group by sv.masv, tensv, maLop, gioitinh ORDER BY sv.masv")
            cur.execute(query)
            for row in cur:
                danhSach.append(tklh.TKLHSinhvien(row[0], row[1], row[2], row[3], row[4])) # masv, tensv, malop, gioitinh, Tongvang
            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()

    def layDSngayDD(malophoc):#lấy danh ngày điểm danh theo mã lớp học (IS434A)
        try:
            danhSach = []
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()
            query=("SELECT ngaydd from DiemDanh as dd, sinhvien as sv where dd.maSV=sv.masv and maLopHoc='"+malophoc+"' group by ngayDD")
            cur.execute(query)
            for row in cur:
                danhSach.append(row[0]) # ngày điểm danh
            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()

    def layDSvang(malophoc, ngaydd):  # lấy danh ngày điểm danh theo mã lớp học (IS434A)
        try:
            danhSach = {}
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()
            query = ("SELECT vang ,maSV from DiemDanh where  maLopHoc='"+malophoc+"'  and ngayDD='"+ngaydd+"' ORDER BY masv")
            cur.execute(query)
            for row in cur:
                danhSach[row[1]] = row[0]   # vắng của ngàydd
            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()

    def layDSLopHoc_SinhVien(maSV):  # lấy lớp học của sv có mã : maSV
        try:
            danhSach = []
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()
            query = ("select lh.maLopHoc, lh.TenLop, tenMH, SUM(CASE WHEN vang=1 THEN 0 ELSE 1 END) AS TONG  ,"
                     " (select  count(*) from DiemDanh where maSV='"+maSV+"' and DiemDanh.maLopHoc=lh.maLopHoc ) as soBuoi "
                     "from (LopHoc as lh left join monhoc as mh on lh.maMH=mh.maMH) RIGHT join  DiemDanh as dd on lh.maLopHoc=dd.maLopHoc "
                     "where dd.maSV='"+maSV+"' group by lh.maLopHoc, lh.TenLop,tenMH")
            cur.execute(query)
            for row in cur:
                danhSach.append(
                    tksv.TKSinhvienLophoc(row[0], row[1], row[2], row[3], row[4]))  # malophoc, tenlop, tenmh,  vang, số buổi học
            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()


class xldl_GiangVien():
    @staticmethod
    def layDSGiangVien():
        try:
            danhSach = []
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()
            cur.execute("select * from giangvien")
            for row in cur:
                danhSach.append(gv.Giangvien(row[0], row[1]))  #  maGV, tenGV
            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()


def layThonTinSinhVien(masv):
        try:
            danhSach = []
            conn = DT.DBConnet.getConnet()
            cur = conn.cursor()
            cur.execute("select masv, tensv, gioitinh, diachi from SinhVien where masv='"+masv+"'")
            print(cur)
            for row in cur:
                danhSach.append(row[0])  # masv
                danhSach.append(row[1])  # ten sv
                danhSach.append(row[2])  # gioi tinh
                danhSach.append(row[3])  # dia chi
            return danhSach

        except Exception as e:
            print(e)
        finally:
            conn.close()
