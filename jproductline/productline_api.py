# coding: utf-8

from Crypto.PublicKey import RSA
from subprocess import call

from jproductline.models import ProductLine,Department
from jumpserver.api import *
from jumpserver.settings import BASE_DIR, EMAIL_HOST_USER as MAIL_FROM



def db_add_productline(**kwargs):
    """
    add a product line in database
    数据库中添加产品线
    """
    productline = ProductLine(**kwargs)
    productline.save()

def db_del_productline(productlinename):
    """
        数据库删除产品线
    """
    productline = get_object(ProductLine, name=productlinename)
    if productline:
        productline.delete()

def db_add_department(**kwargs):
    """
        add a product line in database
        数据库中添加部门
        """
    department = Department(**kwargs)
    department.save()


def db_del_department(departmentname):
    """
        数据库删除部门
    """
    department = get_object(Department, name=departmentname)
    if department:
        department.delete()