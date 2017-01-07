# coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from productline_api import *
# Create your views here.

@require_role(role='super')
def department_list(request):
    """
        部门列表
    """
    header_title, path1, path2 = '查看部门', '组织管理', '查看部门'
    keyword = request.GET.get('search', '')
    department_list = Department.objects.all().order_by('name')
    department_id = request.GET.get('id', '')
    if keyword:
        department_list = department_list.filter(Q(name__icontains=keyword) | Q(comment__icontains=keyword))

    if department_id:
        department_list = department_list.filter(id=int(department_id))

    department_list, p, departments, page_range, current_page, show_first, show_end = pages(department_list, request)
    return my_render('jproductline/department_list.html', locals(), request)

@require_role(role='super')
def department_add(request):
    """
    添加部门的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '添加部门', '组织管理', '添加部门'
    department_all = Department.objects.all()

    if request.method == 'POST':
        department_name = request.POST.get('department_name', '')
        comment = request.POST.get('comment', '')

        try:
            if not department_name:
                error = u'部门名称 不能为空'
                raise ServerError(error)

            if Department.objects.filter(name=department_name):
                error = u'部门名称已存在'
                raise ServerError(error)
            db_add_department(name=department_name, comment=comment)
        except ServerError:
            pass
        except TypeError:
            error = u'添加部门失败'
        else:
            msg = u'添加部门 %s 成功' % department_name

    return my_render('jproductline/department_add.html', locals(), request)

@require_role(role='super')
def department_edit(request):
    """
    修改部门
    :param request:
    :return:
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '编辑部门', '组织管理', '编辑部门'

    if request.method == 'GET':
        department_id = request.GET.get('id', '')
        department = get_object(Department, id=department_id)
        # user_group = UserGroup.objects.get(id=group_id)
        department_all = Department.objects.all()

    elif request.method == 'POST':
        department_id = request.POST.get('department_id', '')
        department_name = request.POST.get('department_name', '')
        comment = request.POST.get('comment', '')

        try:
            if '' in [department_id, department_name]:
                raise ServerError('组名不能为空')

            if len(Department.objects.filter(name=department_name)) > 1:
                raise ServerError(u'%s 部门已存在' % department_name)
            # add user group
            department = get_object_or_404(Department, id=department_id)
            department.name = department_name
            department.comment = comment
            department.save()
        except ServerError, e:
            error = e

        if not error:
            return HttpResponseRedirect(reverse('department_list'))
        else:
            department_all = Department.objects.all()
            department_selected = Department.objects.filter(department=department)

    return my_render('jproductline/department_edit.html', locals(), request)

@require_role(role='super')
def department_del(request):
    """
    del a group
    删除部门
    """
    department_ids = request.GET.get('id', '')
    department_id_list = department_ids.split(',')
    for department_id in department_id_list:
        Department.objects.filter(id=department_id).delete()

    return HttpResponse('删除成功')

@require_role(role='super')
def productline_add(request):
    """
    添加产品线的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '添加产品线', '组织管理', '添加产品线'

    productline_all = ProductLine.objects.all()
    department_all = Department.objects.all()
    if request.method == 'POST':
        productline_name = request.POST.get('productline_name', '')
        department_name = request.POST.get('department', '')
        comment = request.POST.get('comment', '')
        #department = Department.objects.filter(name=unicode(department_name))[0]
        department = get_object(Department,name=department_name)
        try:
            if not productline_name:
                error = u'产品线名称 不能为空'
                raise ServerError(error)

            if ProductLine.objects.filter(name=productline_name):
                error = u'产品线名称已存在'
                raise ServerError(error)
            if not department:
                error = u'部门名称 不能为空，清先添加部门'
            db_add_productline(name=productline_name, department=department, comment=comment)
        except ServerError:
            pass
        except TypeError:
            error = u'添加产品线失败'
        else:
            msg = u'添加产品线 %s 成功' % productline_name

    return my_render('jproductline/productline_add.html', locals(), request)

@require_role(role='super')
def productline_list(request):
    """
        产品线列表
    """
    header_title, path1, path2 = '查看产品线', '组织管理', '查看产品线'
    keyword = request.GET.get('search', '')
    department_name = request.GET.get('department_name','')
    productline_list = ProductLine.objects.all().order_by('name')
    department_all = Department.objects.all()
    if keyword:
        productline_list = productline_list.filter(Q(name__icontains=keyword) | Q(comment__icontains=keyword))

    if department_name:
        productline_list = productline_list.filter(department=department_all.filter(name=department_name))

    productline_list, p, productlines, page_range, current_page, show_first, show_end = pages(productline_list, request)
    return my_render('jproductline/productline_list.html', locals(), request)

@require_role(role='super')
def productline_edit(request):
    """
    修改产品线
    :param request:
    :return:
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '编辑产品线', '组织管理', '编辑产品线'

    if request.method == 'GET':
        productline_id = request.GET.get('id', '')
        productline = get_object(ProductLine, id=productline_id)
        department_all = Department.objects.all()

    elif request.method == 'POST':
        productline_id = request.POST.get('productline_id', '')
        productline_name = request.POST.get('productline_name', '')
        department_name = request.POST.get('department', '')
        comment = request.POST.get('comment', '')
        department = get_object(Department, name=department_name)
        try:
            if '' in [productline_id, productline_name]:
                raise ServerError('产品线名称不能为空')

            if len(ProductLine.objects.filter(name=productline_name)) > 1:
                raise ServerError(u'%s 产品线已存在' % productline_name)
            # add user group
            productline = get_object_or_404(ProductLine, id=productline_id)
            productline.name = productline_name
            productline.department = department
            productline.comment = comment
            productline.save()
        except ServerError, e:
            error = e

        if not error:
            return HttpResponseRedirect(reverse('productline_list'))
        else:
            productline_all = ProductLine.objects.all()
            #productline_selected = ProductLine.objects.filter(productline=productline)

    return my_render('jproductline/productline_edit.html', locals(), request)

@require_role(role='super')
def productline_del(request):
    """
    del a group
    删除产品线
    """
    productline_ids = request.GET.get('id', '')
    productline_id_list = productline_ids.split(',')
    for productline_id in productline_id_list:
        ProductLine.objects.filter(id=productline_id).delete()

    return HttpResponse('删除成功')