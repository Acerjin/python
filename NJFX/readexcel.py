#!/usr/bin/env python
# -*- coding: utf-8 -*-
def readexcel(wb,startr,endc,*args,**kwargs): #对合并的列进行检测并处理。
    table = wb.sheet_by_index(0)
    nrows = table.nrows 
    tuprow =()
    datalist = []
    for n in range(startr,nrows):
        if table.cell(n,0).value != "":
            rownum = n
        for c in range(0,endc):
            if table.cell(n,0).value =="":
                celldata = table.cell(rownum,0).value
            celldata = table.cell(n,c).value
            celldatatup = (celldata,)
            tuprow +=celldatatup
        datalist.append(tuprow)
    print (datalist)
    return datalist
    