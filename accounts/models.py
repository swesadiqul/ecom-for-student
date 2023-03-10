from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField



#create model
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    last_login = models.DateTimeField(auto_now=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    sign_up_for_newsletter = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    receive_offer_from_our_partner = models.BooleanField(default=False)
    title = models.CharField(max_length=10, choices=[('Mr', 'Mr'), ('Ms', 'Ms')], blank=True)

    def __str__(self):
        return self.user.email
    
#today
class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = RichTextField()

    def __str__(self):
        return self.question


class Media(models.Model):
    name = models.CharField(max_length=120, verbose_name='Media name')

    class Meta:
        verbose_name_plural = "Media Type"

    def __str__(self):
        return self.name


class SocialAccount(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='social_media')
    link = models.URLField()

    class Meta:
        verbose_name_plural = "Social Account"
    
    def __str__(self):
        return self.media.name


class ContactInformation(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=16)
    location = models.CharField(max_length=255)


    class Meta:
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return self.email
    


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('audio', 'Audio'),
    ]
    title = models.CharField(max_length=255)
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default='article')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = RichTextUploadingField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail = models.FileField(upload_to='thumbnails/', null=True, blank=True)


    def __str__(self):
        return self.title