from django.contrib import admin

# 資料表
from .models import Products, MainUser


# 註冊(register)資料表到後台
admin.site.register(Products)
admin.site.register(MainUser)
