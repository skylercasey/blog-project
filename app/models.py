from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from datetime import datetime,date
from ckeditor.fields import RichTextField

class MyUserManager(BaseUserManager):
	def create_user(self,email,password=None):
		if not email:
			raise ValueError('user must have an email addres')
		user=self.model(
		email=self.normalize_email(email),)
		user.set_password(password)
		user.save(using=self.db)
		return user
	def create_superuser(self,email,password=None):
		user=self.create_user(
			email,
			password=password,)
		user.is_admin=True
		user.save(using=self.db)
		return user

class MyUser(AbstractBaseUser):
	email=models.EmailField(verbose_name='email_address',max_length=255,unique=True)
	first_name=models.CharField(max_length=100,default="none")
	last_name=models.CharField(max_length=100,default="none")
	is_active=models.BooleanField(default=True)
	is_admin=models.BooleanField(default=False)
	objects=MyUserManager()
	USERNAME_FIELD='email'
	# REQUIRED_FIELD=['password']
	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return True
	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		return self.is_admin

class UserProfile(models.Model):
	user=models.OneToOneField(MyUser,on_delete=models.CASCADE,null=True,blank=True)
	bio=models.TextField(null=True,blank=True)
	profile_image=models.ImageField(null=True, blank=True, upload_to="images/")
	def __str__(self):
		return str(self.user)


# User=get_user_model()


@receiver(post_save,sender=MyUser)
def create_profile(sender,instance,created,**kwargs):
	if created:
		obj=UserProfile.objects.create(user=instance)
	
class Category(models.Model):
	name=models.CharField(max_length=255)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		# return reverse('ac',args=(str(self.id)))
		return reverse('home')



class Post(models.Model):
	title=models.CharField(max_length=255,null=True,blank=True)
	title_tag=models.CharField(max_length=255,default="")
	author=models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
	body=RichTextField(blank=True,null=True)
	post_date=models.DateField(auto_now_add=True)
	category=models.CharField(max_length=255,default='uncategorized')
	likes=models.ManyToManyField(MyUser,related_name='blog_post')
	header_image=models.ImageField(null=True, blank=True, upload_to="images/")

	def __str__(self):
		return self.title + '|' + str(self.author)

	def get_absolute_url(self):
		# return reverse('ac',args=(str(self.id)))
		return reverse('home')

	def total_likes(self):
		return self.likes.count()

