
from django.conf.urls import url
from . import views
app_name="api"
urlpatterns = [
url(r'^$', views.index, name='index'),
url(r'v1/token', views.index, name='index'),
url(r'v1/register', views.registeruser, name='registeruser'),
url(r'v1/devicelog', views.index, name='devicelog'),
url(r'v1/log', views.index, name='log'),
url(r'v1/auth', views.auth, name='auth'),
url(r'v1/articles', views.listarticles, name='listarticles'),
url(r'v1/verify', views.verify, name='verify'),
url(r'v1/confirm', views.confirm, name='confirm'),
url(r'v1/user', views.index, name='user'),
url(r'v1/products', views.index, name='listproducts'),

url(r'v1/getupdates', views.index, name='authors'),
url(r'v1/fetchupdates', views.index, name='authors'),

url(r'v1/publishers', views.index, name='publishers'),
url(r'v1/license_validate', views.index, name='license_validate'),

url(r'v1/notes/list', views.listnotes, name='profile'),
url(r'v1/notes/add', views.addnote, name='profile'),
url(r'v1/notes/delete', views.deletenote, name='profile'),

url(r'v1/annotations/list', views.listannotations, name='profile'),
url(r'v1/annotations/add', views.addannotation, name='profile'),
url(r'v1/annotations/delete', views.deleteannotation, name='profile'),
]
