#-*- coding:utf-8 -*-
'''
Author:Refer.Con www.PHPdesigner.org
QQ:334192009
'''
import settings
import Models
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time
import datetime
from django.db.models import Q
from django.db import connection
import Common,os
from django.db import connection

#默认方法
def default (request):
#	print os.path.join(os.path.dirname(__file__), 'upload')
#	print os.path.dirname(__file__)
	web_domain = settings.WEB_DOMAIN#域名
	web_name = settings.WEB_NAME#名称
	categories = Common.cate()#文章分类
	captions = Common.caption()#文章标题
	linkValues = Common.links()#友情链接
	tagValues = Common.tag()#文章标签
	category = request.GET.get('category')#GET文章分类ID
	keywords = request.GET.get('keywords')#搜索
	tags = request.GET.get('tags')#Tags
#	print dir(Models.Article.objects)
	if category:#分类
		category = int(category)
		articles = Models.Article.objects.order_by('-id').filter(cate__id = category).values(
				'times','cate__cateName','degree','id','caption','shortContent')
		action = '&category=%d'%category
	elif keywords:#搜索
		articles = Models.Article.objects.order_by('-id').filter(Q(content__icontains
			= keywords) | Q(caption__icontains = keywords) | Q(times__icontains =
			keywords)).values('times','cate__cateName','degree','id','caption',
			'shortContent')
		action = '&keywords='+keywords
	elif tags:#Tags
		articles = Models.Article.objects.order_by('-id').filter(Q(tags__icontains = tags) | 
				Q(content__icontains = tags)).values(
						'times','cate__cateName','degree','id','caption','shortContent')
		action = '&tags='+tags
	else:#默认
		articles = Models.Article.objects.order_by('-id').values('times','cate__cateName',
				'degree','id','caption','shortContent')

	for date in articles:
		year = time.strftime('%Y', time.localtime(date['times']))
		month = time.strftime('%m', time.localtime(date['times']))
		day = time.strftime('%d', time.localtime(date['times']))
		date['times'] = datetime.date(int(year),int(month),int(day))

	after_range_num = 2
	before_range_num = 9
	try:
		page = int(request.GET.get('page',1))
		if page < 1:
			page = 1
	except ValueError:
			page = 1
	paginator = Paginator(articles,6)
	try:
		articleList = paginator.page(page)
	except(EmptyPage,InvalidPage,PageNotAnInteger):
		articleList = paginator.page(1)
	if page >= after_range_num:
		page_range = paginator.page_range[page-after_range_num:page + before_range_num]
	else:
		page_range = paginator.page_range[0:int(page) + before_range_num]
#	print connection.queries
	return render_to_response('index.html',locals())
#文章详细
def action(request):
	web_domain = settings.WEB_DOMAIN#域名
	categories = Common.cate()#文章分类
	captions = Common.caption()#文章标题
	linkValues = Common.links()#友情链接
	tagValues = Common.tag()#文章标签
	id = int(request.GET.get('action'))
	article = Models.Article.objects.filter(id = id).values('times','cate__cateName',
				'degree','caption','content')
	caption_one = article[0]['caption']
	cateName_one = article[0]['cate__cateName']
	degree_one = article[0]['degree']
	degreeGo = int(degree_one) + 1
	Models.Article.objects.filter(id = id).update(degree = degreeGo)
	times = time.strftime('%Y-%m-%d',time.localtime(article[0]['times']))
	content_one = article[0]['content']
	#下一篇文章
	next = Models.Article.objects.order_by('id').filter(id__gt = id).values('id',
				'caption')[:1]
	if next:
		next_id = next[0]['id']
		next_caption = next[0]['caption']
	#上一篇文章
	previous = Models.Article.objects.order_by('-id').filter(id__lt = id).values('id',
				'caption')[:1]
	if previous:
		previous_id =  previous[0]['id']
		previous_caption = previous[0]['caption']
	return render_to_response('articleList.html',locals())
#相册
def photo(request):
	web_domain = settings.WEB_DOMAIN#域名
	web_name = settings.WEB_NAME#程序名称
	categories = Common.cate()#文章分类
	captions = Common.caption()#文章标题
	linkValues = Common.links()#友情链接
	tagValues = Common.tag()#文章标签
	photoCate = Models.Photocategories.objects.order_by('-orderId').all()
	print photoCate
	after_range_num = 2
	before_range_num = 9
	try:
		page = int(request.GET.get('page',1))
		if page < 1:
			page = 1
	except ValueError:
			page = 1
	paginator = Paginator(photoCate,18)
	try:
		photoCategories = paginator.page(page)
	except(EmptyPage,InvalidPage,PageNotAnInteger):
		photoCategories = paginator.page(1)
	if page >= after_range_num:
		page_range = paginator.page_range[page - after_range_num:page +
			before_range_num]
	else:
		page_range = paginator.page_range[0:int(page) + before_range_num]
	return render_to_response('photo.html',locals())
#相册列表
def photoList(request):
	web_domain = settings.WEB_DOMAIN#域名
	categories = Common.cate()#文章分类
	captions = Common.caption()#文章标题
	linkValues = Common.links()#友情链接
	tagValues = Common.tag()#文章标签
	id = int(request.GET.get('cateId'))
	cate = Models.Photocategories.objects.filter(id = id).values('cateName')
	cateName = cate[0]['cateName']
	photoList = Models.Photo.objects.order_by('-id').filter(cate = id).all()
	after_range_num = 2
	before_range_num = 9
	try:
		page = int(request.GET.get('page',1))
		if page < 1:
			page = 1
	except ValueError:
			page = 1
	paginator = Paginator(photoList,18)
	try:
		photo = paginator.page(page)
	except(EmptyPage,InvalidPage,PageNotAnInteger):
		photo = paginator.page(1)
	if page >= after_range_num:
		page_range = paginator.page_range[page - after_range_num:page +
			before_range_num]
	else:
		page_range = paginator.page_range[0:int(page) + before_range_num]
	action = '&cateId=%d'%id
	return render_to_response('photoList.html',locals())
#图片详细
def photoShow(request):
	web_domain = settings.WEB_DOMAIN#域名
	categories = Common.cate()#文章分类
	captions = Common.caption()#文章标题
	linkValues = Common.links()#友情链接
	tagValues = Common.tag()#文章标签
	id = int(request.GET.get('id'))
	nonePhoto = Models.Photo.objects.filter(id = id).values('picAdr','picRemark',
			'id','picName')
	nonePhoto_one = nonePhoto[0]['picAdr']
	nonePicRemark_one = nonePhoto[0]['picRemark']
	nonePicName_one = nonePhoto[0]['picName']
	previous = Models.Photo.objects.order_by('-id').filter(id__lt = id).values('id',
			'picName')[:1]
	if previous:
		previous_id = previous[0]['id']
		previous_picName = previous[0]['picName']
	next = Models.Photo.objects.order_by('id').filter(id__gt = id).values('id',
			'picName')[:1]
	if next:
		next_id = next[0]['id']
		next_picName = next[0]['picName']
	return render_to_response('photoShow.html',locals())