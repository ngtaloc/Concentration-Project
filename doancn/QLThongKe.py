import pylab

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
import xlwt

from xlwt import Workbook
#import xlsxwriter
import DataConn
from Controllers import XLDL

def loadDSLopHoc(TW_dstk, maLH):
    dsLopHoc = XLDL.xldl_ThongKe.layDSsinhVien_lopHoc(maLH.split(' ')[0])
    row = 0
    TW_dstk.setRowCount(len(dsLopHoc))

    for dssv in dsLopHoc:
        TW_dstk.setItem(row, 0, QTableWidgetItem(dssv.getmaSV()))
        TW_dstk.setItem(row, 1, QTableWidgetItem(dssv.getTenSV()))
        TW_dstk.setItem(row, 2, QTableWidgetItem(dssv.getmalop()))
        TW_dstk.setItem(row, 3, QTableWidgetItem(dssv.getgioitinh()))
        TW_dstk.setItem(row, 4, QTableWidgetItem(str(dssv.getVang())))
        row = row +1

    dsNgay = XLDL.xldl_ThongKe.layDSngayDD(maLH.split(' ')[0])
    column_index = TW_dstk.columnCount()
    TW_dstk.setColumnCount(column_index + len(dsNgay))
    for i in range(len(dsNgay)):
        dsNgay[i]= str(dsNgay[i])
        TW_dstk.setHorizontalHeaderItem(column_index + i, QTableWidgetItem(dsNgay[i]))
        print(dsNgay[i])

        dsvang = XLDL.xldl_ThongKe.layDSvang(maLH.split(' ')[0], dsNgay[i])
        rowVang = 0
        if len(dsvang) != 0:
            for dssvV in dsLopHoc:
                value = "Vắng"
                try:
                    if dsvang[dssvV.getmaSV()] == 1:
                        value = 'Có'
                except:
                    print()
                TW_dstk.setItem(rowVang, column_index + i, QTableWidgetItem(value))
                rowVang = rowVang+1

    rowTiLeHoc = 0
    for dssv in dsLopHoc: # in ra tỉ lệ đi học của sinh viên
        tileHoc = 100 -(dssv.getVang()/len(dsNgay) * 100)  #tỉ lệ đi học = 100 - (ngày vắn / số ngày dd * 100)
        print(dssv.getTenSV(),' - ', dssv.getVang(),' - ',len(dsNgay))
        TW_dstk.setItem(rowTiLeHoc, 5, QTableWidgetItem(str(round(tileHoc, 2))))
        rowTiLeHoc = rowTiLeHoc + 1
    return len(dsNgay)


def loadDSSinhVien(TW_dstk, maSV):
    dsLopHoc = XLDL.xldl_ThongKe.layDSLopHoc_SinhVien(maSV.split(' ')[0])
    row = 0
    TW_dstk.setRowCount(len(dsLopHoc))
    print("maSV= ", maSV)
    for dssv in dsLopHoc:
        TW_dstk.setItem(row, 0, QTableWidgetItem(dssv.getMaLopHoc()))
        TW_dstk.setItem(row, 1, QTableWidgetItem(dssv.getTenLop()))
        TW_dstk.setItem(row, 2, QTableWidgetItem(dssv.getTenMH()))
        TW_dstk.setItem(row, 3, QTableWidgetItem(str(dssv.getTongVang())))
        TW_dstk.setItem(row, 4, QTableWidgetItem(str(dssv.getSobuoi())))
        try:
            TW_dstk.setItem(row, 5, QTableWidgetItem(str(round(100-dssv.getTongVang()/dssv.getSobuoi()*100, 2))))#rà soát tt
        except:
            TW_dstk.setItem(row, 5, QTableWidgetItem(str(0)))  # rà soát tt
        row = row +1

def load_pie(TW_dstk, tru):
    sum = 0
    count = 0
    for row in range(TW_dstk.rowCount()):
        sum = sum + int(TW_dstk.item(row, int(tru)-1).text())
        count = count + 1

    sdd= int(TW_dstk.columnCount()) - int(tru)
    print(sdd)
    try:
        percent = (sum / (count*sdd)) * 100
    except:
        return "Chưa có sinh viên"
    percents = [percent , 100 - percent]
    programming =  ["Vắng: "+ str(round(percent,2)) +"%","Có mặt: "+ str(round(100-percent,2)) +"%"]
    explode = [0.1,0]
    pylab.pie(percents, labels=programming, explode= explode,)
    pylab.title("Biểu đồ tỉ lệ vắng học")
    pylab.show()


def load_pie_SV(TW_dstk):
    sum = 0
    soBuoi=0
    count = 0
    for row in range(TW_dstk.rowCount()):
        sum = sum + int(TW_dstk.item(row, 3).text())
        soBuoi = soBuoi + int(TW_dstk.item(row, 4).text())
        count = count + 1
    print(soBuoi)
    try:
        percent = (sum / soBuoi) * 100
    except:
        return "Chưa có sinh viên"
    percents = [percent , 100 - percent]
    programming =  ["Vắng: "+ str(round(percent,2)) +"%","Có mặt: "+ str(round(100-percent,2)) +"%"]
    explode = [0.1,0]
    pylab.pie(percents, labels=programming, explode= explode, shadow=True, startangle=45 )
    pylab.legend(title="Biểu đồ tỉ lệ vắng học",)
    pylab.show()


def xuat_bao_cao(TW_dstk, malophoc, nam):
    wb = Workbook()
    xlwt.add_palette_colour("custom_colour", 0x21)
    wb.set_colour_RGB(0x21, 251, 228, 228)
    sheet = wb.add_sheet('sheet 1')
    style = xlwt.easyxf('font: bold off, color black;\
                         borders: top_color black, bottom_color black, right_color black, left_color black,\
                                  left thin, right thin, top thin, bottom thin;\
                         pattern: pattern solid, fore_color white;')
    style1 = xlwt.easyxf('font: bold on, color black, height 260;\
                            borders: top_color black, bottom_color black, right_color black, left_color black,\
                                     left thin, right thin, top thin, bottom thin;\
                            pattern: pattern solid,  fore_color custom_colour;\
                          align: vertical center, horizontal center;' )

    style2 = xlwt.easyxf('font: bold on, color black;\
                         borders: top_color black, bottom_color black, right_color black, left_color black,\
                                  left thin, right thin, top thin, bottom thin;\
                         pattern: pattern solid, fore_color yellow;')
    style3 = xlwt.easyxf('font: bold on, color black;\
                         borders: top_color black, bottom_color black, right_color black, left_color black,\
                                  left thin, right thin, top thin, bottom thin;\
                         pattern: pattern solid, fore_color white;')
    cot = 5
    hang = 1
    ttlophoc = XLDL.xldl_LopHoc.layThonTinLopHoc(malophoc.split(' ')[0])
    # write_merge(top_row, bottom_row, left_col , right_col)
    sheet.write_merge(0, 1, 1, 3, "BÁO CÁO THỐNG KÊ ĐIỂM DANH LỚP HỌC", style1)
    sheet.write(0, 6, "Năm: "+ nam)
    sheet.write_merge(2, 2, 0, 1, "Mã lớp học: "+ttlophoc[0], style2)
    sheet.write_merge(2, 2, 2, 3, "Tên lớp học: "+ttlophoc[1], style2)
    sheet.write_merge(2, 2, 4, 6, "Tên giảng viên: "+ttlophoc[2], style2)
    sheet.write_merge(2, 2, 7, 7, "Sỉ số: "+ str(ttlophoc[3]), style2)
    sum = 0
    for row in range(TW_dstk.rowCount()):
        sum = sum + int(TW_dstk.item(row, 4).text())
    sheet.write_merge(2, 2, 8, 9, "Tổng vắng: " + str(sum), style2)

    heder= ["STT", "Mã sinh viên", "Tên sinh viên", "Lớp hinh hoạt", "giới tính", "Tổng vắng", "Tỉ lệ đi học(%)"]
    for i in range(len(heder)): # ghi các herder
        cwidth = sheet.col(i).width  # lấy độ rộng hiện tại của column
        if (len(str(heder[i])) * 367) > cwidth:
            sheet.col(i).width = (len(str(heder[i])) * 367)
        sheet.write(4, 0 + i, str(heder[i]), style3)

    dsNgay = XLDL.xldl_ThongKe.layDSngayDD(malophoc.split(' ')[0])
    for i in range(len(dsNgay)): # ghi các cột ngày điểm danh
        cwidth = sheet.col(7 + i).width  # lấy độ rộng hiện tại của column
        if (len(str(dsNgay[i])) * 367) > cwidth:
            sheet.col(7 + i ).width = (len(str(dsNgay[i])) * 367)
        sheet.write(4, 7 + i, str(dsNgay[i]), style3)

    for row in range(TW_dstk.rowCount()):
        sheet.write(cot + row, 0, row + 1, style)
        for col in range(TW_dstk.columnCount()):
            # auto chỉnh size của cột
            cwidth = sheet.col(col).width # lấy độ rộng hiện tại của column
            if (len(TW_dstk.item(row, col).text()) * 367) > cwidth:
                sheet.col(col+1).width = (len(TW_dstk.item(row,col).text()) * 367)

            if col==4:
                sheet.write(cot+row, hang+col, int(TW_dstk.item(row,col).text()),style)
            elif col==5:
                sheet.write(cot + row, hang + col, float(TW_dstk.item(row, col).text()), style)
            else:
                sheet.write(cot+row, hang+col, TW_dstk.item(row,col).text(),style)

    wb.save('bao_cao_lopHoc_'+malophoc+'.xls')


def xuat_bao_cao_SV(TW_dstk, masv):
    wb = Workbook()
    xlwt.add_palette_colour("custom_colour", 0x21)
    wb.set_colour_RGB(0x21, 251, 228, 228)
    sheet = wb.add_sheet('sheet 1')
    style = xlwt.easyxf('font: bold off, color black;\
                            borders: top_color black, bottom_color black, right_color black, left_color black,\
                                     left thin, right thin, top thin, bottom thin;\
                            pattern: pattern solid, fore_color white;')
    style1 = xlwt.easyxf('font: bold on, color black, height 260;\
                               borders: top_color black, bottom_color black, right_color black, left_color black,\
                                        left thin, right thin, top thin, bottom thin;\
                               pattern: pattern solid,  fore_color custom_colour;\
                             align: vertical center, horizontal center;')

    style2 = xlwt.easyxf('font: bold on, color black;\
                            borders: top_color black, bottom_color black, right_color black, left_color black,\
                                     left thin, right thin, top thin, bottom thin;\
                            pattern: pattern solid, fore_color yellow;')
    style3 = xlwt.easyxf('font: bold on, color black;\
                            borders: top_color black, bottom_color black, right_color black, left_color black,\
                                     left thin, right thin, top thin, bottom thin;\
                            pattern: pattern solid, fore_color white;')
    cot = 5
    hang = 1
    ttSinhVien = XLDL.xldl_SinhVien.layThonTinSinhVien(masv.split(' ')[0])
    sheet.write_merge(0, 1, 1, 3, "BÁO CÁO THỐNG KÊ ĐIỂM DANH", style1)
    sheet.write_merge(2, 2, 0, 1, "Mã sinh viên: "+ttSinhVien[0], style2)
    sheet.write_merge(2, 2, 2, 4, "Họ và tên: "+ttSinhVien[1], style2)
    sheet.write_merge(2, 2, 5, 6, "Giới tính: "+ttSinhVien[2], style2)
    sheet.write_merge(2, 2, 7, 8, "Địa chỉ: "+ str(ttSinhVien[3]), style2)

    sum = 0
    for row in range(TW_dstk.rowCount()):
        sum = sum + int(TW_dstk.item(row, 3).text())
    sheet.write_merge(2, 2, 9, 10, "Tổng vắng: " + str(sum), style2)

    heder = ["STT", "Mã lớp học", "Tên lớp học", "Tên môn học", "Tổng vắng", "Số buổi học", "Tỉ lệ đi học(%)"]
    for i in range(len(heder)):  # ghi các herder
        cwidth = sheet.col(i).width  # lấy độ rộng hiện tại của column
        if (len(str(heder[i])) * 367) > cwidth:
            sheet.col(i).width = (len(str(heder[i])) * 367)
        sheet.write(4, 0 + i, str(heder[i]), style3)

    for row in range(TW_dstk.rowCount()):
        sheet.write(cot + row, 0, row + 1, style)
        for col in range(TW_dstk.columnCount()):
            # auto chỉnh size của cột
            cwidth = sheet.col(col).width # lấy độ rộng hiện tại của column
            if (len(TW_dstk.item(row,col).text()) * 367) > cwidth:
                sheet.col(col+1).width = (len(TW_dstk.item(row, col).text()) * 367)
            if col == 4 or col == 3:
                sheet.write(cot + row, hang + col, int(TW_dstk.item(row, col).text()), style)
            elif col == 5:
                sheet.write(cot + row, hang + col, float(TW_dstk.item(row, col).text()), style)
            else:
                sheet.write(cot + row, hang + col, TW_dstk.item(row, col).text(), style)
    wb.save('bao_cao_SinhVien_'+masv+'.xls')