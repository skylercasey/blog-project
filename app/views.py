from django.shortcuts import render,redirect,get_object_or_404
from .models import MyUser,Post,UserProfile,Category
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from .forms import UserCreateForm,AccountAuthenticationForm
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django import forms
from .forms import PostForm,EditForm,Profile,UserEditForm
from django.urls import reverse_lazy,reverse
from django.contrib.auth.forms import UserChangeForm

# def none(request):
# 	return HttpResponse("<h1>we will work later on this</h1>")
# class UserEditView(UpdateView):
# 	model=UserProfile
# 	form_class=Profile
# 	template_name='app/edit_profile.html'
# 	success_url=reverse_lazy('home')
# class UpdatePostView(UpdateView):
# 	model=Post
# 	form_class=EditForm
# 	template_name='app/update_post.html'

def UserEditView(request,pk):
	form=Profile()

	objects1=UserProfile.objects.get(user=pk)
	
	context = {}
	if request.method=="POST":
		form=Profile(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
	else:
		form=Profile(
			initial={
			"bio":objects1.bio
			})

	
	context["form"]=form
	return render(request,"app/edit_profile.html",context)	

def ProfileView(request,pk):
	objects=UserProfile.objects.all()
	context={"obj":objects}
	return render(request,"app/profile.html",context)


def UserProfileView(request):
	return render(request,"app/profile.html")

class AddPostView(CreateView ):
	model=Post
	form_class=PostForm
	template_name='app/add_post.html'
	# fields='__all__'
	# fields=('title','body')

class UpdatePostView(UpdateView):
	model=Post
	form_class=EditForm
	template_name='app/update_post.html'
	# fields=['title','title_tag','body']
class DeletePostView(DeleteView):
	model=Post
	template_name='app/delete_post.html'
	success_url=reverse_lazy('home')

class HomeView(ListView):
	model=Post
	template_name='app/home.html'  
	ordering=['-post_date']

	def get_context_data(self,*args,**kwargs):
		cat_menu=Category.objects.all()
		context=super(HomeView,self).get_context_data(*args,**kwargs)
		context["cat_menu"]=cat_menu
		return context

def ArticleDetailView(request,pk):
	object=Post.objects.get(id=pk)
	liked=False
	context={}
	context['post']=object
	total_likes=len(object.likes.all())
	cat_menu=Category.objects.all()
	context["cat_menu"]=cat_menu
	context["total_likes"]=total_likes
	return render(request,'app/article_details.html',context)

	# def get_context_data(self,*args,**kwargs):
	# 	cat_menu=Category.objects.all()
	# 	context=super(ArticleDetailView,self).get_context_data(*args,**kwargs)
	# 	stuff=get_object_or_404(Post,id=self.kwargs['pk'])
	# 	total_likes=stuff.total_likes()
	# 	context["cat_menu"]=cat_menu
	# 	context["total_likes"]=total_likes
	# 	context["liked"]=liked
	# 	liked=False
	# 	if stuff.likes.filter(id=self.request.user.id).exist():
	# # 		liked=True
		
	# 	return context

def signup_view(request):
	if request.method=='POST':
		form=UserCreateForm(request.POST)
		if form .is_valid():
			new_user=form.save()
			new_user=authenticate(email=form.cleaned_data['email'],password=form.cleaned_data['password1'])
			login(request,new_user)
			return redirect('home')
		else:
			print(request.GET,form.errors)
			return render(request,'app/signup.html',{'form':form})

	else:
		form=UserCreateForm()
		return render(request,'app/signup.html', {'form':form})

def logout_view(request):
	logout(request)
	return redirect('home')

def login_view(request):
	context={}
	user=request.user
	if user.is_authenticated:
		return redirect('home')
	if request.POST:
		form=AccountAuthenticationForm(request.POST)
		email=request.POST.get('email')
		password=request.POST.get('password')
		user=authenticate(email=email,password=password)
		if user:
			login(request,user)
			return redirect('home')
		else:
			context['login_form']=form
			return render(request,'app/login.html',context)
	else:
		form=AccountAuthenticationForm()
		context['login_form']=form
		return render(request,'app/login.html',context)

class AddCategoryView(CreateView ):
	model=Category
	template_name='app/add_category.html'
	fields='__all__'

def CategoryView(request,cats):
	category_posts=Post.objects.filter(category=cats.replace('-',' '))
	return render(request,'app/categories.html',{'cats':cats.title().replace('-',' '),'category_posts':category_posts})

def LikeView(request,pk):
	post=get_object_or_404(Post,id=request.POST.get('post_id'))
	liked=False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		liked=False
	else:
		post.likes.add(request.user)
		liked=True
	post.likes.add(request.user)
	post.save()
	return HttpResponseRedirect(reverse('ac',args=[str(pk)]))