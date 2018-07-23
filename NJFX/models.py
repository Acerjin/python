# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils.translation import ugettext_lazy as _






# Create your models here.

class Njzh(models.Model):
    id = models.AutoField(primary_key=True)
    zhsj = models.CharField(max_length=20,verbose_name = "组合上级名称")
    zhmc = models.CharField(max_length=20,verbose_name = "组合")
    zhje = models.DecimalField(max_digits=10, decimal_places=2,verbose_name = "组合金额")
    zhll = models.DecimalField(max_digits=4, decimal_places=2,verbose_name = "组合利率")
    class Meta:
        #db_table = 't_faq_category'
        verbose_name = u'组合'
        verbose_name_plural = u'组合'
        
        #app_label = u'My_Category'
    def __unicode__(self):
        return self.zhmc
    
class Pz(models.Model):
    
    pz = models.CharField(max_length=20,verbose_name = "品种",unique=True)
    class Meta:
        #db_table = 't_faq_category'
        verbose_name = u'品种'
        verbose_name_plural = u'品种'
        
        #app_label = u'My_Category'
    def __unicode__(self):
        return self.pz
    
class Wdcp(models.Model):
    id = models.AutoField(primary_key=True)
    zhmc = models.ForeignKey(Njzh,verbose_name = "组合")
    pz = models.ForeignKey(Pz,verbose_name = "品种")
    mc = models.CharField(max_length=100,blank=True,null=True,verbose_name = "名称")
    je = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True,verbose_name = "金额")
    zhzb = models.DecimalField(max_digits=4, decimal_places=2,blank=True,null=True,verbose_name = "组合占比")
    rzzt = models.CharField(max_length=20, blank=True,null=True,verbose_name = "融资主体")
    ztpj = models.CharField(max_length=20, blank=True,null=True,verbose_name = "主体评级")
    zxpj = models.CharField(max_length=20, blank=True,null=True,verbose_name = "债项评级")
    qx = models.CharField(max_length=20, blank=True,null=True,verbose_name = "期限")
    syl = models.DecimalField(max_digits=4, decimal_places=2,blank=True,null=True,verbose_name = "收益率")
    pzrq = models.DateField(blank=True,null=True,  verbose_name = "配置日期")
    dqrq = models.DateField(blank=True,null=True,verbose_name = "到期日期")
    synx = models.DecimalField(max_digits=4, decimal_places=2,blank=True,null=True,verbose_name = "剩余年限")
    lshzj = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True,verbose_name = "理事会资金")
    by1 = models.CharField(max_length=20, blank=True,null=True,verbose_name = "备用字段")
    sfgq =  models.CharField(max_length=5,blank=True,null=True,verbose_name='是否到期',choices=(('1','合同到期'),('0','未到期')),default='0')

    class Meta:
        #db_table = 't_faq_category'
        verbose_name = u'稳定类产品'
        verbose_name_plural = u'稳定类产品'
        unique_together = ('mc','pzrq')
        #app_label = u'My_Category'
    def __unicode__(self):
        return self.mc
    
class Gyfx(models.Model):
    id = models.AutoField(primary_key=True)
    ksrq = models.CharField(max_length=15, blank=True, null=True,verbose_name='开始日期')
    jsrq = models.CharField(max_length=15, blank=True, null=True,verbose_name='结束日期')
    tgh = models.CharField(max_length=5, blank=True, null=True)
    zclb = models.CharField(max_length=30,verbose_name='资产类别')
    zcmc = models.CharField(max_length=50,verbose_name='资产名称')
    sye1_bqlj = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    sye1_bqsyzb = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    sye1_bnlj = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    sye1_bnsyzb = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    sye2_bqlj = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    sye2_bnlj = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    tzsyl_bqlj = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True) # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    tzsyl_bnlj = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    zhmc = models.CharField(max_length=10, blank=True, null=True,verbose_name='组合名称')
    drrq = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        verbose_name = u'归因分析表'
        verbose_name_plural = u'归因分析表'        
        unique_together = ('zcmc','ksrq','zhmc','zclb')
    def __unicode__(self):
        return self.tgh
    
class ZcFbb(models.Model):
    id = models.AutoField(primary_key=True)
    rq = models.CharField(max_length=15, blank=True, null=True)
    zhmc = models.CharField(max_length=10, blank=True, null=True)
    #tgh = models.CharField(max_length=5, blank=True, null=True)
    zclb = models.CharField(max_length=30)
    zcmc = models.CharField(max_length=50)
    sz = models.CharField(max_length=30,blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    zjzcbl = models.DecimalField(max_digits=25, decimal_places=15, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    zjzcblhj = models.DecimalField(max_digits=25, decimal_places=15, blank=True, null=True)
    drrq = models.CharField(max_length=20, blank=True, null=True)
    class Meta:     
        verbose_name = '资产分布表'
        verbose_name_plural = '资产分布表'
        unique_together = ('rq','zhmc','zcmc','zclb')
    def __unicode__(self):
        return self.zhmc
class ZcQkb(models.Model):
    id = models.AutoField(primary_key=True)
    rq = models.CharField(max_length=15)
    tzzhdm = models.CharField(max_length=15)
    #tgh = models.CharField(max_length=5, blank=True, null=True)
    zhmc = models.CharField(max_length=30)
    
    dwjz = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    stzcjz = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    zcfe = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    wtje = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    jsy = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    drrq = models.CharField(max_length=20, blank=True, null=True)
    class Meta:     
        
        unique_together = ('rq','tzzhdm')
    def __unicode__(self):
        return self.zhmc
class Tzqkfx(models.Model):
    zhmc_CHOICES = (
        (u'国寿',u'国寿'),
        (u'长江',u'长江'),
        (u'长江2',u'长江2'),
        (u'中信',u'中信'),
        (u'华夏',u'华夏'),
        (u'中金',u'中金'),
        (u'中金2',u'中金2'),
        (u'中金信托',u'中金信托'),
        (u'中金合并',u'中金合并'),
        (u'工银',u'工银'),
        (u'太平',u'太平'),
        (u'太平2',u'太平2'),
        (u'太平信托',u'太平信托'),
        (u'太平合并',u'太平合并'),
        (u'泰康',u'泰康'),
        (u'泰康2',u'泰康2'),
        (u'泰康3',u'泰康3'),
        (u'泰康合并',u'泰康合并'),
        (u'博时',u'博时'),
        (u'嘉实',u'嘉实'),
        (u'泰康4',u'泰康4'),
        (u'平安',u'平安'),
        (u'平安2',u'平安2'),
        (u'平安合并',u'平安合并'),
        (u'受托户',u'受托户'),
        (u'长江退休',u'长江退休'),
        (u'长江退休2',u'长江退休2'),
        (u'退休合并',u'退休合并'),
        (u'本期累计',u'本期累计'),
        (u'本期变动',u'本期变动'),
        (u'上期累计',u'上期累计'),
        (u'计划',u'计划'),
        (u'本期增减变动',u'本期增减变动'),
        
    )
    id = models.AutoField(primary_key=True)
    
    zhmc = models.CharField(max_length=15, blank=True, null=True,verbose_name = "组合",choices=zhmc_CHOICES)
    #tgh = models.CharField(max_length=5, blank=True, null=True)
    wtje = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='本金')
    yhck = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='货币类-银行存款')
    
    zqnhg =  models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='货币类-债券逆逆回购')  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    qthbjj = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='货币类-货币基金')  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    hblxj = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='货币类-货币类小计')
    hblzb = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,verbose_name='货币类-占净值比列')
    hblsr = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='货币类-收入')
    hblsrzb = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,verbose_name='货币类-比列')
    xdg = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='固定类-协议/定期存款/国债')
    wcp =  models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='固定类-23/24号文产品')  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    qyz = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='固定类-企业债')  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    qtgdl = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='固定类-其他固定类')
    gdlxj = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='固定类-固定类小计')
    gdlzb = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='固定类-占净值比例')
    gdlsr = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='固定类-收入')
    gdlsrzb = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,verbose_name='固定类-比列') 
    gp = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='权益类-股票')
    gpjj =  models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='权益类-股票基金')  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    qylxj = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='权益类-权益类小计')  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    qylzb = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='权益类-占净值比列')
    gpzb = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,verbose_name='权益类-股票比列')
    qylsr = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='权益类-收入')
    qylsrzb = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,verbose_name='权益类-比列')      
    stzcjz = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='基金净资产')  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    srhj = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='收入合计')
    sndljlr = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='截止上年底累计利润')
    bnlr = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='本年利润')
    ljlr = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='累计利润')
    sndwjz = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='上年单位净值')
    sndtzhdwjz = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='调整后上年单位净值')
    sqdwjz = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='上期单位净值')
    dwjz = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='本期单位净值')
    bqjzzjbd = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,verbose_name='上期净值增减变动')
    bnsyl = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,verbose_name='本期收益率')
    jz = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,verbose_name='基准率')
    ljpm = models.CharField(max_length=2,blank=True, null=True,verbose_name='累计排名')
    bnpm = models.CharField(max_length=2,blank=True, null=True,verbose_name='本年排名')
    rq = models.CharField(max_length=15,blank=True, null=True,verbose_name='日期')
    
    class Meta:
        verbose_name = u'投资情况分析表'
        verbose_name_plural = u'投资情况分析表'     
        
        unique_together = ('rq','zhmc')
    def __unicode__(self):
        return self.zhmc
class ZcFbbRjcc(models.Model):
    id = models.AutoField(primary_key=True)
    ksrq = models.CharField(max_length=15, blank=True, null=True)
    jsrq = models.CharField(max_length=15, blank=True, null=True)
    zhmc = models.CharField(max_length=10, blank=True, null=True)
    #tgh = models.CharField(max_length=5, blank=True, null=True)
    zclb = models.CharField(max_length=30)
    zcmc = models.CharField(max_length=50)
    rjcccb = models.CharField(max_length=30,blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    rjccye = models.DecimalField(max_digits=25, decimal_places=15, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    drrq = models.CharField(max_length=20, blank=True, null=True)
    class Meta:     
        
        unique_together = ('jsrq','zhmc','zcmc','zclb')
    def __unicode__(self):
        return self.zhmc
class Ctgl(models.Model):
    lb_CHOICES = (
        (u'基金',u'基金'),
        (u'养老金',u'养老金'),
        (u'万能险',u'万能险'),
    )
    id = models.AutoField(primary_key=True)
    rq = models.DateField(verbose_name='日期')
    lb = models.CharField(max_length=10, blank=True, null=True, choices=lb_CHOICES, verbose_name='类别')
    zhmc = models.CharField(max_length=15, blank=True, null=True, verbose_name='组合名称')
    cpmc = models.CharField(max_length=20, blank=True, null=True, verbose_name='产品名称')
    gm = models.DecimalField(max_digits=25, decimal_places=15, blank=True, null=True,verbose_name='规模（万元）')
    zb = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,verbose_name='占组合资产净值比例')
    zcfb = models.CharField(max_length=100, blank=True, null=True, verbose_name='基金内资产分布%')
    xyfb1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,verbose_name='信用分布AAA',help_text='万能险不填写')
    xyfb2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,verbose_name='信用分布AA+',help_text='万能险不填写')
    xyfb3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,verbose_name='信用分布AA',help_text='万能险不填写')
    xyfb4 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,verbose_name='信用分布AA-',help_text='万能险不填写')
    qyzb = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,verbose_name='权益占比')
    ggb = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,verbose_name='权益占比',help_text='养老金、万能险不填写')
    dwjz = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True,verbose_name='单位净值',help_text='养老金、万能险不填写')
    synx = models.CharField(max_length=20, blank=True, null=True, verbose_name='剩余年限')
    fxzkpg = models.CharField(max_length=20, blank=True, null=True, verbose_name='风险状况评估')
    fkcs = models.CharField(max_length=20, blank=True, null=True, verbose_name='风控措施')
    bz = models.CharField(max_length=20, blank=True, null=True, verbose_name='备注')
    class Meta:
        verbose_name = u'穿透管理'
        verbose_name_plural = u'穿透管理' 
    def __unicode__(self):
        return self.zhmc
class TA(models.Model):
    id = models.AutoField(primary_key=True)
    rq = models.CharField(max_length=15, blank=True, null=True)
    zhmc = models.CharField(max_length=10, blank=True, null=True)
    #tgh = models.CharField(max_length=5, blank=True, null=True)
    bz = models.CharField(max_length=15)
    slje = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='数量/金额')
    jzrq = models.CharField(max_length=15, blank=True, null=True)
    xspzrq = models.CharField(max_length=15, blank=True, null=True)
    drrq = models.CharField(max_length=20, blank=True, null=True)
    class Meta: 
        unique_together = ('rq','zhmc','jzrq')
    def __unicode__(self):
        return self.zhmc
class Syl(models.Model):
    id = models.AutoField(primary_key=True)
    rq = models.CharField(max_length=10,verbose_name='日期')
    zhmc = models.CharField(max_length=15, blank=True, null=True, verbose_name='组合名称')
    zh1zc = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='组合1资产')  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    zh2zc = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='组合2资产')
    zh3zc = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='组合3资产')
    zh4zc = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='组合4资产')
    zh5zc = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='组合5资产')
    zh6zc = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='组合6资产')
    zh7zc = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='组合7资产')
    zhhj = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='资产合计')
    TAbd = models.CharField(max_length=5, blank=True, null=True,verbose_name='TA变动')
    TAbdje = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='TA变动金额')
    bdhzhhj = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='变动后资产合计')
    syl = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,verbose_name='收益率')
    drrq = models.CharField(max_length=20, blank=True, null=True)
    class Meta:         
        unique_together = ('rq','zhmc')
    def __unicode__(self):
        return self.zhmc
class ZcJz(models.Model):
    id = models.AutoField(primary_key=True)
    rq = models.CharField(max_length=15, blank=True, null=True)
    zhmc = models.CharField(max_length=10, blank=True, null=True)
    #tgh = models.CharField(max_length=5, blank=True, null=True)
    
    slje = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='数量/金额')

    drrq = models.CharField(max_length=20, blank=True, null=True)
    class Meta: 
        unique_together = ('rq','zhmc')
    def __unicode__(self):
        return self.zhmc
class Srfx(models.Model):
    id = models.AutoField(primary_key=True)
    jsrq = models.CharField(max_length=15,verbose_name='结束日期')
    zhmc = models.CharField(max_length=15, blank=True, null=True, verbose_name='组合名称')
    xm = models.CharField(max_length=15, blank=True, null=True, verbose_name='')
    zqnhg = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='')  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    qthbl = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='')
    xyck = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='')
    ldxxj = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='')
    gz = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='')
    qyz = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='')
    kzz = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='')
    llcp = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='')
    qtgdl = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='')
    gdlxj = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='')
    gp = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='')
    qtqyl = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='')
    qylxj = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='')
    hj = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True,verbose_name='')
    class Meta:         
        unique_together = ('jsrq','zhmc','xm')
    def __unicode__(self):
        return self.zhmc
class Zczd(models.Model): 
    srlb_choice = (
        ('债券逆回购','债券逆回购'),
        ('其他货币类','其他货币类'),
        ('协议存款','协议存款'),
        ('国债','国债'),
        ('企业债','企业债'),
        ('可转债','可转债'),
        ('另类产品','另类产品'),
        ('其他固定类','其他固定类'),
        ('股票','股票'),
        ('其他权益类','其他权益类'),
        ('备用','备用'),
    )
    tzlb_choice = (
        ('银行存款','银行存款'),
        ('债券逆回购','债券逆回购'),
        ('央行票据','央行票据'),
        ('货币基金','货币基金'),
        ('协议/定期存款/国债','协议/定期存款/国债'),
        ('23/24号文产品','23/24号文产品'),
        ('企业债','企业债'),
        ('其它固定类','其它固定类'),
        ('其它货币基金','其它货币基金'),
        ('股票','股票'),
        ('股票基金','股票基金'),
        ('比例','比例'),
        ('备用','备用'),
    )
    id = models.AutoField(primary_key=True)
    srlb = models.CharField(max_length=15,verbose_name='收入类别', choices=srlb_choice)
    tzlb = models.CharField(max_length=15,verbose_name='投资类别',choices=tzlb_choice)
    zcmc = models.CharField(max_length=50, verbose_name='资产名称')
    class Meta:
        verbose_name = u'资产分类关系'
        verbose_name_plural = u'资产分类关系' 
        def __unicode__(self):
            return self.zcmc