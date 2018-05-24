from django.conf.urls import url
from . import views        
   # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.signin),
    url(r'^register$', views.register),
    url(r'^reg$', views.reg),
    url(r'^login$', views.login), 
    url(r'^dashboard$', views.user_dashboard),
    url(r'^dashboard/admin$', views.admin_dashboard), 
    url(r'^logout$', views.logout),
    url(r'^users/new$', views.usersnew), 
    url(r'^create$', views.create),
    url(r'^users/edit/(?P<id>\d+)$', views.edit),
    url(r'^users/edit/(?P<id>\d+)/info', views.edit_info),
    url(r'^users/edit/password', views.edit),   #do i need this line??
    url(r'^users/remove/(?P<id>\d+)', views.remove),
    url(r'^users/show/(?P<id>\d+)$', views.usershow),
    # url(r'^users/edit$', views.normal_edit),
    url(r'^users/edit/(?P<id>\d+)/password', views.edit_password),
    url(r'^users/edit/(?P<id>\d+)/normalname', views.edit_normalname),
    url(r'^users/edit/normal/(?P<id>\d+)$', views.normal_edit),
    
    url(r'^users/edit/(?P<id>\d+)/normalpassword', views.edit_normalpassword),
    url(r'^users/edit/(?P<id>\d+)/normaldescription', views.edit_normaldescription),
    url(r'^users/wall/(?P<id>\d+)$', views.wall),
    url(r'^users/comment/(?P<id>\d+)$', views.comment), 

    url(r'^users/edit/admin/(?P<id>\d+)$', views.edit_admin),
    ]