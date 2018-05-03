
from django.conf.urls import url
from . import views
app_name="portal"
urlpatterns = [
url(r'^$', views.index, name='index'),
url(r'auth', views.auth, name='auth'),
url(r'forgotpasswd', views.forgotpasswd, name='forgotpasswd'),
url(r'login', views.login, name='login'),
url(r'logout', views.logout, name='logout'),
url(r'payment/completed', views.paymentcompleted, name='paymentcompleted'),
url(r'payment/list', views.listpayments, name='listpayments'),
url(r'^payment', views.payment, name='payment'),
url(r'verifycode', views.verifycode, name='verifycode'),
url(r'verify', views.verify, name='verify'),
url(r'^lawdetail/(?P<lawid>\d+)$', views.getlaw, name='getlaw'),
url(r'^lawsection/(?P<sectionid>\d+)$', views.getlawdetail, name='getlawdetail'),
url(r'^section/(?P<sectionid>\d+)$', views.listsections, name='listsections'),
url(r'^section', views.getsection, name='getsection'),
url(r'profile/update', views.updateprofile, name='updateprofile'),
url(r'profile', views.profile, name='profile'),
url(r'activity', views.activity, name='profile'),
url(r'billing', views.billing, name='billing'),

url(r'^notes/list', views.listnotes, name='profile'),
url(r'^notes/add', views.addnote, name='addnote'),
url(r'^notes/delete/(?P<id>\d+)', views.deletenote, name='profile'),
url(r'^annotations/list', views.listannotation, name='profile'),
url(r'^annotations/add', views.addannotation, name='addannotation'),
url(r'^annotations/delete/(?P<id>\d+)', views.deleteannotation, name='profile'),
url(r'registeruser', views.registeruser, name='registeruser'),
url(r'search', views.search, name='search'),
url(r'signup', views.signup, name='signup'),
url(r'view', views.noteview, name='noteview'),

]
