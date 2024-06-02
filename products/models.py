from django.db import models

# 商品分類
class Categories(models.Model):
    name = models.CharField(max_length=64, unique=True)
    # 是否啟用
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.name

# 商品
class Products(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    content = models.TextField(null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# 商品所屬分類
class CategoryProducts(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

# 商品追加項目
class Additions(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField(default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# 商品包含追加項目
class ProductAdditions(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    addition = models.ForeignKey(Additions, on_delete=models.CASCADE)








