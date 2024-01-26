from django.db import models
from django.contrib.auth.models import Group
import uuid
from django.conf import settings

class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
       abstract = True
       


class Role(Group):

    class Meta:
        proxy = True
        verbose_name = verbose_name_plural = "Role & Permissions"
    
    def get_users(self):
        return self.user_set.all()



class Category(TimeStampedMixin):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self) -> str:
        return self.name


class SubCategory(TimeStampedMixin):
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Sub_Categories"
    def __str__(self) -> str:
        return self.name


class Sizes(TimeStampedMixin):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Size"

    def __str__(self) -> str:
        return self.name


class ForSeason(TimeStampedMixin):
    for_season = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        verbose_name_plural = "For Season"

    def __str__(self) -> str:
        return self.for_season
    

class Product(TimeStampedMixin):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    season = models.ForeignKey(ForSeason, on_delete=models.CASCADE,related_name = 'Season_Special', null=True, default="All")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name = 'sub_category', null=False, blank=False)
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    size_available = models.ManyToManyField(Sizes,blank=True)
    is_available = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self) -> str:
        return f'{self.uid}'


class ProductReviews(TimeStampedMixin):
    RATING_CHOICES = (
        ("1" , "1"),
        ("2" , "2"),
        ("3" , "3"),
        ("4" , "4"),
        ("5" , "5"),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name = "product", null=True)
    rating = models.CharField(max_length=50, choices=RATING_CHOICES)
    customer_review = models.TextField()
    class Meta:
        verbose_name_plural = "Reviews"

    def __str__(self) -> str:
        return self.product.name
    




class Customer(TimeStampedMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=70)
    class Meta:
        verbose_name_plural = "Customers"

    def __str__(self) -> str:
        return self.email
    

class Address(TimeStampedMixin):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=70)
    postal_code = models.IntegerField()
    street = models.IntegerField()
    complete_address = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self) -> str:
        return self.customer.email

class Order(TimeStampedMixin):
    PAYMENT_TYPES = (
        ("Cash On Delevery" , "Cash On Delivery"),
        ("Online Payment" , "Online Payment"),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name = "customer")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_product")
    product_size = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(null=True)
    discount = models.IntegerField(default=0)
    shipping_date = models.DateField(null=True)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPES, null=True)
    class Meta:
        verbose_name_plural = "Orders"

    def __str__(self) -> str:
        return self.customer.email
