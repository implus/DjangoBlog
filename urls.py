#-*- coding:utf-8 -*-
from django.conf.urls.defaults import *
from blog import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
import settings
urlpatterns = patterns('',
    # Example:
    (r'^$', 'blog.views.default'),
    (r'^action/','blog.views.action'),
    (r'^photoList/','blog.views.photoList'),
    (r'^photoShow/','blog.views.photoShow'),
    (r'^photo/','blog.views.photo'),
    (r'^manager/','blog.adminViews.default'),
    (r'^adminArticle/','blog.adminViews.adminArticle'),
    (r'^addArticleCategories/','blog.adminViews.addArticleCategories'),
    (r'^addArticle/','blog.adminViews.addArticle'),
    (r'^articleCategories/','blog.adminViews.articleCategories'),
    (r'^picCategories/','blog.adminViews.picCategories'),
    (r'^picManager/','blog.adminViews.picManager'),
    (r'^photoAdmin/','blog.adminViews.photoAdmin'),
    (r'^linkAdmin/','blog.adminViews.linkAdmin'),
    (r'^addLink/','blog.adminViews.addLink'),
    (r'^adminUser/','blog.adminViews.adminUser'),
    (r'^login','blog.adminViews.login'),
   
#    django.views.static.serve对于静态文件的处理，
#    这种方法是低效且不安全，不要在生产环境使用此方法，
#    只在开发环境使用
#    只能使用Web服务器来处理
    (r'^adminPhotoCategory/','blog.adminViews.adminPhotoCategory'),
    (r'^(?!admin)(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    (r'^(?P<path>.*)$','django.views.static.serve',{'document_root':settings.ADMIN_HTML_ROOT}),
    # (r'^blog/', include('blog.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
