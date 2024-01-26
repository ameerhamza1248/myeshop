from rest_framework import serializers
from .models import *
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import *
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode




User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    main_category = CategorySerializer(read_only=True)
    class Meta:
        model = SubCategory
        fields = "__all__"



class ForSeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForSeason
        fields = "__all__"

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(read_only=True)
    season = ForSeasonSerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
  product_serializer = ProductSerializer(read_only=True)
  
  class Meta:
    model = Order
    fields = "__all__"



class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://0.0.0.0:8000/api/user/reset-password/'+uid+'/'+token+'/'
      print('Password Reset Link', link)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')




class UserPasswordResetSerializer(serializers.Serializer):
  password1 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password1', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password1')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      data = {
        'subject':'Reset Your Password Successfully',
        'body':"body",
        'to_email':user.email
      }
      send_email(data)
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      raise serializers.ValidationError('Token is not Valid or Expired')
   