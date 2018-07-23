from django.contrib import admin

# Register your models here.

from .models import dwxx,dclxxb,UserAccount

class dwxxAdmin(admin.ModelAdmin):
	list_display = ('dwbm','dwmc','dwcwsx')
	fields = ['dwbm','dwmc','dwcwsx']

class  dclxxbAdmin(admin.ModelAdmin):
	"""docstring for  dcl"""
	list_display = ('xm','ybh','dwmc')
	fields = ['xm','ybh','dwmc']
class UserAccountAdmin(admin.ModelAdmin):
	list_display = ('user','dept','phone',)
	fields = ['user','dept','phone',]

admin.site.register(dwxx,dwxxAdmin)
admin.site.register(dclxxb,dclxxbAdmin)
admin.site.register(UserAccount,UserAccountAdmin)