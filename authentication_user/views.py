from django.shortcuts import render, HttpResponse
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.translation import gettext as _
from rest_framework.pagination import PageNumberPagination



class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [IsAuthenticated]

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        return Response({"detail": "Successfully logged out."})



User = get_user_model()

class SignUpAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response_data = {
                'user_id': user.id,
                'email': user.email,
                'access_token': access_token,
                'refresh_token': refresh_token,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SendPasswordResetEmailView(APIView):
  permission_classes = [AllowAny]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)



class UserPasswordResetView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 10


class ProductListAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LargeResultsSetPagination
    
    def create(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ProductDetailAPIView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self, request, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        product = self.get_object(request, pk)
        serializer = self.get_serializer(product)
        return Response(serializer.data)
 


class OrderAPiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data["product"]
        product_size = request.data["size"]
        customer_id = request.data["customer"]
        quantity = request.data["quantity"]
        total_price = request.data["total_price"]
        discount = request.data["discount"]
        shipping_date = request.data["shipping_date"]
        payment_type = request.data["payment_type"]
        customer = Customer.objects.get(id=customer_id)
        for id_ in product_id:
            product = Product.objects.get(uid=id_)
            order = Order.objects.create(customer=customer, product=product, quantity=quantity, product_size=product_size
                                ,total_price=total_price, payment_type=payment_type, discount=discount, shipping_date=shipping_date)
        return Response({"messege":"Order Saved Successfully", "status":status.HTTP_200_OK})
    



def dashboard(request):
    qs = Category.objects.all()
    return render(request, "dashboard.html", {"qs":qs})