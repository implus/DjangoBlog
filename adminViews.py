#-*- coding:utf-8 -*-
'''
Author:Refer.Con www.PHPdesigner.org
QQ:334192009
'''
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time,datetime
from django.db.models import Q
from django.db import connection
import Common,Models,settings,os,Image,hashlib
import StringIO
import django.core.files.uploadedfile

#管理员登录页面
def login(request):
    if request.POST.has_key('ok'):
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            passwordMd5 = hashlib.md5()
            passwordMd5.update(password)
            passwordNewMd5 = passwordMd5.hexdigest()
            passwordSha1 = hashlib.sha1()
            passwordSha1.update(passwordNewMd5)
            passwordNewMd5AndSha1 = passwordSha1.hexdigest()
            haveUser = Models.Manager.objects.filter(username = username,password = 
            passwordNewMd5AndSha1).count()
            if haveUser:
                response = HttpResponse()             
                response.set_cookie('username',username)
                #这里能否使用django的跳转？
                response.write("<script>window.location='/manager/'</script>")
#                response.redirect('/manager.php')
                return response
            else:
                return HttpResponseRedirect('/login/')
    return render_to_response('admin/login.html')
#默认
def default(request):
    if False == request.COOKIES.has_key('username'):
        return HttpResponseRedirect('/login/') 
    web_domain = settings.WEB_DOMAIN#域名
    if 'logout' == request.GET.get('method'):
        response = HttpResponse()
        response.delete_cookie('username')
        #这里能否使用django的跳转
        response.write("<script>window.location='/manager/'</script>")
        return response
    return render_to_response('admin/index.html',locals())
#文章列表
def adminArticle(request):
    if False == request.COOKIES.has_key('username'):
            return HttpResponseRedirect('/login/')    
    web_domain = settings.WEB_DOMAIN#域名
    keywords = request.GET.get('keywords')#搜索
    if keywords:
        articles = Models.Article.objects.order_by('-id').filter(Q(content__icontains
        = keywords) | Q(caption__icontains = keywords) | Q(times__icontains =   
        keywords) | Q(cate__cateName__icontains = keywords)).values('times',
            'cate__cateName','degree','id','caption')
        action = '&keywords='+keywords
    else:
        articles = Models.Article.objects.order_by('-id').values('times','cate__cateName',
        'degree','id','caption')
    for date in articles:
        date['times'] = time.strftime('%Y-%m-%d', time.localtime(date['times']))
    after_range_num = 2
    before_range_num = 9
    try:
       page = int(request.GET.get('page',1))
       if page < 1:
           page = 1
    except ValueError:
           page = 1
    paginator = Paginator(articles,15)
    try:
       articleList = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
       articleList = paginator.page(1)
    if page >= after_range_num:
       page_range = paginator.page_range[page - after_range_num:page + before_range_num]
    else:
       page_range = paginator.page_range[0:int(page) + before_range_num]
    if request.POST.has_key('delete'):#文章删除
        for id in request.POST.getlist('id'):
            delete = Models.Article.objects.get(id = id)
            delete.delete()
        return HttpResponseRedirect('/adminArticle/')
    return render_to_response('admin/archives.html',locals())
#增加文章
def addArticle(request):
    if False == request.COOKIES.has_key('username'):
            return HttpResponseRedirect('/login/')    
    category = Common.cate()#文章分类
    editId = request.GET.get('action')
    if not editId:
        if request.POST.has_key('ok'):
            caption = request.POST['caption']
            shortContent = request.POST['description']
            content = request.POST['content']
            tags = request.POST['tags']
            times = time.time()
            cate_id = int(request.POST['category'])
            if caption and shortContent:
                addArticle = Models.Article(caption = caption,shortContent = shortContent,
                            content = content,tags = tags,times = times,degree = 1,
                            cate_id = cate_id)
                addArticle.save()
                return HttpResponseRedirect('/addArticle/')
    else:#编辑文章
        article = Models.Article.objects.filter(id = int(editId)).values('cate_id','tags',
                'caption','content','shortContent')
        caption =  article[0]['caption']
        content = article[0]['content']
        cateId = article[0]['cate_id']
        tags = article[0]['tags']
        description = article[0]['shortContent']
        if request.POST.has_key('ok'):
            caption = request.POST['caption']
            shortContent = request.POST['description']
            content = request.POST['content']
            tags = request.POST['tags']
            times = time.time()
            cate_id = int(request.POST['category'])
            if caption and shortContent:
                Models.Article.objects.filter(id = editId).update(caption = caption,
                            shortContent = shortContent,content = content,tags = tags,
                            cate = cate_id)
                return HttpResponseRedirect('/addArticle/?action='+editId)
    return render_to_response('admin/addArticle.html',locals())

#文章分类
def articleCategories(request):
    if False == request.COOKIES.has_key('username'):
            return HttpResponseRedirect('/login/')    
    categories = Models.Categories.objects.order_by('-id').all()
    for i in categories:
        i.count = Models.Article.objects.filter(cate = i.id).count()

    return render_to_response('admin/adminArticleCategories.html',locals())
#文章分类管理
def addArticleCategories(request):
    if False == request.COOKIES.has_key('username'):
            return HttpResponseRedirect('/login/')    
    method = request.GET.get('method')
    id = request.GET.get('action')
    if not method:#增加
        if request.POST.has_key('ok'):
            cateName = request.POST['cateName']
            orderId = request.POST['orderId']
            if cateName:
                addCategory = Models.Categories(cateName = cateName,orderId = int(orderId))
                addStatus = addCategory.save()
                return HttpResponseRedirect('/articleCategories/')
    elif('edit' == method):#编辑
        category = Models.Categories.objects.filter(id = int(id)).values('cateName','orderId')
        cateName = category[0]['cateName']
        orderId = category[0]['orderId']
        if request.POST.has_key('ok'):
            cateName = request.POST['cateName']
            orderId = request.POST['orderId']
            if cateName:
                Models.Categories.objects.filter(id = int(id)).update(cateName = cateName,
                orderId = int(orderId))
                return HttpResponseRedirect('/articleCategories/')
    else:#删除
        count = Models.Article.objects.filter(cate = id).count()
        if not count:
            delete = Models.Categories.objects.get(id = int(id))
            delete.delete()
            return HttpResponseRedirect('/articleCategories/')
        else:
            return HttpResponseRedirect('/articleCategories/')
    return render_to_response('admin/addArticleCategories.html',locals())
#相册分类
def picCategories(request):
    if False == request.COOKIES.has_key('username'):
            return HttpResponseRedirect('/login/')    
    web_domain = settings.WEB_DOMAIN
    photoCategories = Models.Photocategories.objects.order_by('-id').all()
    return render_to_response('admin/photoCategories.html',locals())
#相册分类管理
def adminPhotoCategory(request):
    if False == request.COOKIES.has_key('username'):
            return HttpResponseRedirect('/login/')    
    web_domain = settings.WEB_DOMAIN
    id = request.GET.get('action')
    method = request.GET.get('method')
    if 'edit' == method:#编辑相册分类
        photoCategories = Models.Photocategories.objects.filter(id = id).values('orderId',
        'cateName','remark','bgImage')
        cateName = photoCategories[0]['cateName']
        orderId = photoCategories[0]['orderId']
        remark = photoCategories[0]['remark']
        bgImage = photoCategories[0]['bgImage']
        fileObj = request.FILES.get('file', None)
        if fileObj:#当修改封面时
            cate_name = request.POST['cate_name']
            order_id = request.POST['order']
            remark_post = request.POST['description']
            f = request.FILES.get('file', None)
            image = open(f)
            #image.thumbnail((206,155),Image.ANTIALIAS)#缩略图
            imageTime = str(time.time()).split('.')
            image.save(settings.MEDIA_ROOT+imageTime[0]+".png","png")   
            Models.Photocategories.objects.filter(id = id).update(orderId = order_id,
            cateName = cate_name,remark = remark_post,bgImage = 'upload/'+imageTime[0]+'.png')        
            if os.path.exists(settings.STATIC_ROOT+bgImage):
                os.remove(settings.STATIC_ROOT+bgImage)
                return HttpResponseRedirect('/picCategories/')
        else:#当不修改封面时
            if request.POST.has_key('ok'):
                cate_name = request.POST['cate_name']
                order_id = request.POST['order']
                remark_post = request.POST['description']
                Models.Photocategories.objects.filter(id = id).update(orderId = order_id,
                cateName = cate_name,remark = remark_post)
                return HttpResponseRedirect('/picCategories/')  
    elif 'delete' == method:#删除分类时
        cateId = request.GET.get('action')
        count = Models.Photo.objects.filter(cate = cateId).count()
        if not count:#当分类下有图片时:不能删除该分类
            delete = Models.Photocategories.objects.get(id = cateId)
            bgImage = str(delete.bgImage)
#           print bgImage
            if os.path.exists(settings.STATIC_ROOT+bgImage):
                os.remove(settings.STATIC_ROOT+bgImage)
                delete.delete()
                return HttpResponseRedirect('/picCategories/')
        else:
            return HttpResponseRedirect('/picCategories/')
    else:#添加相册分类
        if request.POST.has_key('ok'):
            if request.POST['cate_name']:
                cate_name = request.POST['cate_name']
                order_id = request.POST['order']
                remark_post = request.POST['description']
                fileObj = request.FILES.get('file', None)
                if fileObj:
                    image = open(fileObj)
                    imageTime = str(time.time()).split('.')
                    image.save(settings.MEDIA_ROOT+imageTime[0]+".png","png")
                    add = Models.Photocategories(orderId = order_id,cateName = cate_name,
                    remark = remark_post,bgImage = 'upload/'+imageTime[0]+'.png')
                    add.save()
                    return HttpResponseRedirect('/adminPhotoCategory/')
    return render_to_response('admin/adminPhotoCategory.html',locals())
#图片管理
def picManager(request):
    if False == request.COOKIES.has_key('username'):
            return HttpResponseRedirect('/login/')    
    web_domain = settings.WEB_DOMAIN
    if request.GET.get('category'):
        cateId = request.GET['category']
        photo = Models.Photo.objects.order_by('-id').filter(cate = int(cateId)).values('id',
        'picAdr','picName','picRemark','cate__cateName')
        action = "&category="+cateId 
    else:
        photo = Models.Photo.objects.order_by('-id').values('id','picAdr','picName',
        'picRemark','cate__cateName')
    after_range_num = 2
    before_range_num = 9
    try:
       page = int(request.GET.get('page',1))
       if page < 1:
           page = 1
    except ValueError:
           page = 1
    paginator = Paginator(photo,15)
    try:
       photoList = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
       articleList = paginator.page(1)
    if page >= after_range_num:
       page_range = paginator.page_range[page - after_range_num:page + before_range_num]
    else:
       page_range = paginator.page_range[0:int(page) + before_range_num]
    return render_to_response('admin/picManager.html',locals())
#图片操作(增删改)
def photoAdmin(request):
    if False == request.COOKIES.has_key('username'):
            return HttpResponseRedirect('/login/')    
    web_domain = settings.WEB_DOMAIN
    method = request.GET['method']
    photoCategories = Models.Photocategories.objects.order_by('-id').all()
    if 'edit' == method:#图片编辑
        id = request.GET['action']        
        picGet = Models.Photo.objects.get(id = int(id))
        fileObj = request.FILES.get('file', None)
        if request.POST.has_key('ok'):
            picName = request.POST['picName']
            picCategory = request.POST['category']
            picDescription = request.POST['picDescription']
            if fileObj:#当修改图片地址
                f = request.FILES.get('file', None)
                image = open(f)
                imageTime = str(time.time()).split('.')
                image.save(settings.MEDIA_ROOT+imageTime[0]+".png","png")
                picAdr = str(picGet.picAdr)
                Models.Photo.objects.filter(id = int(id)).update(cate = picCategory,
                picAdr = 'upload/'+imageTime[0]+'.png',picName = picName,picRemark = picDescription)
                if os.path.exists(settings.STATIC_ROOT+picAdr):
                    os.remove(settings.STATIC_ROOT+picAdr)
                    return HttpResponseRedirect('/photoAdmin/?method=edit&action='+id)
            else:#不修改图片地址
                Models.Photo.objects.filter(id = int(id)).update(cate = picCategory,
                picName = picName,picRemark = picDescription)
                return HttpResponseRedirect('/photoAdmin/?method=edit&action='+id)  
    elif 'add' == method:#图片增加
        fileObj = request.FILES.get('file', None)
        if request.POST.has_key('ok') and request.POST['picName']:
            picName = request.POST['picName']
            picCategory = request.POST['category']
            picDescription = request.POST['picDescription']
            f = request.FILES.get('file', None)

#data = f.file
#fs = StringIO.StringIO(data)
            fs = request.FILES['file']
            image = Image.open(fs)

#            image = open(f['content'])
            imageTime = str(time.time()).split('.')
            image.save(settings.MEDIA_ROOT+imageTime[0]+".png","png")
            photoAdd = Models.Photo(cate_id = picCategory,
            picAdr = 'upload/'+imageTime[0]+'.png',picName = picName,
            picRemark = picDescription)
            photoAdd.save()
            return HttpResponseRedirect('/photoAdmin/?method=add') 
    elif 'delete' == method:#图片删除
        id = request.GET['action']
        photoDelete = Models.Photo.objects.get(id = int(id))
        picGet = Models.Photo.objects.get(id = int(id))
        picAdr = str(picGet.picAdr)
        if os.path.exists(settings.STATIC_ROOT+picAdr):
            os.remove(settings.STATIC_ROOT+picAdr)
            photoDelete.delete()
            return HttpResponseRedirect('/picManager/') 
    return render_to_response('admin/photoAdmin.html',locals())
#友情链接
def linkAdmin(request):
    if False == request.COOKIES.has_key('username'):
            return HttpResponseRedirect('/login/')    
    web_domain = settings.WEB_DOMAIN
    links = Models.Links.objects.order_by('orderId').all()
    return render_to_response('admin/linkAdmin.html',locals())
#友情链接操作--增删改
def addLink(request):
    if False == request.COOKIES.has_key('username'):
            return HttpResponseRedirect('/login/')    
    web_domain = settings.WEB_DOMAIN
    if 'edit' == request.GET.get('method'):#修改
        linkString = '修改链接'
        id = request.GET.get('action')
        linkOne = Models.Links.objects.get(id = int(id))
        linkName = linkOne.linkName
        linkAdr = linkOne.linkAdr
        description = linkOne.linkRemark
        orderId = linkOne.orderId
        if request.POST.has_key('ok'):
            linkNamePost = request.POST['linkName']
            linkAdrPost = request.POST['linkAdr']
            descriptionPost = request.POST['description']
            orderIdPost = int(request.POST['order'])
            if linkNamePost and linkAdrPost:
                Models.Links.objects.filter(id = int(id)).update(linkName = linkNamePost,
                linkAdr = linkAdrPost,linkRemark = descriptionPost,orderId  = orderIdPost)
                return HttpResponseRedirect('/linkAdmin/')
    elif 'delete' == request.GET.get('method'):#删除
        id = request.GET.get('action')
        deleteLink = Models.Links.objects.get(id = int(id))
        deleteLink.delete()
        return HttpResponseRedirect('/linkAdmin/')            
    else:#增加
        linkString = '增加链接'  
        if request.POST.has_key('ok'):
            linkNamePost = request.POST['linkName']
            linkAdrPost = request.POST['linkAdr']
            descriptionPost = request.POST['description']
            orderIdPost = int(request.POST['order'])
            if linkNamePost and linkAdrPost:
                addLink = Models.Links(linkName = linkNamePost,linkAdr = linkAdrPost,
                linkRemark = descriptionPost,orderId  = orderIdPost) 
                addLink.save()
                return HttpResponseRedirect('/linkAdmin/')
    return render_to_response('admin/addLink.html',locals())
#管理员设置
def adminUser(request):
    if False == request.COOKIES.has_key('username'):
            return HttpResponseRedirect('/login/')    
    adminUser = Models.Manager.objects.get(id = 1)
    username = adminUser.username
    password = adminUser.password
    if request.POST.has_key('ok'):
        passwordPost = request.POST['password']
        passwordNew = request.POST['password2']
        md5 = hashlib.md5()
        md5.update(passwordPost)
        passwordMd5 = md5.hexdigest()
        sha1 = hashlib.sha1()
        sha1.update(passwordMd5)
        md5AndSha1= sha1.hexdigest()
        if passwordPost and passwordNew:
            passwordMd5 = hashlib.md5()
            passwordMd5.update(passwordNew)
            passwordNewMd5 = passwordMd5.hexdigest()
            passwordSha1 = hashlib.sha1()
            passwordSha1.update(passwordNewMd5)
            passwordNewMd5AndSha1 = passwordSha1.hexdigest()
            if password == md5AndSha1:
                Models.Manager.objects.filter(id = 1).update(password = passwordNewMd5AndSha1)
            else:
                errorString = '原始密码输入错误!'    
    
    return render_to_response('admin/adminUser.html',locals())
    
    
    
            