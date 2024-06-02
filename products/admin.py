from django.contrib import admin

# 資料表
from .models import Products

# 註冊(register)資料表到後台
admin.site.register(Products)
