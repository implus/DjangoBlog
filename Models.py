#-*- coding:utf-8 -*-
#数据模型
from django.db import models
import time
class Categories(models.Model):
	orderId = models.IntegerField()
	cateName = models.CharField(max_length = 50)

	class Meta:
		db_table = 'categories'

	def __str__(self):
		#return self.name
		return '%s %s' % (self.orderId,self.cateName)

class Article(models.Model):
	cate = models.ForeignKey(Categories)#,db_column = 'cate_id', to_field = 'id'
	caption = models.CharField(max_length = 100)
	shortContent = models.TextField()
	content = models.TextField()
	tags = models.TextField()
	times = models.IntegerField()
	date = models.CharField(max_length = 50)
	degree = models.IntegerField()
	#cid = models.IntegerField(db_column = 'cate_id')#db_column = 'cid'我被这里害惨了，加上它数据只能出不能进
	password = models.CharField(max_length = 200)

	class Meta:
		db_table = 'article'


	def __str__(self):
		return '%s %s %s %s %s %s %s %s %s %s' % (self.cate,self.caption,self.shortContent,self.content,
		self.tags,self.times,self.date,self.degree,self.cate_id,self.password)


class Links(models.Model):
	linkName = models.CharField(max_length = 50)
	linkAdr = models.URLField()
	linkRemark = models.CharField(max_length = 50)
	orderId = models.IntegerField()

	class Meta:
		db_table = 'links'

	def __str__(self):
		return '%s %s ' % (self.linkName,self.linkAdr)


class Manager(models.Model):
	username = models.CharField(max_length = 200)
	password = models.CharField(max_length = 200)
	
	class Meta:
			db_table = 'manager'


class Photocategories(models.Model):
	orderId = models.IntegerField()
	cateName = models.CharField(max_length = 50)
	remark = models.CharField(max_length = 200)
	bgImage = models.ImageField()
	class Meta:
		db_table = 'photocategories'


class Photo(models.Model):
	#cate_id = models.IntegerField()
	picAdr = models.ImageField(upload_to='upload/',blank=True,null=True)
	picName = models.CharField(max_length = 200)
	picRemark = models.CharField(max_length = 200)
	cate = models.ForeignKey(Photocategories)

	class Meta:
		db_table = 'photo'

	def __str__ (self):
		return '%s %s %s %s '%(self.cate_id,self.picAdr,self.picName,self.picRemark)
