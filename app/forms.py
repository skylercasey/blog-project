from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import MyUser,Post,UserProfile,Category
from django.contrib.auth import authenticate 


#choices=[('coding','coding'),('sport','sport'),('entertainment','entertainment')]
choices=Category.objects.all().values_list('name','name')
choice_list=[]
for item in choices:
	choice_list.append(item)

class PostForm(forms.ModelForm):
	class Meta:
		model=Post
		fields=('title','title_tag','category','author','body','header_image')
		widgets={
			"title": forms.TextInput(attrs={'class':'form-control','placeholder':'this is the title tag'}),
			"title_tag": forms.TextInput(attrs={'class':'form-control'}),
			"author": forms.Select(attrs={'class':'form-control'}),
			"body": forms.Textarea(attrs={'class':'form-control'}),
			"category": forms.Select(choices=choice_list,attrs={'class':'form-control'}),
			}
class Profile(forms.ModelForm):
	class Meta:
		model=UserProfile
		fields=('bio','profile_image')
		widgets={
		"bio":forms.Textarea(attrs={'class':'form-control'}),
		}

class UserEditForm(forms.ModelForm):
	class Meta:
		model=MyUser
		fields=('first_name',)
	def __init__(self,*args,**kwargs):
			super(AccountAuthenticationForm,self).__init__(*args,**kwargs)
			for field in (self.fields['email'],self.fields['password']):
				field.widget.attrs.update({'class':'form-control'})



		# widgets={
		# 	"email": forms.TextInput(attrs={'class':'form-control','placeholder':'this is the title tag'}),
		# 	"title_tag": forms.TextInput(attrs={'class':'form-control'}),
		# 	# "author": forms.Select(attrs={'class':'form-control'}),
		# 	"body": forms.Textarea(attrs={'class':'form-control'}),
			
		# 	}




class EditForm(forms.ModelForm):
	class Meta:
		model=Post
		fields=('title','title_tag','body')
		widgets={
			"title": forms.TextInput(attrs={'class':'form-control','placeholder':'this is the title tag'}),
			"title_tag": forms.TextInput(attrs={'class':'form-control'}),
			# "author": forms.Select(attrs={'class':'form-control'}),
			"body": forms.Textarea(attrs={'class':'form-control'}),
			}

class UserCreateForm(UserCreationForm):
	first_name=forms.CharField(max_length=100,widget= forms.TextInput(attrs={'class':'form-control','placeholder':'first name'}))
	last_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'last name'}))
	class Meta:
		model=MyUser 
		fields=('email','first_name','last_name','password1','password2',)
		# widgets={
		# 	"email": forms.TextInput(attrs={'class':'form-control','placeholder':'enter your email id'}),
		# 	}

	def __init__(self,*args,**kwargs):
		super(UserCreateForm, self).__init__(*args,**kwargs)
		self.fields['password1'].widget.attrs['class']='form-control'
		self.fields['password2'].widget.attrs['class']='form-control'
		self.fields['email'].widget.attrs['class']='form-control'

class AccountAuthenticationForm(forms.ModelForm):
	email=forms.EmailField(label='Enter Email')
	password=forms.CharField(label='PASSWORD',widget=forms.PasswordInput)
	class Meta:
		model=MyUser 
		fields=('email','password',)
		widget={
		'email':forms.TextInput(attrs={'class':'form-control'}),
		'password':forms.TextInput(attrs={'class':'form-control'})
		}
		def __init__(self,*args,**kwargs):
			super(AccountAuthenticationForm,self).__init__(*args,**kwargs)
			for field in (self.fields['email'],self.fields['password']):
				field.widget.attrs.update({'class':'form-control'})

		def clean(self):
			if self.is_valid():
				email=self.cleaned_data.get('email')
				password=self.cleaned_data.get('password')
				if not authenticate(email=email,password=password):
					raise forms.ValidationErrors('invalid login')

