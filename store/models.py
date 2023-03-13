from django.db import models
from django.shortcuts import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
import string, random
from django.db import IntegrityError
from ckeditor.fields import RichTextField
from django.utils import timezone

# Create your models here.
class SiteLogo(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='siteLogo',)

    def __str__(self):
        return self.name
    

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
    product_name = models.CharField(max_length=100)
    product_code = models.CharField(max_length = 150)
    slug = models.SlugField(max_length=100, blank=True, null=True, unique=True)  
    categoris = models.ForeignKey(ProductCategory, verbose_name='Product Category', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='productImg', default='ProductImg/noimg.jpg')
    hover_image = models.ImageField(upload_to='ProductImg', default='noimg.jpg', blank=True, null=True)
    regular_price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    product_purchase_price = models.IntegerField()
    sort_discription = RichTextField(blank=True, null=True)
    details = RichTextUploadingField()
    shipping_and_return = RichTextUploadingField()
    size_chart = RichTextField(blank=True, null=True)
    stock_quantity = models.PositiveIntegerField()
    show_status  = models.BooleanField(default=False)
    product_label = models.CharField(max_length=255, )
    flash_sale_add_and_expire_date = models.DateTimeField(blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    price_range =models.ForeignKey(PriceRange, on_delete=models.CASCADE, blank=True, null=True)
    meta_title = models.CharField(blank=True, null=True, max_length=100)
    availability = models.CharField(blank=True, null=True, max_length=120)
    rating = models.CharField(blank=True, null=True, max_length=120)
    tax = models.CharField(blank=True, null=True, max_length=120)
    
    def saving_price(self):
        return self.price  - self.discount_price

    def saving_percent(self):
        return self.saving_price() / self.price  * 100
        
    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['-id']
    
    def save(self, *args, **kwargs):
        try:
            self.slug =''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(49))
            
            super().save(*args, **kwargs)
            # super().save()  # saving image first

            img = Image.open(self.image.path) # Open image using self
            
            if img.height > 630 or img.width > 1200:
                new_img = (700, 700)
                img.thumbnail(new_img)
                img.save(self.image.path)  # saving image at the same path
        except IntegrityError:
            self.save(*args, **kwargs)
            
      

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

    def get_product_update_url(self):
        return reverse('product-update', kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse('remove-form-cart', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={'slug': self.slug})

    def get_buy_now_url(self):
        return reverse('buy-now', kwargs={'slug': self.slug})


    def get_review_list(self):
        reviews = ProductReview.objects.filter(product=self,approve_status=True)
        return reviews

    def get_avg_rating(self):
        reviews = ProductReview.objects.filter(product=self,approve_status=True)
        count = len(reviews)
        sum = 0
        for rvw in reviews:
            sum += rvw.rating
        if count != 0:
            return (sum*20/count)

    def get_rating_count(self):
        reviews = ProductReview.objects.filter(product=self,approve_status=True)
        count = len(reviews)
        return count

class ProductImgGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.FileField(upload_to='ProductImgGallery')

    def __str__(self):
        return self.product.slug

class VariationManager(models.Manager): 
    def all(self):
        return super(VariationManager, self).filter(active=True)

    def sizes(self):
        return self.all().filter(category='size')

    def colors(self):
        return self.all().filter(category='color')

VAR_CATEGORIES = ( 
    ('size', 'size'), 
    ('color', 'color'), 
    )

class Variation(models.Model): 
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES) 
    title = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    objects = VariationManager()

    def __str__(self):
        return self.title

class OrderItem(models.Model): 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    ordered = models.BooleanField(default=False) 
    item = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.IntegerField(default=1) 
    variation = models.ManyToManyField(Variation)
  
    def saving_price(self):
        return (self.item.price * self.quantity) - (self.item.discount_price * self.quantity)

    def saving_percent(self):

        return (self.saving_price()) / (self.item.price * self.quantity) * 100

    def get_subtotal(self):
        if self.item.discount_price:
            return self.item.discount_price * self.quantity
        else:
            return self.item.price * self.quantity

    def get_purchase_price_subtotal(self):
        return self.item.product_purchase_price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.item.product_name}"

    class Meta:
        ordering = ['-id']


Order_Status = (
    ('pending','pending'),
    ('processing','processing'),
    ('on the way','on the way'),
    ('complete','complete'),
    ('cancel','cancel')
)

class Order(models.Model): 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField()
    order_complate_date = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    order_status = models.CharField(max_length = 150, choices=Order_Status , default='pending')
    total_order_amount = models.CharField(max_length = 150, blank=True, null=True)
    paid_amount = models.CharField(max_length = 150, default=0)
    due_amount = models.CharField(max_length = 150,default=0)
    ordered = models.BooleanField(default=False)
    orderId = models.CharField(max_length = 150, blank=True, null=True)
    paymentId = models.CharField(max_length = 150, blank=True, null=True) 
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    # shipping_address = models.ForeignKey(ShipingAddress, on_delete=models.CASCADE, blank=True, null=True)
    payment_option = models.CharField(max_length = 150)
    order_read_status  = models.BooleanField(default=False)
    redx_percel_traking_number  = models.CharField(max_length = 150, blank=True, null=True)
    others_transport_trakink_url  = models.URLField(max_length = 200,blank=True, null=True)
    
    
    def __str__(self):
        return self.user.username   

    def get_purchase_price_total(self):
        total = 0
        for i in self.items.all():
            total += i.get_purchase_price_subtotal()
        return total

    def get_total(self):
        total = 0
        for i in self.items.all():
            total += i.get_subtotal()
        return total

    def get_total_sale(self):
        total = 0
        for i in self.items.all():
            total += i.get_subtotal()
        return total

    def get_total_with_shiping_charge(self):
        total = 0
        for i in self.items.all():
            total += i.get_subtotal()
        if self.shipping_address.shiping_area == 'Only Chittagong District':
            total += 50
        elif self.shipping_address.shiping_area == 'Inside Dhaka':
            total += 80
        elif self.shipping_address.shiping_area == 'Outside Dhaka':
            total += 95
        return total

    def only_shiping_charge_payment(self):
        if self.shipping_address.shiping_area == 'Only Chittagong District':
            total = 50
        elif self.shipping_address.shiping_area == 'Inside Dhaka':
            total = 80
        elif self.shipping_address.shiping_area == 'Outside Dhaka':
            total = 95
        return total

    def get_total_with_coupon(self):
        total = 0
        for i in self.items.all():
            total += i.get_subtotal()
        total += self.only_shiping_charge_payment()
        total -= self.coupon.amount
        return total

    def total(self):
        if self.coupon:
            return self.get_total_with_coupon()
        else:
            return self.get_total_with_shiping_charge()
    
    def total_paid_amount(self):
        return self.total() - int(self.paid_amount)



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

class  Mission(models.Model):
    all_information = RichTextField()

    def __str__(self):
        return 'Mission'

class  Vision(models.Model):
    all_information = RichTextField()

    def __str__(self):
        return 'Vision'

class  Returns_Policy(models.Model):
    all_information = RichTextField()

    def __str__(self):
        return 'Returns Policy'

class  ShippingAndDelivery(models.Model):
    all_information = RichTextField()

    def __str__(self):
        return 'Shipping And Delivery'

class  AboutUs(models.Model):
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