#! /usr/bin/env python
#coding=utf-8
#文章分类
import Models
def cate():
    categories = Models.Categories.objects.order_by('orderId').all()
    return categories
#文章标题
def caption():
    caption = Models.Article.objects.order_by('-id').values('id','caption')[:20]
    return caption
#友情链接
def links():
    links = Models.Links.objects.order_by('-orderId').all()
    return links
#标签
def tag():
    tags = Models.Article.objects.order_by('-id').values('tags','caption')
    info = []
    for  tagsValues in tags:
        if tagsValues['tags']:
            tag = tagsValues['tags']
            info.append(tag)
    str = ','.join(info)
    str = str.split(',')
    return set(str)
