from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets

import DataConn
from Controllers import XLDL

def loadDSLopHoc(TW_dsMonHoc):
    dsMonHoc = XLDL.xldl_MonHoc.layDSMonHoc()
    row = 0
    TW_dsMonHoc.setRowCount(len(dsMonHoc))

    for mh in dsMonHoc:
        TW_dsMonHoc.setItem(row, 0, QTableWidgetItem(mh.getMaMH()))
        TW_dsMonHoc.setItem(row, 1, QTableWidgetItem(mh.getTenMH()))
        TW_dsMonHoc.setItem(row, 2, QTableWidgetItem(str(mh.getSoTC())))
        row = row +1


def them(maMH, TenMH, soTC):
    conn = DataConn.DBConnet.getConnet()
    query = "INSERT INTO MonHoc VALUES ('"+maMH+"', N'"+TenMH+"', "+soTC+")"
    st = 'Thêm thành công !'
    try:
        conn.execute(query)
        conn.commit()
    except Exception as e:
        if str(e).find('PRIMARY KEY') !=-1:
            st = 'Mã môn học này đã có rồi.'
            print(e)
    conn.close()

    return st


def sua(maMH, tenMH, soTC):
    conn = DataConn.DBConnet.getConnet()
    query = " UPDATE MonHoc SET tenMH = N'"+tenMH+"' , sotinchi = "+soTC+" WHERE maMH = '"+maMH+"';"
    st = 'Sửa thành công !'
    try:
        conn.execute(query)
        conn.commit()
        print(query)
    except Exception as e:
        return e
    conn.close()

    return st

def xoa(maMH):
    conn = DataConn.DBConnet.getConnet()
    query = " DELETE FROM MonHoc WHERE maMH = '"+maMH+"';"
    st = 'Xóa thành công !'
    try:
        conn.execute(query)
        conn.commit()
        print(query)
    except Exception as e:
        return e
    conn.close()

    return st
