from django.urls import path, re_path
from .views import *
from rest_framework_simplejwt.views import TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('order/', OrderAPiView.as_view(), name='order'),
    path('signup/', SignUpAPIView.as_view(), name='SignUp'),
    path('reset-password/', SendPasswordResetEmailView.as_view(), name='reset-password'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/verify', TokenVerifyView.as_view(), name='token_refresh'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('home/', dashboard),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

