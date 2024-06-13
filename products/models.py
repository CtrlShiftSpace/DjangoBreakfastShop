from django.db import models
from django.db.models import F
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from website.utils import *

class MainUserManager(BaseUserManager):
    # 一般使用者
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 定義創建管理員的函式
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

# 商品分類 Manager
class CategoriesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    # 取得類別下所有商品
    def get_all_products(self):
        order_field = 'id'
        ret_list = []
        all_categories = Categories.objects.only('id', 'name', 'is_active').order_by(order_field)
        for category in all_categories:
            products = category.products_set.all().annotate(product_id=F('id'))
            prod_list = []
            for product in products:
                # 檢查商品圖片
                img_url = ""
                if product.img and hasattr(product.img, 'url'):
                    img_url = product.img.url

                prod_dict = {
                    'product_id': product.product_id,
                    'name': product.name,
                    'price': product.price,
                    'content': product.content,
                    'img': img_url,
                    'addition_ids': list(product.additions_set.only('id').values_list('id', flat=True)),
                }
                prod_list.append(prod_dict)

            cat_dict = {
                'id': category.id,
                'name': category.name,
                'products': prod_list,
            }
            ret_list.append(cat_dict)
            # print(additions)
        return ret_list

# 商品分類 Manager
class AdditionCategoriesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    # 取得類別下所有商品
    def get_all_additions(self):
        order_field = 'id'
        ret_list = []
        all_addi_cat = AdditionCategories.objects.order_by(order_field)
        for addi_cat in all_addi_cat:
            addi_dict = {
                'id': addi_cat.id,
                'name': addi_cat.name,
                'is_multiple': addi_cat.is_multiple,
                'is_active': addi_cat.is_active,
                'additions': list(addi_cat.additions_set.values('id', 'name', 'price', 'is_active')),
            }
            ret_list.append(addi_dict)
            # print(additions)
        return ret_list


class MainUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MainUserManager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS 不用包含 USERNAME_FIELD欄位 和 password
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'main_users'

    def __str__(self):
        return self.username

# 商品分類
class Categories(models.Model):
    name = models.CharField(max_length=64, unique=True)
    # 是否啟用
    is_active = models.BooleanField(default=False)
    # 預設的Manager
    objects = models.Manager()
    # 另外建立一個新的Manager
    catmanger = CategoriesManager()

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name

# 商品
class Products(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    content = models.TextField(null=True)
    img = models.ImageField(upload_to=MediaPathAndRename('products/'), null=True, blank=True)
    is_active = models.BooleanField(default=False)
    categories = models.ManyToManyField(Categories, through='CategoryProducts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name

# 商品所屬分類
class CategoryProducts(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    class Meta:
        db_table = 'category_products'


# 追加項目分類
class AdditionCategories(models.Model):
    name = models.CharField(max_length=64)
    # 是否可多選
    is_multiple = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    # 預設的Manager
    objects = models.Manager()
    # 另外建立一個新的Manager
    addi_catmanger = AdditionCategoriesManager()

    class Meta:
        db_table = 'addition_categories'

    def __str__(self):
        return self.name


# 商品追加項目
class Additions(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField(default=0)
    is_active = models.BooleanField(default=False)
    products = models.ManyToManyField(Products, through='ProductAdditions')
    addition_categories = models.ForeignKey(AdditionCategories, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'additions'

    def __str__(self):
        return self.name

# 商品包含追加項目
class ProductAdditions(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    addition = models.ForeignKey(Additions, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_additions'










