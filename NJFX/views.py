# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os 
from _ast import Pass
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NJ.settings") 
import django

if django.VERSION >= (1, 7):#自动判断版本
    django.setup()


import xlrd,xlwt
import re
import io
import math
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.http import StreamingHttpResponse
from .models import *
import datetime
from django.utils import timezone
from datetime import timedelta
from django.db import connection,transaction
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.

def readexcel(wb,startr,endc,**kwargs): #对合并的列进行检测并处理,对第一列格式为日期进行处理，其它列暂不处理。
    table = wb.sheet_by_index(0)
    nrows = table.nrows 
    tuprow =()
    datalist = []
    if 'startc' not in kwargs.keys():
        startc = 0
    else:
        startc = kwargs['startc']
    for n in range(startr,nrows): 
        tuprow =()
        if table.cell(n,0).value != "":
            if table.cell(n, 0).ctype == 3: # 3 means 'xldate' , 1 means 'text'
                ms_date_number = table.cell(n,0).value # Correct option 2                        
                year, month, day, hour, minute, second = xlrd.xldate_as_tuple(ms_date_number,wb.datemode)
                py_date = datetime.datetime(year, month, day)
                celldatatemp = str(py_date)[0:10]
            else:
                celldatatemp= table.cell(n,0).value
        for c in range(startc,endc):
            if c==0 and table.cell(n,c).value =="":
                celldata = celldatatemp
            elif c==0 and table.cell(n, 0).ctype == 3 and table.cell(n,0).value !="": # 3 means 'xldate' , 1 means 'text'
                ms_date_number = table.cell(n,0).value # Correct option 2                        
                year, month, day, hour, minute, second = xlrd.xldate_as_tuple(ms_date_number,wb.datemode)
                py_date = datetime.datetime(year, month, day)
                celldatatemp = str(py_date)[0:10]                 
                celldata = celldatatemp
            else:
                celldata = table.cell(n,c).value
            celldatatup = (celldata,)
            tuprow +=celldatatup
        datalist.append(tuprow)
    return datalist

@login_required
def index(request,):
    username = request.user.username
    now = datetime.datetime.now()
    newnow = now.strftime("%Y-%m-%d")
    addday = timedelta(days=30)
    newrq = (now+addday).strftime("%Y-%m-%d")
    cursor1 = connection.cursor()
    #cursor.execute("select a.id,b.zhmc,c.pz pz,mc,je,round(a.je*100/b.zhje,2) zhzb,ifnull(rzzt,''),ifnull(ztpj,''),ifnull(zxpj,''),ifnull(qx,''),ifnull(syl,''),pzrq,dqrq,ifnull(synx,''),ifnull(lshzj,''),(case when a.dqrq <%s  then '1' else  '0' end ) ifgq,by1 from njfx_wdcp a,njfx_zh b,njfx_pz c where a.zhmc_id=b.id and a.pz_id=c.id and a.dqrq >%s",[newrq,newnow])
    cursor1.execute("select a.id,b.zhmc,c.pz pz,mc,je,round(a.je*100/b.zhje,2) zhzb,rzzt,ztpj,zxpj,qx,syl,pzrq,dqrq,synx,lshzj,(case when a.dqrq <%s  then '1' else  '0' end ) ifgq,by1,case  when sfgq='1' then '提前到期' else  '' end as sfgq from njfx_wdcp a,njfx_njzh b,njfx_pz c where a.zhmc_id=b.id and a.pz_id=c.id and a.dqrq >%s",[newrq,newnow])
    wdcp = cursor1.fetchall()
    cursor1.close()
    cursor2 = connection.cursor()
    cursor2.execute("select count(id) gqcount from njfx_wdcp where dqrq < %s and dqrq > %s",[newrq,newnow])
    gqcount = cursor2.fetchall()
    gc = gqcount[0][0]
    cursor2.close()
    return render_to_response('index.html', {'wdcp':wdcp,'gqcount':gc,'username':username})
@login_required
def hz(request):
    username = request.user.username
    now = datetime.datetime.now()
    newnow = now.strftime("%Y-%m-%d")
    #各有效组合的总金额
    cursor1 = connection.cursor()
    cursor1.execute('select round(sum(b.zhje),2) zh from njfx_njzh b where b.id in (select zhmc_id from njfx_wdcp a where a.dqrq>%s )',[newnow])
    zh_temp = cursor1.fetchone()
    cursor1.close() 
    zh = zh_temp[0]
    # 各组合所占比例
    cursor2 = connection.cursor()
    cursor2.execute('select b.zhmc,sum(a.je) hzje, round(sum(a.je)*100/%s,2) zhzb,sum(a.lshzj) hzlshzj from  njfx_wdcp a,njfx_njzh b where  a.dqrq>%s and b.id=a.zhmc_id group by b.zhmc',[zh,newnow])
    zhhz = cursor2.fetchall()
    cursor2.close()
    #各品种所占比例
    cursor3  = connection.cursor()
    cursor3.execute('select b.pz,sum(a.je) hzje,round(sum(a.je)*100/%s,2) zhzb,sum(lshzj) hzlshzj from njfx_wdcp a,njfx_pz b where a.pz_id=b.id and  dqrq > %s group by b.pz ',[zh,newnow])
    pzhz =  cursor3.fetchall()
    cursor3.close()
    return render_to_response('hz.html',{'zhhz':zhhz,'pzhz':pzhz,'username':username})
#def excel(request):
    #data= xlrd.open_workbook('media/1.xls') #打开文件
    #table = data.sheet_by_index(0) #获取工作表
    #nrows = table.nrows #行数
    #ncols = table.ncols #列数
    #colnames =  table.row_values(2)
    #sheetdata =[]
    #for r in xrange(0,nrows):
        #sheetdata.append(table.row_values(r))
    #return render_to_response('njtzfx.html',{'colnames':sheetdata})
@login_required
def data_import(request):  
    username = request.user.username
    if request.method == 'POST':  
        file_obj = request.FILES.getlist('upfile', None)        
        if file_obj == None:
            return HttpResponse('xxx')
        else:   
            #fname= file_obj.name
            cursor1 = connection.cursor() 
            b1= '归因分析表'
            b2= '资产分布表'
            b3='资产情况表'
            b4='日均持仓'
            b5='TA'
            b6='两费'
            b7='净值'            
            errorrow=[]
            fnamelist =[]
            errorfnamelist = []
            for f in file_obj:
                settings.K += 1
                datalist=[]
                fname = f.name
                fnamelist.append(fname)
                blx1 = re.findall(b1, fname) # 表类型判断
                blx2 = re.findall(b2, fname)
                blx3 = re.findall(b3, fname)
                blx4 = re.findall(b4, fname)
                blx5 = re.findall(b5, fname)
                blx6 = re.findall(b6, fname)
                blx7 = re.findall(b7, fname)
                wb = xlrd.open_workbook(filename=None,file_contents=f.read())
                table = wb.sheet_by_index(0)
                now = datetime.datetime.now()
                import_time = str(now)[:-7]
                headtup = (import_time,)
                if blx1:   # 归因分析表
                    #strsql = 'insert into NJFX_GYFX(drrq,ksrq,jsrq,zhmc,zclb,zcmc,sye1_bqlj,sye1_bqsyzb,sye1_bnlj,sye1_bnsyzb,sye2_bqlj,sye2_bnlj,tzsyl_bqlj,tzsyl_bnlj) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
                    strsql = 'insert into NJFX_GYFX(drrq,ksrq,jsrq,zhmc,zclb,zcmc,sye1_bqlj,sye1_bqsyzb,sye1_bnlj,sye1_bnsyzb,sye2_bqlj,sye2_bnlj,tzsyl_bqlj,tzsyl_bnlj) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

                    data1 = readexcel(wb,4,10)
                    rq= table.cell(1,3).value
                    ksrq = rq[0:11]
                    jsrq = rq[-11:]
                    zhmc = table.cell(1,6).value
                    tup1 =(ksrq,jsrq,zhmc,)
                    headtup +=tup1
                elif blx2:  #资产分布表
                    strsql = 'insert into NJFX_zcfbb(drrq,rq, zhmc, zclb, zcmc, sz, zjzcbl) values(%s,%s,%s,%s,%s,%s,%s)' 
                    data1 = readexcel(wb,3,4)
                    rq= table.cell(1,0).value
                    zhmc = table.cell(1,1).value
                    tup1 =(rq,zhmc,)
                    headtup +=tup1                    
                elif blx3:  #资产情况表
                    strsql = 'insert into NJFX_zcqkb(drrq,rq,tzzhdm, zhmc,dwjz, stzcjz, zcfe, wtje, jsy) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    data1 = readexcel(wb,4,8)
                elif blx4: #日均持仓表
                    strsql = 'insert into NJFX_ZCFBBrjcc(drrq,ksrq, jsrq, zhmc, zclb, zcmc, rjcccb, rjccye) values(%s,%s,%s,%s,%s,%s,%s,%s)'  
                    data1 = readexcel(wb,5,4)
                    rqzhmc= table.cell(2,0).value
                    ksrq = rqzhmc[0:11]
                    jsrq = rqzhmc[12:24]
                    zhmc=rqzhmc.split(' ')[1].split('_')[1][0:7]
                    tup1 =(ksrq,jsrq,zhmc,)
                    headtup +=tup1   
                elif blx5: #TA数据表
                    strsql = 'insert into njfx_ta  (drrq,rq,zhmc, bz, slje,jzrq, xspzrq) values(%s,%s,%s,%s,%s,%s,%s)' 
                    data1 = readexcel(wb,1,7,startc=1)
                elif blx6: #资产净值及收益率表
                    strsql = 'insert into njfx_syl  (drrq,rq, zhmc, zh1zc, zh2zc, zh3zc, zh4zc, zhhj, tabd, tabdje, bdhzhhj, syl) values  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    data1 = readexcel(wb, 1, 11) 
                elif blx7: #当期资产净值浏览表
                    strsql = 'insert into njfx_zcjz  (rq, zh, slje, drrq) values (%s,%s,%s,%s)' 
                    data1 = readexcel(wb, 1, 3)
            #合并导入日期，日期，组合名称
                for d in range(len(data1)):
                    data1[d]= headtup+data1[d]
                    datalist.append(data1[d])
                #--####################
                for x in range(0,len(datalist)):
                    print (x,':',datalist[x])
                for m in datalist:
                    errorinfo = []
                    try:
                        cursor1.execute(strsql,m)
                        print ('ok')
                    except Exception as error:
                        errorinfo = [fname,m,str(error)[:str(error).index(':')]]
                        errorfnamelist.append(errorinfo)
                        
                    finally:
                        sql1 =''                   
        cursor1.close() 
        sql1 = '' 
        return render_to_response('sjdr.html', {'errorrow':errorrow,'errorfname':errorfnamelist,'username':username,'filename':fnamelist})         
            #return HttpResponseRedirect('/tghsj/zcqkb/?rq='+rq)
    else:
        return render_to_response('sjdr.html', {})
def uploadpro(request):
    return HttpResponse(settings.K)
@login_required
def tghsj(request):
    username = request.user.username
    rq = request.GET.get('rq') 
    zh = request.GET.get('zh')
    rq2= request.GET.get('rq2')
    blx = request.GET.get('blx')
    page = request.GET.get('page')
    if page is None:
        trnum = 0
    else:
        trnum = (int(page) - 1) * 30
    #print type(rq),'11',type(blx),rq ,blx[0][0]   
    cursorsj = connection.cursor()
    cursorrq = connection.cursor()
    cursorzh = connection.cursor()
    sj =''
    rqlist = ''
    zhlist=''
    sqlrq = ''
    sqlzh = ''
    sqlbdrq=''

    print (trnum)
    if zh is None or zh=='ALL':
        zh = 'ALL'
        sqlzh = '1=1'
    else:
        sqlzh = 'zhmc=\''+str(zh)+'\''
    if rq is None or rq=='ALL':
        sqlrq = '1=1'
        rq= 'ALL'
    elif blx=='2' or blx=='4':
        sqlrq = 'jsrq=\''+str(rq)+'\'' 
    else:
        sqlrq = 't1.rq=\''+str(rq)+'\''
        sqlbdrq = 't1.rq<\''+str(rq)+'\''
    if blx[0][0] =='1':#资产情况表
        cursorrq.execute('select distinct(rq) from njfx_zcqkb t ')
        cursorzh.execute('select distinct(zhmc) from njfx_zcqkb t')
        rqlist = cursorrq.fetchall()
        zhlist = cursorzh.fetchall()
        sql = 'select rq, tzzhdm, zhmc, dwjz, stzcjz, zcfe, wtje, jsy, drrq from njfx_zcqkb t1 where '+sqlrq+' and '+ sqlzh+' order by rq desc '
        #cursorsj.execute('select rq, tzzhdm, zhmc, dwjz, stzcjz, zcfe, wtje, jsy, drrq from njfx_zcqkb where %s and %s order by rq desc ',[sqlrq,sqlzh]) 
        cursorsj.execute(sql)
        sj = cursorsj.fetchall()
    elif blx[0][0] =='2':# 归因分析
        cursorrq = connection.cursor()
        cursorrq.execute('select distinct(jsrq) from NJFX_GYFX t order by jsrq desc')
        cursorzh.execute('select distinct(zhmc) from NJFX_GYFX t ')
        zhlist =cursorzh.fetchall()
        rqlist = cursorrq.fetchall()
        cursorrq.close()
        sql = 'select  ksrq, jsrq,zhmc, zclb, zcmc, sye1_bqlj, round(sye1_bqsyzb,2) ,sye1_bnlj, round(sye1_bnsyzb,2), sye2_bqlj, sye2_bnlj, round(tzsyl_bqlj,2), round(tzsyl_bnlj,2), drrq from njfx_gyfx t1 where '+sqlrq+' and '+ sqlzh+' order by jsrq desc '
        #cursorsj.execute('select  ksrq, jsrq,zh, zclb, zcmc, sye1_bqlj, round(sye1_bqsyzb,2) ,sye1_bnlj, round(sye1_bnsyzb,2), sye2_bqlj, sye2_bnlj, round(tzsyl_bqlj,2), round(tzsyl_bnlj,2), drrq from njfx_gyfx where jsrq= %s order by jsrq desc',[rq])
       
        cursorsj.execute(sql)
        sj = cursorsj.fetchall()
    elif blx[0][0] =='3':#资产分布
        cursorrq = connection.cursor()
        cursorrq.execute('select distinct(rq) from njfx_zcfbb t order by rq desc')
        rqlist = cursorrq.fetchall()
        cursorzh.execute('select distinct(zhmc) from njfx_zcfbb ')
        zhlist = cursorzh.fetchall()
        cursorrq.close()
        sql = 'select  rq, zhmc, zclb, zcmc, sz, zjzcbl,  drrq from njfx_zcfbb t1 where '+sqlrq+' and '+ sqlzh+' order by rq desc '
        cursorsj.execute(sql)
        sj = cursorsj.fetchall()
    elif blx[0][0] =='4':#日均持仓分析
        cursorrq = connection.cursor()
        cursorrq.execute('select distinct(jsrq) from njfx_zcfbbrjcc t order by jsrq desc')
        rqlist = cursorrq.fetchall()
        cursorzh.execute('select distinct(zhmc) from njfx_zcfbbrjcc ')
        zhlist = cursorzh.fetchall()        
        cursorrq.close()
        sql = 'select  ksrq, jsrq, zhmc, zclb, zcmc, rjcccb, rjccye, drrq from  njfx_zcfbbrjcc t1 where '+sqlrq+' and '+ sqlzh+' order by jsrq desc '
        cursorsj.execute(sql)
        sj = cursorsj.fetchall()
    elif blx[0][0] =='5': #收入分析
        cursorsj.execute('select jsrq, zhmc, xm, zqnhg, qthbl, ldxxj, xyck, gz, qyz, kzz, llcp, qtgdl, gdlxj, gp, qtqyl, qylxj, hj from njfx_srfx t1 order by jsrq desc ,zhmc,xm')
        sj = cursorsj.fetchall()
    elif blx[0][0] =='6': #投资分析
        cursorrq = connection.cursor()
        cursorrq.execute('select distinct(rq) from njfx_tzqkfx t ')
        rqlist = cursorrq.fetchall()
        #if rq is None:
            #rq = rqlist[0][0]
        cursorrq.close()
        sql = "select rq,zhmc, wtje, yhck, zqnhg, qthbjj, hblxj, hblzb, hblsr, hblsrzb, xdg, wcp, qyz, qtgdl, gdlxj, gdlzb, gdlsr, gdlsrzb, gp, gpjj, qylxj, qylzb, gpzb, qylsr, qylsrzb, stzcjz, srhj, sndljlr, bnlr, ljlr, sndwjz, sndtzhdwjz, sqdwjz, dwjz, bqjzzjbd, bnsyl, jz, ljpm, bnpm from njfx_tzqkfx t1 where "+sqlrq
        sql += """ union SELECT distinct t1.rq,'上期累计' as zhmc,t2.wtje, t2.yhck, t2.zqnhg, t2.qthbjj, t2.hblxj, t2.hblzb, t2.hblsr, t2.hblsrzb, t2.xdg, t2.wcp, t2.qyz, t2.qtgdl, t2.gdlxj, t2.gdlzb, t2.gdlsr, t2.gdlsrzb, t2.gp, t2.gpjj, t2.qylxj, t2.qylzb, t2.gpzb, t2.qylsr, t2.qylsrzb, t2.stzcjz, t2.srhj, t2.sndljlr, t2.bnlr, t2.ljlr, t2.sndwjz, t2.sndtzhdwjz, t2.sqdwjz, t2.dwjz, t2.bqjzzjbd, t2.bnsyl, t2.jz, t2.ljpm, t2.bnpm FROM njfx_tzqkfx t1 
left join 
(select * from njfx_tzqkfx where zhmc='本期累计') t2
on t2.rq in (select max(rq) from njfx_tzqkfx where zhmc='本期累计' and rq<t1.rq)
 where t1.zhmc='本期累计'and """ +sqlrq
        if rq != None and rq!='ALL':
            sql +=""" union select n1.rq,'本期增减变动' as zhmc,
            round(n1.wtje-n2.wtje,4) as wtje,
            round(n1.yhck-n2.yhck,4) as yhck,
            round(n1.zqnhg-n2.zqnhg,4) as zqnhg,
            round(n1.qthbjj-n2.qthbjj,4) as qthbjj,
            round(n1.hblxj-n2.hblxj,4) as hblxj,
            round(n1.hblzb-n2.hblzb,4) as hblzb,
            round(n1.hblsr-n2.hblsr,4) as hblsr,
            round(n1.hblsrzb-n2.hblsrzb,4) as hblsrzb,
            round(n1.xdg-n2.xdg,4) as xdg,
            round(n1.wcp-n2.wcp,4) as wcp,
            round(n1.qyz-n2.qyz,4) as qyz,
            round(n1.qtgdl-n2.qtgdl,4) as qtgdl,
            round(n1.gdlxj-n2.gdlxj,4) as gdlxj,
            round(n1.gdlzb-n2.gdlzb,4) as gdlzb,
            round(n1.gdlsr-n2.gdlsr,4) as gdlsr,
            round(n1.gdlsrzb-n2.gdlsrzb,4) as gdlsrzb,
            round(n1.gp-n2.gp,4) as gp,
            round(n1.gpjj-n2.gpjj,4) as gpjj,
            round(n1.qylxj-n2.qylxj,4) as qylxj,
            round(n1.qylzb-n2.qylzb,4) as qylzb,
            round(n1.gpzb-n2.gpzb,4) as gpzb,
            round(n1.qylsr-n2.qylsr,4) as qylsr,
            round(n1.qylsrzb-n2.qylsrzb,4) as qylsrzb,
            round(n1.stzcjz-n2.stzcjz,4) as stzcjz,
            round(n1.srhj-n2.srhj,4) as srhj,
            round(n1.sndljlr-n2.sndljlr,4) as sndljlr,
            round(n1.bnlr-n2.bnlr,4) as bnlr,
            round(n1.ljlr-n2.ljlr,4) as ljlr,
            round(n1.sndwjz-n2.sndwjz,4) as sndwjz,
            round(n1.sndtzhdwjz-n2.sndtzhdwjz,4) as sndtzhdwjz,
            round(n1.sqdwjz-n2.sqdwjz,4) as sqdwjz,
            round(n1.dwjz-n2.dwjz,4) as dwjz,
            round(n1.bqjzzjbd-n2.bqjzzjbd,4) as bqjzzjbd,
            round(n1.bnsyl-n2.bnsyl,4) as bnsyl,
            round(n1.jz-n2.jz,4) as jz,
            round(n1.ljpm-n2.ljpm,4) as ljpm,
            round(n1.bnpm-n2.bnpm,4) as bnpm from
 (select * from njfx_tzqkfx t1 where zhmc='本期累计'  and """ +sqlrq+""" limit 0,1 )  n1,
 (select * from njfx_tzqkfx t1 where zhmc='本期累计'  and """ +sqlbdrq+' order by t1.rq desc limit 0,1 ) n2 order by zhmc'
        
        cursorsj.execute(sql)
        sj = cursorsj.fetchall()
    elif blx[0][0] =='7': #每日资产净值
        cursorzhlist=connection.cursor()
        cursorzhlist.execute('select distinct zhsj from NJFX_NJZH t ')
        zhlist=cursorzhlist.fetchall()
        cursorzhlist.close()
        if rq2 is None or rq is None or zh is None:
            cursorsj.execute('''select x.zhmc,x.rq, x.zh1zc, x.zh2zc, x.zh3zc, x.zh4zc,x.zhhj,x.tabd,x.tabdje,x.bdhzhhj,decode(y.zhhj,null,0,trunc(x.bdhzhhj/y.zhhj,4)) syl from njfx_syl x 
left join ( select a.id,a.zhmc,a.rq,lead(a.rq,1,0) over(order by a.rq) last_rq,a.zhhj as zhhj,a.bdhzhhj from NJFX_SYL a) y on y.zhmc=x.zhmc and x.rq=y.last_rq  where x.rq>=%s order by x.rq desc ''',[rq])
            
        else:
            zhtemp ='%'+zh+'%'
            cursorsj.execute('''select x.zhmc,x.rq, x.zh1zc, x.zh2zc, x.zh3zc, x.zh4zc,x.zhhj,x.tabd,x.tabdje,x.bdhzhhj,decode(y.zhhj,null,0,trunc(x.bdhzhhj/y.zhhj,4)) syl from njfx_syl x 
left join ( select a.id,a.zhmc,a.rq,lead(a.rq,1,0) over(order by a.rq) last_rq,a.zhhj as zhhj,a.bdhzhhj from NJFX_SYL a) y on y.zhmc=x.zhmc and x.rq=y.last_rq where  x.zhmc like %s  and  x.rq>=%s  and x.rq<=%s order by x.rq desc''',[zhtemp,rq,rq2])
            
        sj = cursorsj.fetchall()
        
    else:
        pass   

    cursorrq.close()
    cursorzh.close()    
    cursorsj.close() 
    paginator = Paginator(sj,30)
    try:
        sj = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
        sj = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
        sj = paginator.page(paginator.num_pages)
    return render_to_response('tghsj.html',{'sj':sj,'blx':blx[0][0],'rqlist':rqlist,'zhlist':zhlist,'kssj':rq,'jzsj':rq2,'rq':rq,'zh':zh,'username':username,'trnum':trnum})
@login_required
def Tzqkfx(request):
    username = request.user.username
    cursorsj = connection.cursor()
    cursorsj.execute('''select distinct(t2.rq) from NJFX_gyfx t1,njfx_zcfbb t2,njfx_zcqkb t3 where t1.zhmc=t2.zhmc and t1.zhmc=t3.zhmc
and replace(replace(replace(t1.jsrq,'年','-'),'月','-'),'日','')= t2.rq and t2.rq=t3.rq''')
    rq = cursorsj.fetchall()
    rq1 = rq[0][0]
    cursorsj.close()
    #获取上期的日期，提醒防止数据计算错误
    cursorsqrq = connection.cursor()
    cursorsqrq.execute('select max(rq) from NJFX_TZQKFX t where zhmc=\'本期累计\'')
    sqrq = cursorsqrq.fetchall()
    sqrq = sqrq[0][0]
    cursorsqrq.close()
    cursorsj.close()
    #先查出各项组合的明细分析数据
    sqldata =  '''select  rq,zhmc, wtje, yhck, zqnhg, qthbjj, hblxj, hblzb, hblsr, hblsrzb, xdg, wcp, qyz, qtgdl, gdlxj, gdlzb, gdlsr, gdlsrzb, gp, gpjj, qylxj, qylzb, gpzb, qylsr, qylsrzb, stzcjz, srhj, sndljlr,'' as bnlr,ljlr,'' as sndwjz,'' as tzhsndwjz,sqdwjz,dwjz, ljpm,  bnpm from tzfx1_2 where rq= %s  
 union select  rq,zhmc, wtje, yhck, zqnhg, qthbjj, hblxj, hblzb, hblsr, hblsrzb, xdg, wcp, qyz, qtgdl, gdlxj, gdlzb, gdlsr, gdlsrzb, gp, gpjj, qylxj, qylzb, gpzb, qylsr, qylsrzb, stzcjz, srhj, sndljlr,'' as bnlr,ljlr,'' as sndwjz,'' as tzhsndwjz,sqdwjz,dwjz,ljpm, 
 bnpm from tzfx2 where rq = %s   '''
    
    cursor = connection.cursor()
    cursor.execute(sqldata,[rq1,rq1])
    tzfx = cursor.fetchall()  
    cursor.close()     
    #各有效组合的总金额    
    return render_to_response('tzfx.html',{'rq':rq,'tzfx':tzfx,'sqrq':sqrq}) 
def save_tzqkfx(request):
    rq = request.POST.get('rq1') 
    # 先写入各组合明细tzfx1_2、//合并、本期累计、计划tzfx2
    sql1 = '''insert into njfx_tzqkfx ( rq,zhmc, wtje, yhck, zqnhg, qthbjj, hblxj, hblzb, hblsr, hblsrzb, xdg, wcp, qyz, qtgdl, gdlxj, gdlzb, gdlsr, gdlsrzb, gp, gpjj, qylxj, qylzb, gpzb, qylsr, qylsrzb, stzcjz, srhj, sndljlr,ljlr,bnlr,sndwjz, sndtzhdwjz,sqdwjz,dwjz, bqjzzjbd,ljpm,  bnpm) '''
    sqldata1 =  '''select  rq,zhmc, wtje, yhck, zqnhg, qthbjj, hblxj, hblzb, hblsr, hblsrzb, xdg, wcp, qyz, qtgdl, gdlxj, gdlzb, gdlsr, gdlsrzb, gp, gpjj, qylxj, qylzb, gpzb, qylsr, qylsrzb, stzcjz, srhj,sndljlr, ljlr, ljlr-sndljlr as bnlr,'' as sndwjz, '' as sndtzhdwjz,sqdwjz,dwjz,round(dwjz-sqdwjz,2) as bqjzzjbd, ljpm,  bnpm from tzfx1_2 where rq= %s  
               union select  rq,zhmc, wtje, yhck, zqnhg, qthbjj, hblxj, hblzb, hblsr, hblsrzb, xdg, wcp, qyz, qtgdl, gdlxj, gdlzb, gdlsr, gdlsrzb, gp, gpjj, qylxj, qylzb, gpzb, qylsr, qylsrzb, stzcjz, srhj, sndljlr,ljlr, ljlr-sndljlr as bnlr,'' as sndwjz, '' as sndtzhdwjz,sqdwjz,dwjz, round(dwjz-sqdwjz,2) as bqjzzjbd,ljpm,  bnpm from tzfx2 where rq = %s  '''
 
    sqlinsert1  = sql1+sqldata1
    cursorsave = connection.cursor() # 清楚重复数据
    try:
        cursorsave.execute(sqlinsert1,[rq,rq]) 
    except Exception as error:
        print (error)
    cursorsave.close()                     
    return HttpResponseRedirect('/sjcx/?blx=6&rq='+rq)
@login_required
def srfx(request):
    if request.method=="POST":
        rq1 = request.POST.get('rq1')
        cursorsrfxsave = connection.cursor()
        try:
            cursorsrfxsave.execute('insert into njfx_srfx (jsrq, zhmc, xm, zqnhg, qthbl, ldxxj, xyck, gz, qyz, kzz, llcp, qtgdl, gdlxj, gp, qtqyl, qylxj, hj) select jsrq, zhmc, xm, zqnhg, qthbl, ldxxj, xyck, gz, qyz, kzz, llcp, qtgdl, gdlxj, gp, qtqyl, qylxj, hj from srfx where jsrq= %s order by jsrq desc,zhmc,xm',[rq1])
        except:
            pass
        finally:
            cursorsrfxsave.close()
            return HttpResponseRedirect('/sjcx/?blx=5&rq='+rq1)
    else:
        cursorrq = connection.cursor()
        cursorrq.execute('select distinct jsrq from NJFX_ZCFBBRJCC t')
        rq = cursorrq.fetchall()
        cursorrq.close()
        rq1 = rq[0][0]
        print (rq1)
        cursorsrfx = connection.cursor()
        cursorsrfx.execute('select jsrq, zhmc, xm, zqnhg, qthbl, ldxxj, xyck, gz, qyz, kzz, llcp, qtgdl, gdlxj, gp, qtqyl, qylxj, hj from srfx where jsrq= %s order by jsrq desc,zhmc,xm',[rq1])
        srfx = cursorsrfx.fetchall()
        cursorsrfx.close()         
        return render_to_response('srfx.html', {'srfx':srfx,'rq':rq})
@login_required
def sylfx(request):
    username = request.user.username
    if request.method=="POST":
        rq1 = request.POST.get('kssj')
        rq2 = request.POST.get('jzsj')
        rq1=str(rq1)
        rq2=str(rq2)
        zh = request.POST.get('zh')
        zh1='成都路局-'+zh
        zh2='成都路局-'+zh+'2'
        zh3='成都路局-'+zh+'3'
        zh4='成都路局-'+zh+'4'
        syllist=[]
        cursorzhlist=connection.cursor()
        cursorzhlist.execute('select distinct zhsj from NJFX_NJZH t ')
        zhlist=cursorzhlist.fetchall()
        cursorzhlist.close() 
        cursortabd = connection.cursor()
        cursortabd.execute('''
        select  distinct(t1.rq),'%s' as zhmc,A.slje,B.slje,C.slje,D.slje,round(ifnull(A.slje,0)+ifnull(B.slje,0)+ifnull(C.slje,0)+ifnull(D.slje,0),2) as jehj,E.taslje,round(ifnull(A.slje,0)+ifnull(B.slje,0)+ifnull(C.slje,0)+ifnull(D.slje,0)+ifnull(E.taslje,0),2) as drje 
from njfx_zcjz t1 left join (select NJFX_ZCJZ.RQ,zhmc,NJFX_ZCJZ.SLJE as slje from NJFX_ZCJZ where zhmc='%s') A ON t1.rq=A.rq
left join (select NJFX_ZCJZ.RQ,zhmc,NJFX_ZCJZ.SLJE as slje from NJFX_ZCJZ where zhmc='%s') B ON t1.rq= B.rq
left join (select NJFX_ZCJZ.RQ,zhmc,NJFX_ZCJZ.SLJE as slje from NJFX_ZCJZ where zhmc='%s') C ON t1.rq=C.rq
left join (select NJFX_ZCJZ.RQ,zhmc,NJFX_ZCJZ.SLJE as slje from NJFX_ZCJZ where zhmc='%s') D ON t1.rq=D.rq
left join (select t.jzrq,sum(case when t.bz='申购款' then -(t.slje) else t.slje end) as  taslje from NJFX_TA t where zhmc like '%%%s%%' and  t.slje is not null   group by jzrq) E 
        on REPLACE(t1.RQ,'-','')=substr(e.jzrq,0,9) where t1.rq>='%s' and t1.rq<='%s' order by t1.rq
        ''' %(zh,zh1,zh2,zh3,zh4,zh1,rq1,rq2))
        tabd= cursortabd.fetchall()
        cursortabd.close() 
        for i in range(1,len(tabd)):
            bdtup = tabd[i]
            bdtuptmep = (round(tabd[i][8]/tabd[i-1][6], ndigits=4),)
            bdtup = bdtup+bdtuptmep
            syllist.append(bdtup)
        return render_to_response('sylfx.html', {'tabd':syllist,'zh':zhlist,'kssj1':rq1,'jzsj1':rq2,'zh1':zh})
    else:
        cursorzh=connection.cursor()
        cursorzh.execute('select distinct zhsj from NJFX_NJZH t ')
        zh=cursorzh.fetchall()
        cursorzh.close()
        return render_to_response('sylfx.html',{'zh':zh,'username':username})
def sylfxsave(request):
    if request.method=="POST":
        rq1 = request.POST.get('kssj')
        rq2 = request.POST.get('jzsj')
        zh = request.POST.get('zh')
        rq1=str(rq1)
        rq2=str(rq2)
        #zh=zh.encode("utf-8")
        cursorzhlist=connection.cursor()
        cursorzhlist.execute('select distinct zhsj from NJFX_NJZH t ')
        zhlist=cursorzhlist.fetchall()
        cursorzhlist.close()
        cursortabd = connection.cursor()
        bdsql='select DISTINCT(X.RQ),\''+zh
        bdsql = bdsql+'''' AS zh,A.ZH1,B.ZH2,C.ZH3,D.ZH4,nvl(A.ZH1,0)+nvl(B.ZH2,0)+nvl(c.zh3,0)+nvl(d.zh4,0) AS JZHJ,E.SLJE AS BDJE,nvl(A.ZH1,0)+nvl(B.ZH2,0)+nvl(c.zh3,0)+nvl(d.zh4,0)+nvl(E.SLJE,0) AS DRJZ  from NJFX_ZCJZ x
left join (select NJFX_ZCJZ.RQ,'ss' AS zh,NJFX_ZCJZ.SLJE as zh1 from NJFX_ZCJZ WHERE ZH='''
        bdsql = bdsql + '\'成都路局-'+zh+'1\') A on X.RQ=A.RQ'
        bdsql = bdsql + ' left join (select NJFX_ZCJZ.RQ,\''+zh+'\' AS zh,NJFX_ZCJZ.SLJE as zh2 from NJFX_ZCJZ WHERE ZH=\'成都路局-'+zh+'2\') B on X.RQ=B.RQ'
        bdsql = bdsql + ' left join (select NJFX_ZCJZ.RQ,\''+zh+'\' AS zh,NJFX_ZCJZ.SLJE as zh3 from NJFX_ZCJZ WHERE ZH=\'成都路局-'+zh+'3\') C on X.RQ=C.RQ'
        bdsql = bdsql + ' left join (select NJFX_ZCJZ.RQ,\''+zh+'\' AS zh,NJFX_ZCJZ.SLJE as zh4 from NJFX_ZCJZ WHERE ZH=\'成都路局-'+zh+'4\') D on X.RQ=D.RQ'
        bdsql= bdsql + ' left join (select t.jzrq,sum(case when t.bz=\'申购款\' then -abs(t.slje) else t.slje end) as  slje from NJFX_TA t where zhmc like\'成都路局-'
        bdsql = bdsql+zh+'%\' and t.slje is not null   group by jzrq) E on REPLACE(x.RQ,\'-\',\'\')=TRUNC(e.JZRQ)  where x.rq>=\''+rq1+'\' and x.rq<=\''+rq2+'\' '
        insertsql = 'insert into njfx_syl (rq, zhmc, zh1zc, zh2zc, zh3zc, zh4zc,zhhj,  tabdje, bdhzhhj)' +bdsql
        delsql = 'delete from njfx_syl where zhmc like \''+zh+'\' and rq>=\''+rq1+'\' and rq<=\''+rq2+'\''
        
        try:
            cursortabd.execute(delsql)
        except Exception as error:
            print (error)
        try:
            cursortabd.execute(insertsql)
            print ('ok1ok1ok1')
        finally:
            cursortabd.close()
            return HttpResponseRedirect('/sjcx/?blx=7&rq='+rq1)

def export_excel(request,chunk_size=512):
    rq = request.GET.get('rq') 
    zh = request.GET.get('zh')
    blx = request.GET.get('blx')
    print(blx)
    tabname = ''
    if zh is None or zh=='ALL':
        zh = 'ALL'
        sqlzh = '1=1'
    else:
        sqlzh = 'zhmc=\''+str(zh)+'\''
    if rq is None or rq=='ALL':
        sqlrq = '1=1'
        rq= 'ALL'
    elif blx=='2' or blx=='4':
        sqlrq = 'jsrq=\''+str(rq)+'\'' 
    else:
        sqlrq = 't1.rq=\''+str(rq)+'\''
        sqlbdrq = 't1.rq<\''+str(rq)+'\''
    if blx == '1':
        tabname = 'njfx_zcqkb'
        sqlhead = 'select rq, tzzhdm, zhmc, dwjz, stzcjz, zcfe, wtje, jsy, drrq from njfx_zcqkb t1 where '
    elif blx == '2':
        tabname = 'njfx_gyfx'
    elif blx == '3':
        tabname = 'njfx_zcfbb' 
    elif blx =='4':
        tabname ='njfx_zcfbbrjcc'
    #print (list_obj)
    sql = sqlhead+sqlzh+' and '+sqlrq
    excelname = tabname +'.xls'
    cursordata = connection.cursor()
    data = cursordata.execute(sql)
    if data:  
        # 创建工作薄  
        ws = xlwt.Workbook(encoding='utf-8')  
        w = ws.add_sheet(u"数据报表第一页")  
        w.write(0, 0, "id")  
        w.write(0, 1, u"用户名")  
        w.write(0, 2, u"发布时间")  
        w.write(0, 3, u"内容")  
        w.write(0, 4, u"来源")
        w.write(0, 5, "id")  
        w.write(0, 6, u"用户名")  
        w.write(0, 7, u"发布时间")  
        w.write(0, 8, u"内容")  
        w.write(0, 9, u"来源")   
        # 写入数据  
        excel_row = 1  
        for obj in data:  
            data_id = obj[0]
            data_rq = obj[1]
            data_zhmc = obj[2]
            data_zclb = obj[3]
            data_zcmc = obj[4]
            data_sz = obj[5]             
            w.write(excel_row, 0, data_id)  
            w.write(excel_row, 1, data_rq)  
            w.write(excel_row, 2, data_zhmc)  
            w.write(excel_row, 3, data_zclb)
            w.write(excel_row, 4, data_zhmc)  
            w.write(excel_row, 5, data_sz)  
            excel_row += 1  
        # 检测文件是够存在  
        # 方框中代码是保存本地文件使用，如不需要请删除该代码  
        exist_file = os.path.exists(str(tabname)+'.xls')  
        if exist_file:  
            os.remove(str(tabname)+'.xls')  
        ws.save(str(tabname)+'.xls')  
        sio = io.BytesIO()
        ws.save(sio)  
        sio.seek(0) 
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')  
        response['Content-Disposition'] = 'attachment; filename='+excelname  
        #response.write(sio.getvalue())  
        return response
@login_required
def tghsj1(request):
    username = request.user.username
    rq = request.GET.get('rq') 
    zh = request.GET.get('zh')
    rq2= request.GET.get('rq2')
    blx = request.GET.get('blx')
    page = request.GET.get('page')
    #print type(rq),'11',type(blx),rq ,blx[0][0]   
    cursorsj = connection.cursor()
    cursorrq = connection.cursor()
    cursorzh = connection.cursor()
    sj =''
    rqlist = ''
    zhlist=''
    sqlrq = ''
    sqlzh = ''
    sqlbdrq=''
    if zh is None or zh=='ALL':
        zh = 'ALL'
        sqlzh = '1=1'
    else:
        sqlzh = 'zhmc=\''+str(zh)+'\''
    if rq is None or rq=='ALL':
        sqlrq = '1=1'
        rq= 'ALL'
    elif blx=='2' or blx=='4':
        sqlrq = 'jsrq=\''+str(rq)+'\'' 
    else:
        sqlrq = 't1.rq=\''+str(rq)+'\''
        sqlbdrq = 't1.rq<\''+str(rq)+'\''
    if blx[0][0] =='1':#资产情况表
        cursorrq.execute('select distinct(rq) from njfx_zcqkb t ')
        cursorzh.execute('select distinct(zhmc) from njfx_zcqkb t')
        rqlist = cursorrq.fetchall()
        zhlist = cursorzh.fetchall()
        sql = 'select rq, tzzhdm, zhmc, dwjz, stzcjz, zcfe, wtje, jsy, drrq from njfx_zcqkb t1 where '+sqlrq+' and '+ sqlzh+' order by rq desc '
        #cursorsj.execute('select rq, tzzhdm, zhmc, dwjz, stzcjz, zcfe, wtje, jsy, drrq from njfx_zcqkb where %s and %s order by rq desc ',[sqlrq,sqlzh]) 
        cursorsj.execute(sql)
        sj = cursorsj.fetchall()
    elif blx[0][0] =='2':# 归因分析
        cursorrq = connection.cursor()
        cursorrq.execute('select distinct(jsrq) from NJFX_GYFX t order by jsrq desc')
        cursorzh.execute('select distinct(zhmc) from NJFX_GYFX t ')
        zhlist =cursorzh.fetchall()
        rqlist = cursorrq.fetchall()
        cursorrq.close()
        sql = 'select  ksrq, jsrq,zhmc, zclb, zcmc, sye1_bqlj, round(sye1_bqsyzb,2) ,sye1_bnlj, round(sye1_bnsyzb,2), sye2_bqlj, sye2_bnlj, round(tzsyl_bqlj,2), round(tzsyl_bnlj,2), drrq from njfx_gyfx t1 where '+sqlrq+' and '+ sqlzh+' order by jsrq desc '
        #cursorsj.execute('select  ksrq, jsrq,zh, zclb, zcmc, sye1_bqlj, round(sye1_bqsyzb,2) ,sye1_bnlj, round(sye1_bnsyzb,2), sye2_bqlj, sye2_bnlj, round(tzsyl_bqlj,2), round(tzsyl_bnlj,2), drrq from njfx_gyfx where jsrq= %s order by jsrq desc',[rq])
       
        cursorsj.execute(sql)
        sj = cursorsj.fetchall()
    elif blx[0][0] =='3':#资产分布
        cursorrq = connection.cursor()
        cursorrq.execute('select distinct(rq) from njfx_zcfbb t order by rq desc')
        rqlist = cursorrq.fetchall()
        cursorzh.execute('select distinct(zhmc) from njfx_zcfbb ')
        zhlist = cursorzh.fetchall()
        cursorrq.close()
        sql = 'select  rq, zhmc, zclb, zcmc, sz, zjzcbl,  drrq from njfx_zcfbb t1 where '+sqlrq+' and '+ sqlzh+' order by rq desc '
        cursorsj.execute(sql)
        sj = cursorsj.fetchall()
    elif blx[0][0] =='4':#日均持仓分析
        cursorrq = connection.cursor()
        cursorrq.execute('select distinct(jsrq) from njfx_zcfbbrjcc t order by jsrq desc')
        rqlist = cursorrq.fetchall()
        cursorzh.execute('select distinct(zhmc) from njfx_zcfbbrjcc ')
        zhlist = cursorzh.fetchall()        
        cursorrq.close()
        sql = 'select  ksrq, jsrq, zhmc, zclb, zcmc, rjcccb, rjccye, drrq from  njfx_zcfbbrjcc t1 where '+sqlrq+' and '+ sqlzh+' order by jsrq desc '
        cursorsj.execute(sql)
        sj = cursorsj.fetchall()
    elif blx[0][0] =='5': #收入分析
        cursorsj.execute('select jsrq, zhmc, xm, zqnhg, qthbl, ldxxj, xyck, gz, qyz, kzz, llcp, qtgdl, gdlxj, gp, qtqyl, qylxj, hj from njfx_srfx t1 order by jsrq desc ,zhmc,xm')
        sj = cursorsj.fetchall()
    elif blx[0][0] =='6': #投资分析
        cursorrq = connection.cursor()
        cursorrq.execute('select distinct(rq) from njfx_tzqkfx t ')
        rqlist = cursorrq.fetchall()
        #if rq is None:
            #rq = rqlist[0][0]
        cursorrq.close()
        sql = "select rq,zhmc, wtje, yhck, zqnhg, qthbjj, hblxj, hblzb, hblsr, hblsrzb, xdg, wcp, qyz, qtgdl, gdlxj, gdlzb, gdlsr, gdlsrzb, gp, gpjj, qylxj, qylzb, gpzb, qylsr, qylsrzb, stzcjz, srhj, sndljlr, bnlr, ljlr, sndwjz, sndtzhdwjz, sqdwjz, dwjz, bqjzzjbd, bnsyl, jz, ljpm, bnpm from njfx_tzqkfx t1 where "+sqlrq
        sql += """ union SELECT distinct t1.rq,'上期累计' as zhmc,t2.wtje, t2.yhck, t2.zqnhg, t2.qthbjj, t2.hblxj, t2.hblzb, t2.hblsr, t2.hblsrzb, t2.xdg, t2.wcp, t2.qyz, t2.qtgdl, t2.gdlxj, t2.gdlzb, t2.gdlsr, t2.gdlsrzb, t2.gp, t2.gpjj, t2.qylxj, t2.qylzb, t2.gpzb, t2.qylsr, t2.qylsrzb, t2.stzcjz, t2.srhj, t2.sndljlr, t2.bnlr, t2.ljlr, t2.sndwjz, t2.sndtzhdwjz, t2.sqdwjz, t2.dwjz, t2.bqjzzjbd, t2.bnsyl, t2.jz, t2.ljpm, t2.bnpm FROM njfx_tzqkfx t1 
left join 
(select * from njfx_tzqkfx where zhmc='本期累计') t2
on t2.rq in (select max(rq) from njfx_tzqkfx where zhmc='本期累计' and rq<t1.rq)
 where t1.zhmc='本期累计'and """ +sqlrq
        if rq != None and rq!='ALL':
            sql +=""" union select n1.rq,'本期增减变动' as zhmc,
            round(n1.wtje-n2.wtje,4) as wtje,
            round(n1.yhck-n2.yhck,4) as yhck,
            round(n1.zqnhg-n2.zqnhg,4) as zqnhg,
            round(n1.qthbjj-n2.qthbjj,4) as qthbjj,
            round(n1.hblxj-n2.hblxj,4) as hblxj,
            round(n1.hblzb-n2.hblzb,4) as hblzb,
            round(n1.hblsr-n2.hblsr,4) as hblsr,
            round(n1.hblsrzb-n2.hblsrzb,4) as hblsrzb,
            round(n1.xdg-n2.xdg,4) as xdg,
            round(n1.wcp-n2.wcp,4) as wcp,
            round(n1.qyz-n2.qyz,4) as qyz,
            round(n1.qtgdl-n2.qtgdl,4) as qtgdl,
            round(n1.gdlxj-n2.gdlxj,4) as gdlxj,
            round(n1.gdlzb-n2.gdlzb,4) as gdlzb,
            round(n1.gdlsr-n2.gdlsr,4) as gdlsr,
            round(n1.gdlsrzb-n2.gdlsrzb,4) as gdlsrzb,
            round(n1.gp-n2.gp,4) as gp,
            round(n1.gpjj-n2.gpjj,4) as gpjj,
            round(n1.qylxj-n2.qylxj,4) as qylxj,
            round(n1.qylzb-n2.qylzb,4) as qylzb,
            round(n1.gpzb-n2.gpzb,4) as gpzb,
            round(n1.qylsr-n2.qylsr,4) as qylsr,
            round(n1.qylsrzb-n2.qylsrzb,4) as qylsrzb,
            round(n1.stzcjz-n2.stzcjz,4) as stzcjz,
            round(n1.srhj-n2.srhj,4) as srhj,
            round(n1.sndljlr-n2.sndljlr,4) as sndljlr,
            round(n1.bnlr-n2.bnlr,4) as bnlr,
            round(n1.ljlr-n2.ljlr,4) as ljlr,
            round(n1.sndwjz-n2.sndwjz,4) as sndwjz,
            round(n1.sndtzhdwjz-n2.sndtzhdwjz,4) as sndtzhdwjz,
            round(n1.sqdwjz-n2.sqdwjz,4) as sqdwjz,
            round(n1.dwjz-n2.dwjz,4) as dwjz,
            round(n1.bqjzzjbd-n2.bqjzzjbd,4) as bqjzzjbd,
            round(n1.bnsyl-n2.bnsyl,4) as bnsyl,
            round(n1.jz-n2.jz,4) as jz,
            round(n1.ljpm-n2.ljpm,4) as ljpm,
            round(n1.bnpm-n2.bnpm,4) as bnpm from
 (select * from njfx_tzqkfx t1 where zhmc='本期累计'  and """ +sqlrq+""" limit 0,1 )  n1,
 (select * from njfx_tzqkfx t1 where zhmc='本期累计'  and """ +sqlbdrq+' order by t1.rq desc limit 0,1 ) n2 order by zhmc'
        
        cursorsj.execute(sql)
        sj = cursorsj.fetchall()
    elif blx[0][0] =='7': #每日资产净值
        cursorzhlist=connection.cursor()
        cursorzhlist.execute('select distinct zhsj from NJFX_NJZH t ')
        zhlist=cursorzhlist.fetchall()
        cursorzhlist.close()
        if rq2 is None or rq is None or zh is None:
            cursorsj.execute('''select x.zhmc,x.rq, x.zh1zc, x.zh2zc, x.zh3zc, x.zh4zc,x.zhhj,x.tabd,x.tabdje,x.bdhzhhj,decode(y.zhhj,null,0,trunc(x.bdhzhhj/y.zhhj,4)) syl from njfx_syl x 
left join ( select a.id,a.zhmc,a.rq,lead(a.rq,1,0) over(order by a.rq) last_rq,a.zhhj as zhhj,a.bdhzhhj from NJFX_SYL a) y on y.zhmc=x.zhmc and x.rq=y.last_rq  where x.rq>=%s order by x.rq desc ''',[rq])
            
        else:
            zhtemp ='%'+zh+'%'
            cursorsj.execute('''select x.zhmc,x.rq, x.zh1zc, x.zh2zc, x.zh3zc, x.zh4zc,x.zhhj,x.tabd,x.tabdje,x.bdhzhhj,decode(y.zhhj,null,0,trunc(x.bdhzhhj/y.zhhj,4)) syl from njfx_syl x 
left join ( select a.id,a.zhmc,a.rq,lead(a.rq,1,0) over(order by a.rq) last_rq,a.zhhj as zhhj,a.bdhzhhj from NJFX_SYL a) y on y.zhmc=x.zhmc and x.rq=y.last_rq where  x.zhmc like %s  and  x.rq>=%s  and x.rq<=%s order by x.rq desc''',[zhtemp,rq,rq2])
            
        sj = cursorsj.fetchall()
        
    else:
        pass   

    cursorrq.close()
    cursorzh.close()    
    cursorsj.close() 
    paginator = Paginator(sj,30)
    try:
        sj = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
        sj = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
        sj = paginator.page(paginator.num_pages)
    return render_to_response('tghsj1.html',{'sj':sj,'blx':blx[0][0],'rqlist':rqlist,'zhlist':zhlist,'kssj':rq,'jzsj':rq2,'rq':rq,'zh':zh,'username':username})
def tghsj_ajax(request):
    cursorsj = connection.cursor()
    cursorcount = connection.cursor()
    rq = request.GET.get('rq') 
    zh = request.GET.get('zh')
    blx = request.GET.get('blx')
    htmlstr = ''
    k = 0
    per_page = int(request.GET.get('per_page','50'))
    curr_page = int(request.GET.get('curr_page','1'))
    if zh is None or zh=='ALL':
        zh = 'ALL'
        sqlzh = '1=1'
    else:
        sqlzh = 'zhmc=\''+str(zh)+'\''
    if rq is None or rq=='ALL':
        sqlrq = '1=1'
        rq= 'ALL'
    elif blx=='2' or blx=='4':
        sqlrq = 'jsrq=\''+str(rq)+'\'' 
    else:
        sqlrq = 't1.rq=\''+str(rq)+'\''
        sqlbdrq = 't1.rq<\''+str(rq)+'\''
    if blx[0][0]=='1':
        k=0
        sqlcount = 'select count(*) from njfx_zcqkb t1 where '+sqlrq+' and '+ sqlzh
        sql = 'select rq, tzzhdm, zhmc, dwjz, stzcjz, zcfe, wtje, jsy, drrq from njfx_zcqkb t1 where '+sqlrq+' and '+ sqlzh+' order by rq desc '
    #cursorsj.execute('select rq, tzzhdm, zhmc, dwjz, stzcjz, zcfe, wtje, jsy, drrq from njfx_zcqkb where %s and %s order by rq desc ',[sqlrq,sqlzh]) 
        cursorcount.execute(sqlcount)
        allcount = cursorcount.fetchone()
        allpage = math.ceil(allcount[0]/per_page)
        cursorsj.execute(sql)
        sj = cursorsj.fetchall()
        for i in sj:
            k+=1
            htmlstr += '<tr><td>'+str(k)+'</td>'
            for v in i:
                htmlstr += '<td>'+str(v)+'</td>'
            htmlstr+='</tr>'
    cursorsj.close()
    cursorcount.close()
    test = 'tset'
    return HttpResponse(htmlstr+test)
def uploadfile(request):
    if request.method == 'POST':
        # filename = str(request.FILES['file'])
        # print (filename)
        # xhr单实例多文件
        filescount = len(request.FILES)
       
        for i in range(0,filescount):

            filedata = request.FILES[str(i)]
            filename = filedata.name
            print(filename)
            try:
                handle_uploadfile(filedata,filename)
            except Exception as e:
                print (e)
        request.session.set_expiry(60)
        request.session['test']='acerjin'
        request.session['setest']=['11','22']
        v = request.session.get('test')
        v2 = request.session.get('setest')
        k = request.session.keys()
        va = request.session.values()
        it =  request.session.items() 
        print (v,v2,k,va,it) 
        # request.session.iterkeys()
        # request.session.itervalues()
        # request.session.iteritems()
        
        #webuploader多实例
        # if request.FILES:
        #     print (request.FILES['file'])

    return render_to_response('uploadfile.html')
def handle_uploadfile(filedata,filename):
    path = '\\file'
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print (e)
    with open(os.path.join(path,filename),'wb+') as f:
        for ch in filedata.chunks():
            f.write(ch)