from django.db import models
from django.shortcuts import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
import string, random
from django.db import IntegrityError
from ckeditor.fields import RichTextField
from django.utils import timezone
from PIL import Image

# Create your models here.
class SiteLogo(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to='siteLogo')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Site Logo"
    

class ProductCategory(models.Model):
    category_name = models.CharField(max_length=100, blank=True, null=True)
    show_status = models.BooleanField(default=False)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    img = models.ImageField(upload_to='CategoryImg', blank=True, null=True)
    slug = models.SlugField(max_length = 100, unique=True, blank=True, null=True) 

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        try:
            self.slug =''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(49))
            super().save(*args, **kwargs)           
        except IntegrityError:
            self.save(*args, **kwargs)

    def get_category_update_url(self):
        return reverse('category-update', kwargs={'slug': self.slug})
    
    class Meta:
        verbose_name_plural = "Product Category"


class Brand(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='brandImg')
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    show_status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    def get_brand_update_url(self):
        return reverse('brand-update', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        try:
            self.slug =''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(49))
            super().save(*args, **kwargs)           
        except IntegrityError:
            self.save(*args, **kwargs)


class Banner(models.Model):   
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='bannerImg')
    http_url_link = models.URLField(max_length = 200, blank=True, null=True)
    

    def __str__(self):
        return self.title



class PriceRange(models.Model):
    price_range  = models.CharField(max_length=100, unique=True)
    ordering = models.IntegerField()

    class Meta:
        ordering =['ordering']
        verbose_name = 'Price Range'
        verbose_name_plural = 'Price Range'

    def __str__(self):
        return self.price_range



class Product(models.Model):
    name = models.CharField(max_length=100)
    categoris = models.ForeignKey(ProductCategory, verbose_name='Product Category', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='productImg')
    hover_image = models.ImageField(upload_to="hoverProductImage", default="https://th.bing.com/th/id/OIP.oWPLGwKQFynuDWH43wlwgAHaLH?w=215&h=322&c=7&o=5&pid=1.7")
    regular_price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    details = RichTextUploadingField()
    stock_quantity = models.PositiveIntegerField(default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    
        
    def __str__(self):
        return self.name


class CartProduct(models.Model): 
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)


    def get_total_per_product(self):
        if self.product.discount_price:
            return self.product.discount_price * self.quantity
        else:
            return self.product.regular_price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    class Meta:
        ordering = ['-id']


class Order(models.Model): 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    products = models.ManyToManyField(CartProduct)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField()
    
    
    def __str__(self):
        return self.user.email
    
    def get_total_all_product(self):
        sum = 0
        for x in self.products.all():
            sum += x.get_total_per_product()
        return sum
    
    def get_grand_total(self):
        self.tax = 10
        self.shipping = 0
        total = self.get_total_all_product()  + self.tax + self.shipping
        return total

    class Meta:
        ordering = ['-id']


class Coupon(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField(default=timezone.now)
    max_value = models.IntegerField(validators=[MaxValueValidator(100)], verbose_name='Coupon Quantity', null=True) # No. of coupon
    used = models.IntegerField(default=0)
    
    def __str__(self):
        return self.code

    def get_coupon_update_url(self):
        return reverse('coupon-update', kwargs={'pk': self.pk})
   
#WishListMOdel

class WhishLIst(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wish_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    slug = models.CharField(max_length=100,unique=True,blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username + ' ' + self.wish_product.product_name

    def save(self, *args, **kwargs):
        try:
            self.slug =''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(49))
            super().save(*args, **kwargs)           
        except IntegrityError:
            self.save(*args, **kwargs)


class FlashSale(models.Model):
    title = models.CharField(max_length = 150)  
    FlashSaleOn_date  = models.DateTimeField(default=timezone.now)
    FlashSale_expire_date   = models.DateTimeField()
      
    class Meta:
        verbose_name = 'FlashSale'
        verbose_name_plural = 'FlashSales'

    def __str__(self):
        return str(self.FlashSale_expire_date)


class Campaign(models.Model):
    campaign_name = models.CharField(max_length = 150)
    
    class Meta:
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaign Category'

    def __str__(self):
        return self.campaign_name


class CampaignProduct(models.Model):
    campaign_category  = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
     
    class Meta:
        verbose_name = 'CampaignProduct'
        verbose_name_plural = 'CampaignProduct'

    def __str__(self):
        return self.campaign_category.campaign_name + " / " + self.product.product_name


class DealOfTheDayProduct(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
     
    class Meta:
        verbose_name = 'Deal Of The Day'
        verbose_name_plural = 'Deal Of The Day'

    def __str__(self):
        return self.product.product_name


class ProductReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    RATING =(
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5)
    )
    rating  = models.IntegerField(choices=RATING, default=5)
    review = models.TextField()
    image = models.ImageField(upload_to='ReviewImg', blank=True, null=True)
    approve_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class ConductData(models.Model):
    name = models.CharField(max_length = 150)
    email = models.EmailField()
    phone = models.IntegerField()
    subject  = models.CharField(max_length = 150)
    message  = models.TextField()
    view_status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name + ' /' + self.email

    class Meta:
        verbose_name = 'ConductData'
        verbose_name_plural = 'ConductData'
        ordering = ['-id']


# Privacy Policy
# Terms and conditions
# Our Mission & Vision
# Returns Policy
# Shipping and Delivery

class PrivacyPolicy(models.Model):
    all_information = RichTextField()

    def __str__(self):
        return 'Privacy Policy'


class TermsAndConditions(models.Model):
    all_information = RichTextField()

    def __str__(self):
        return 'Terms And Conditions'

class Mission(models.Model):
    all_information = RichTextField()

    def __str__(self):
        return 'Mission'

class Vision(models.Model):
    all_information = RichTextField()

    def __str__(self):
        return 'Vision'

class Returns_Policy(models.Model):
    all_information = RichTextField()

    def __str__(self):
        return 'Returns Policy'

class ShippingAndDelivery(models.Model):
    all_information = RichTextField()

    def __str__(self):
        return 'Shipping And Delivery'

class AboutUs(models.Model):
    all_information = RichTextField()

    def __str__(self):
        return 'About-us'



class ImageGallery(models.Model):
    title = models.CharField(max_length = 150)
    image = models.FileField(upload_to='gallery')

    def __str__(self):
        return self.title


class VideoGallery(models.Model):
    title = models.CharField(max_length = 150)
    video_embed_link = models.URLField(max_length = 500)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


class ProductPercel(models.Model):
    order  = models.ForeignKey(Order, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length = 150, blank=True, null=True)
    customer_phone = models.CharField(max_length = 150,blank=True, null=True)
    customer_address = models.CharField(max_length = 150,blank=True, null=True)
    merchant_invoice_id = models.CharField(max_length = 150,blank=True, null=True)
    cash_collection_amount = models.CharField(max_length = 150)
    delivery_area  = models.CharField(max_length = 150)
    delivery_area_id  = models.CharField(max_length = 150)
    parcel_weight = models.CharField(max_length = 150)
    tracking_id = models.CharField(max_length = 150)