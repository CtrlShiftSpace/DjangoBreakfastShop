from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.models import User
from .serializers import CategoriesSerializer, ProductSerializer, UserSerializer, AdditionSerializer
from products.models import Categories, Products, Additions


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all().order_by('name')
    serializer_class = CategoriesSerializer

    def list(self, request, *args, **kwargs):
        queryset = Categories.objects.all().order_by('name')
        serializer = CategoriesSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='類別名稱'),
                'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='是否啟用'),
            },
            required=['name', 'is_active'],
        ),
        responses={201: CategoriesSerializer()}
    )
    def create(self, request, *args, **kwargs):
        # action = request.data.get('action', None)
        # if action == 'special_action':
        #     pass

        return super().create(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all().order_by('name')
    serializer_class = ProductSerializer

class AdditionViewSet(viewsets.ModelViewSet):
    queryset = Additions.objects.all().order_by('name')
    serializer_class = AdditionSerializer

    # 先自定義方法
    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        # serializer = self.get_serializer(queryset, many=True)
        # result = [ x.values()[0] for x in serializer.data ]
        result = [
            {
                "id": "AH01",
                "name": "加料",
                "isMulti": True,
                "items": [
                    {
                        "id": "AD011",
                        "name": "加蛋",
                        "price": 10
                    },
                    {
                        "id": "AD012",
                        "name": "加培根",
                        "price": 15
                    },
                    {
                        "id": "AD013",
                        "name": "加蔥花",
                        "price": 5
                    },
                    {
                        "id": "AD014",
                        "name": "加起司",
                        "price": 10
                    },
                    {
                        "id": "AD015",
                        "name": "加蔬菜",
                        "price": 10
                    },
                    {
                        "id": "AD016",
                        "name": "不要醬料",
                        "price": 0
                    },
                    {
                        "id": "AH017",
                        "name": "不要胡椒",
                        "price": 0
                    }
                ]
            },
            {
                "id": "AH02",
                "name": "大小",
                "isMulti": False,
                "items": [
                    {
                        "id": "AD021",
                        "name": "M",
                        "price": 0
                    },
                    {
                        "id": "AD022",
                        "name": "L",
                        "price": 10
                    }
                ]
            },
            {
                "id": "AH03",
                "name": "溫度",
                "isMulti": False,
                "items": [
                    {
                        "id": "AD031",
                        "name": "熱",
                        "price": 0
                    },
                    {
                        "id": "AD032",
                        "name": "溫",
                        "price": 0
                    },
                    {
                        "id": "AD033",
                        "name": "去冰",
                        "price": 0
                    },
                    {
                        "id": "AD034",
                        "name": "冰",
                        "price": 0
                    }
                ]
            },
            {
                "id": "AH04",
                "name": "醬料",
                "isMulti": True,
                "items": [
                    {
                        "id": "AD041",
                        "name": "番茄醬",
                        "price": 0
                    },
                    {
                        "id": "AD042",
                        "name": "芥末醬",
                        "price": 0
                    },
                    {
                        "id": "AD043",
                        "name": "辣椒醬",
                        "price": 0
                    },
                    {
                        "id": "AD044",
                        "name": "凱薩醬",
                        "price": 0
                    },
                    {
                        "id": "AD045",
                        "name": "胡麻醬",
                        "price": 0
                    },
                    {
                        "id": "AD046",
                        "name": "糖醋醬",
                        "price": 0
                    }
                ]
            }
        ]

        return Response(result)


