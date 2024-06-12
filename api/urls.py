from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.MainUserViewSet)
router.register(r'categories', views.CategoriesViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'additions/categories', views.AdditionCategoriesViewSet)
router.register(r'additions', views.AdditionViewSet)

app_name = 'api'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]