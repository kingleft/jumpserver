from django.conf.urls import patterns, include, url
from jumpserver.api import view_splitter
from jproductline.views import *

urlpatterns = patterns('jproductline.views',
                       # Examples:
                       # url(r'^$', 'jumpserver.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       #url(r'^group/add/$', 'group_add', name='user_group_add'),
                        url(r'^department/list/$', 'department_list', name='department_list'),
                        url(r'^department/add/$', 'department_add', name='department_add'),
                        url(r'^department/del/$', 'department_del', name='department_del'),
                        url(r'^department/edit/$', 'department_edit', name='department_edit'),
                        url(r'^productline/add/$', 'productline_add', name='productline_add'),
                        url(r'^productline/list/$', 'productline_list', name='productline_list'),
                        url(r'^productline/del/$', 'productline_del', name='productline_del'),
                        url(r'^productline/edit/$', 'productline_edit', name='productline_edit'),
                       )
