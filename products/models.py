from django.db import models

# 商品分類
class Categories(models.Model):
    name = models.CharField(max_length=64, unique=True)
    # 是否啟用
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name

# 商品
class Products(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    content = models.TextField(null=True)
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

    class Meta:
        db_table = 'addition_categories'


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










