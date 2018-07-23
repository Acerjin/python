# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin
from .models import *
# Register your models here.
class WdcpAdmin(admin.ModelAdmin): 
    list_display = ('zhmc','pz','mc')
    fields = ['zhmc','pz','mc','je','zhzb','rzzt','ztpj','zxpj','qx','syl','pzrq','dqrq','synx','lshzj','by1','sfgq']
    #def __init__(self, *args, **kwargs):
       # self.fields['zh'].queryset = Zh.objects.all()
class TzqkfxAdmin(admin.ModelAdmin):
    list_display = ( 'zhmc','rq','stzcjz', 'srhj', 'sndljlr', 'bnlr', 'ljlr', 'sndwjz', 'sndtzhdwjz', 'sqdwjz', 'dwjz', 'bqjzzjbd', 'bnsyl', 'jz', 'ljpm', 'bnpm')
    fields= [ 'rq','zhmc','stzcjz', 'srhj', 'sndljlr', 'bnlr', 'ljlr', 'sndwjz', 'sndtzhdwjz', 'sqdwjz', 'dwjz', 'bqjzzjbd', 'bnsyl', 'jz', 'ljpm', 'bnpm']
    list_per_page=30
    list_filter = ['rq','zhmc',]
class NjzhAdmin(admin.ModelAdmin): 
    fields = ['zhmc','zhje','zhsj','zhll']
    list_display = fields = ('zhmc','zhje','zhsj','zhll')
class PzAdmin(admin.ModelAdmin): 
    fields = ['pz']
class CtglAdmin(admin.ModelAdmin):
    list_display = ('cpmc','lb','zhmc')
    fields = ['lb','rq', 'zhmc', 'cpmc', 'gm', 'zb', 'zcfb', 'xyfb1', 'xyfb2', 'xyfb3', 'xyfb4', 'qyzb', 'ggb', 'dwjz', 'synx', 'fxzkpg', 'fkcs', 'bz']
class ZczdAdmin(admin.ModelAdmin):
    list_display = ('zcmc','srlb','tzlb')
    fields = ['zcmc','srlb','tzlb']
    list_filter = ['srlb','tzlb',]
class GyfxAdmin(admin.ModelAdmin):
    list_display = ('ksrq','jsrq','zhmc','zclb','zcmc')
    fields = ['ksrq','jsrq','zhmc','zclb','zcmc']
    list_filter =['ksrq','jsrq','zhmc']
    list_per_page=30
class ZcfbbAdmin(admin.ModelAdmin):
    list_display = ('rq','zhmc','zclb','zcmc','sz')
    fields = ['rq','zhmc','zclb','zcmc','sz']
    list_filter =['rq','zhmc','zclb','zcmc']
    list_per_page=100    
admin.site.register(Wdcp,WdcpAdmin)
admin.site.register(Njzh,NjzhAdmin)
admin.site.register(Pz,PzAdmin)
admin.site.register(Tzqkfx,TzqkfxAdmin)
admin.site.register(Ctgl,CtglAdmin)
admin.site.register(Zczd,ZczdAdmin)
admin.site.register(Gyfx,GyfxAdmin)
admin.site.register(ZcFbb,ZcfbbAdmin)