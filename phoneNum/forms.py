from django.forms import ModelForm
# Create your views here.

from phoneNum.models import dclxxb

class dclxxbform(ModelForm):
	"""docstring for dwxxform"""
	class Meta:
		model = dclxxb
		fields = ['xm','ybh','dwmc','yhm','xhm','bz','fbz']
		# fields = '__all__'