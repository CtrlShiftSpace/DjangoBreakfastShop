from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import *
from products.models import *
from website.constants import *
# 改用get_user_model()產生User
from django.contrib.auth import get_user_model

User = get_user_model()

class MainUserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all().order_by('name')
    serializer_class = CategoriesSerializer

    @swagger_auto_schema(
        operation_summary='取得商品類別',
        operation_description='取得商品類別',
        manual_parameters=[
            openapi.Parameter(
                    name='show_type',
                    in_=openapi.IN_QUERY,
                    description=f"商品類別內容(\
                                    {GLOBAL_CONST_API_SHOW_CATEGORY_ONLY}: 只顯示商品類別,\
                                    {GLOBAL_CONST_API_SHOW_CATEGORY_AND_PRODUCT}: 顯示商品類別與類別下商品\
                                )",
                    type=openapi.TYPE_INTEGER,
                    enum = [
                        GLOBAL_CONST_API_SHOW_CATEGORY_ONLY,
                        GLOBAL_CONST_API_SHOW_CATEGORY_AND_PRODUCT
                    ],
                )
        ]
    )
    def list(self, request, *args, **kwargs):
        show_type = request.query_params.get('show_type')
        if show_type is not None:
            show_type = int(show_type)
        if show_type == GLOBAL_CONST_API_SHOW_CATEGORY_AND_PRODUCT:
            # 顯示商品類別與類別下商品
            ret_list = Categories.catmanger.get_all_products()
            return Response(ret_list)
        else:
            # 只顯示商品類別
            all_categories = Categories.objects.all().order_by("id")
            serializer = CategoriesSerializer(all_categories, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary='新增商品類別',
        operation_description='新增商品類別',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='類別名稱'),
                'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='是否啟用'),
            },
            required=['name', 'is_active'],
        ),
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all().order_by('name')
    serializer_class = ProductSerializer

class AdditionCategoriesViewSet(viewsets.ModelViewSet):
    queryset = AdditionCategories.objects.all().order_by('name')
    serializer_class = AdditionCategoriesSerializer

    def list(self, request, *args, **kwargs):
        ret_list = AdditionCategories.addi_catmanger.get_all_additions()
        return Response(ret_list)

        # result = [
        #     {
        #         "id": "AH01",
        #         "name": "加料",
        #         "isMulti": True,
        #         "items": [
        #             {
        #                 "id": "AD011",
        #                 "name": "加蛋",
        #                 "price": 10
        #             },
        #             {
        #                 "id": "AD012",
        #                 "name": "加培根",
        #                 "price": 15
        #             },
        #             {
        #                 "id": "AD013",
        #                 "name": "加蔥花",
        #                 "price": 5
        #             },
        #             {
        #                 "id": "AD014",
        #                 "name": "加起司",
        #                 "price": 10
        #             },
        #             {
        #                 "id": "AD015",
        #                 "name": "加蔬菜",
        #                 "price": 10
        #             },
        #             {
        #                 "id": "AD016",
        #                 "name": "不要醬料",
        #                 "price": 0
        #             },
        #             {
        #                 "id": "AH017",
        #                 "name": "不要胡椒",
        #                 "price": 0
        #             }
        #         ]
        #     },
        #     {
        #         "id": "AH02",
        #         "name": "大小",
        #         "isMulti": False,
        #         "items": [
        #             {
        #                 "id": "AD021",
        #                 "name": "M",
        #                 "price": 0
        #             },
        #             {
        #                 "id": "AD022",
        #                 "name": "L",
        #                 "price": 10
        #             }
        #         ]
        #     },
        #     {
        #         "id": "AH03",
        #         "name": "溫度",
        #         "isMulti": False,
        #         "items": [
        #             {
        #                 "id": "AD031",
        #                 "name": "熱",
        #                 "price": 0
        #             },
        #             {
        #                 "id": "AD032",
        #                 "name": "溫",
        #                 "price": 0
        #             },
        #             {
        #                 "id": "AD033",
        #                 "name": "去冰",
        #                 "price": 0
        #             },
        #             {
        #                 "id": "AD034",
        #                 "name": "冰",
        #                 "price": 0
        #             }
        #         ]
        #     },
        #     {
        #         "id": "AH04",
        #         "name": "醬料",
        #         "isMulti": True,
        #         "items": [
        #             {
        #                 "id": "AD041",
        #                 "name": "番茄醬",
        #                 "price": 0
        #             },
        #             {
        #                 "id": "AD042",
        #                 "name": "芥末醬",
        #                 "price": 0
        #             },
        #             {
        #                 "id": "AD043",
        #                 "name": "辣椒醬",
        #                 "price": 0
        #             },
        #             {
        #                 "id": "AD044",
        #                 "name": "凱薩醬",
        #                 "price": 0
        #             },
        #             {
        #                 "id": "AD045",
        #                 "name": "胡麻醬",
        #                 "price": 0
        #             },
        #             {
        #                 "id": "AD046",
        #                 "name": "糖醋醬",
        #                 "price": 0
        #             }
        #         ]
        #     }
        # ]


class AdditionViewSet(viewsets.ModelViewSet):
    queryset = Additions.objects.all().order_by('id')
    serializer_class = AdditionSerializer


