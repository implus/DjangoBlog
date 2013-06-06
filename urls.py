#-*- coding:utf-8 -*-
from django.conf.urls import *
#from DjangoBlog import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
import settings
urlpatterns = patterns('',
    # Example:
    (r'^$', 'DjangoBlog.views.default'),
    (r'^action/','DjangoBlog.views.action'),
    (r'^photoList/','DjangoBlog.views.photoList'),
    (r'^photoShow/','DjangoBlog.views.photoShow'),
    (r'^photo/','DjangoBlog.views.photo'),
    (r'^manager/','DjangoBlog.adminViews.default'),
    (r'^adminArticle/','DjangoBlog.adminViews.adminArticle'),
    (r'^addArticleCategories/','DjangoBlog.adminViews.addArticleCategories'),
    (r'^addArticle/','DjangoBlog.adminViews.addArticle'),
    (r'^articleCategories/','DjangoBlog.adminViews.articleCategories'),
    (r'^picCategories/','DjangoBlog.adminViews.picCategories'),
    (r'^picManager/','DjangoBlog.adminViews.picManager'),
    (r'^photoAdmin/','DjangoBlog.adminViews.photoAdmin'),
    (r'^linkAdmin/','DjangoBlog.adminViews.linkAdmin'),
    (r'^addLink/','DjangoBlog.adminViews.addLink'),
    (r'^adminUser/','DjangoBlog.adminViews.adminUser'),
    (r'^login','DjangoBlog.adminViews.login'),
   
#    django.views.static.serve对于静态文件的处理，
#    这种方法是低效且不安全，不要在生产环境使用此方法，
#    只在开发环境使用
#    只能使用Web服务器来处理
    (r'^adminPhotoCategory/','DjangoBlog.adminViews.adminPhotoCategory'),
    (r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    (r'^(?P<path>.*)$','django.views.static.serve',{'document_root':settings.ADMIN_HTML_ROOT}),
    # (r'^DjangoBlog/', include('DjangoBlog.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
