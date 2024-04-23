from django.shortcuts import render, reverse, HttpResponseRedirect, redirect, get_object_or_404, HttpResponse, redirect
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView,  UpdateView, DeleteView, View, TemplateView
from .models import Post, Category, Profile, NewsletterSubscription
from django.urls import reverse_lazy
from .forms import PostForm, NewPostForm, CategoryForm, PrimeUserForm, NewsletterSubscriptionForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from .decorators import staff_or_superuser_required
from .decorators import superuser_required, staff_required
from django.core.mail import EmailMessage
from .models import ContactEntry
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Notification
from django.contrib.sessions.models import Session




def logout_views(request):
    logout(request)
    # Redirect to a success page or any other page after logout
    return render(request, "logout_views.html")

# @method_decorator(staff_required, name='dispatch') [we use this for class base views]   
# @method_decorator(login_required, name='dispatch')
# @method_decorator(superuser_required, name='dispatch')
# @login_required
# @superuser_required [we use this for def means for functions]
# @staff_required





# class home(ListView):
#     model = Post
#     template_name = name='home.html'
#     # ordering = ['-id']
#     ordering = ['-post_date']
# @staff_or_superuser_required
# @login_required
# @superuser_required
def home(request):
    categories = Category.objects.all()
    category_posts = {}
    
    
    for category in categories:
        # Fetch the four latest posts for each category
        posts = Post.objects.filter(category=category).order_by('-post_date')[:4]
        category_posts[category] = posts
        
    cricket_category = Category.objects.get(name="Cricket")
    
    # Fetch the four latest posts from the Cricket category
    cricket_posts = Post.objects.filter(category=cricket_category).order_by('-post_date')
    
    football_category = Category.objects.get(name="Football")
    football_posts = Post.objects.filter(category=football_category).order_by('-post_date')
    basketball_category = Category.objects.get(name="Basketball")
    basketball_posts = Post.objects.filter(category=basketball_category).order_by('-post_date')
    athelatics_category = Category.objects.get(name="Athelatics")
    athelatics_posts = Post.objects.filter(category=athelatics_category).order_by('-post_date')
    prime_category = Category.objects.get(name="Prime")
    prime_posts = Post.objects.filter(category=prime_category).order_by('-post_date')
    return render(request, 'home.html', {'category_posts': category_posts, 'cricket_posts': cricket_posts, 'football_posts': football_posts, 'basketball_posts': basketball_posts, 'athelatics_posts': athelatics_posts, 'prime_posts': prime_posts})
    
    
def landingpage(request):
    categories = Category.objects.all()
    category_posts = {}
    
    
    for category in categories:
        # Fetch the four latest posts for each category
        posts = Post.objects.filter(category=category).order_by('-post_date')[:4]
        category_posts[category] = posts
        
    cricket_category = Category.objects.get(name="Cricket")
    
    # Fetch the four latest posts from the Cricket category
    cricket_posts = Post.objects.filter(category=cricket_category).order_by('-post_date')
    
    football_category = Category.objects.get(name="Football")
    football_posts = Post.objects.filter(category=football_category).order_by('-post_date')
    basketball_category = Category.objects.get(name="Basketball")
    basketball_posts = Post.objects.filter(category=basketball_category).order_by('-post_date')
    athelatics_category = Category.objects.get(name="Athelatics")
    athelatics_posts = Post.objects.filter(category=athelatics_category).order_by('-post_date')
    prime_category = Category.objects.get(name="Prime")
    prime_posts = Post.objects.filter(category=prime_category).order_by('-post_date')
    return render(request, 'landingpage.html', {'category_posts': category_posts, 'cricket_posts': cricket_posts, 'football_posts': football_posts, 'basketball_posts': basketball_posts, 'athelatics_posts': athelatics_posts, 'prime_posts': prime_posts})
   
# class landingpage(ListView):
#     model = Post
#     template_name = name='landingpage.html'
#     # ordering = ['-id']
#     ordering = ['-post_date']

def categorypage(request, cat):
    category = get_object_or_404(Category, name__iexact=cat)
    category_posts = Post.objects.filter(category=category)
    ordering = '-post_date'  # Define the ordering separately
    category_posts = category_posts.order_by(ordering)  # Apply the ordering to the queryset
    return render(request, 'categories.html', {'cat': category, 'category_posts': category_posts})
 

    
# class DetailArticle(DetailView):
#     model = Post
#     template_name = 'detail-article.html'
#     slug_url_kwarg = 'slug'

    
#     def get_absolute_url(self):
#         return reverse("detail-article", kwargs={"slug": self.slug})

# class DetailArticle(DetailView):
#     model = Post
#     template_name = 'detail-article.html'
#     slug_url_kwarg = 'slug'
#     context_object_name = 'post'

#     def get_object(self, queryset=None):
#         obj = super().get_object(queryset)
#         return obj

#     def dispatch(self, request, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return HttpResponseForbidden("You must be logged in to view this page.")
        
#         # Get the post object
#         self.object = self.get_object()
        
#         # Check if the post belongs to the prime category
#         if self.object.category.name == 'Prime':
#             # Check if the user is a prime user
#             if not self.request.user.profile.is_prime_user:
#                 return HttpResponseForbidden("You are not authorized to view this post.")
        
#         return super().dispatch(request, *args, **kwargs)

# class DetailArticle(DetailView):
#     model = Post
#     template_name = 'detail-article.html'
#     slug_url_kwarg = 'slug'

#     def dispatch(self, request, *args, **kwargs):
#         post = self.get_object()
#         if post.category.name == 'Prime':
#             if request.user.is_authenticated:
#                 # Check if the user is a prime member
#                 if not request.user.profile.is_prime_user:
#                     return redirect('half-detail')
#                     # return HttpResponseForbidden("You are not authorized to view this post.")
#             else:
#                 return HttpResponseForbidden("You are not authorized to view this post.")
#         return super().dispatch(request, *args, **kwargs)
    
# class DetailArticle(DetailView):
#     model = Post
#     template_name = 'detail-article.html'
#     slug_url_kwarg = 'slug'

#     def dispatch(self, request, *args, **kwargs):
#         post = self.get_object()
#         if post.category.name == 'Prime':
#             if request.user.is_authenticated:
#                 # Check if the user is a prime member
#                 if not request.user.profile.is_prime_user:
#                     # Redirect non-prime users to half-detail.html
#                     return redirect('half_detail')
#             else:
#                 # Redirect unauthenticated users to a login page or display a message
#                 return HttpResponseForbidden("You are not authorized to view this post.")
#         return super().dispatch(request, *args, **kwargs)

class DetailArticle(DetailView):
    model = Post
    template_name = 'detail-article.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['is_prime_user'] = self.request.user.is_authenticated and self.request.user.profile.is_prime_user if hasattr(self.request.user, 'profile') else False
        return context
    

class HalfDetailPageView(LoginRequiredMixin, TemplateView):
    template_name = 'half-detail.html'
    login_url = '/login/'  # Adjust the login URL as per your project

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            # Allow staff members to access the view
            return super().dispatch(request, *args, **kwargs)
        else:
            # Deny access to non-staff users
            return HttpResponseForbidden("Access Denied. Only staff members are allowed to view this page.")


# def become_prime_user(request):
#     if request.method == 'POST':
#         form = PrimeUserForm(request.POST)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.user = request.user
#             profile.is_prime_user = True
#             profile.save()
#             return redirect('/')
#     else:
#         form = PrimeUserForm()
#     return render(request, 'become_prime_user.html', {'form': form})

# @login_required
# def become_prime_user(request):
#     # Check if the user already has a profile
#     existing_profile = Profile.objects.filter(user=request.user).exists()
#     if existing_profile:
#         # If a profile already exists, redirect or display an error message
#         # Redirecting to some other page for demonstration
#         return redirect('home')  # Replace 'home' with the desired URL name
#     else:
#         # If no profile exists, create a new one
#         profile = Profile.objects.create(user=request.user, is_prime_user=True)
#         profile.save()
#         # Perform any additional actions or redirect as needed
#         return redirect('home')  # Replace 'home' with the desired URL name
# def EditPrimeRole(request):
#     return render(request, 'become_prime_user.html')

# def EditPrimeRole(request):
#     # Fetch all profiles from the Profile model
#     profiles = Profile.objects.all()

#     # Pass the fetched profiles to the template
#     return render(request, 'become_prime_user.html', {'profiles': profiles})
# def EditPrimeRole(request):
#     profiles = Profile.objects.all()
#     if request.method == 'POST':
#         user_id = request.POST.get('user_id')
#         user = get_object_or_404(User, pk=user_id)
#         profile = user.profile
#         profile.is_prime_user = not profile.is_prime_user
#         profile.save()
#         return redirect('')  # Redirect back to the page with updated data
#     else:
#         form = PrimeUserForm()
#     return render(request, 'become_prime_user.html', {'profiles': profiles, 'form': form})
#---------------------------------------
#working
# @superuser_required
# def EditPrimeRole(request):
#     profiles = Profile.objects.all()
#     if request.method == 'POST':
#         user_id = request.POST.get('user_id')
#         user = User.objects.get(id=user_id)
#         profile = user.profile
#         profile.is_prime_user = not profile.is_prime_user
#         profile.save()
#         # Redirect back to the same page
#         return redirect(request.path)
#     else:
#         form = PrimeUserForm()
#     return render(request, 'become_prime_user.html', {'profiles': profiles, 'form': form})
#-------------------------------------------------------
# @superuser_required
# def EditPrimeRole(request):
#     profiles = Profile.objects.all()
#     if request.method == 'POST':
#         user_id = request.POST.get('user_id')
#         subscription_start_date = request.POST.get('subscription_start_date')
#         subscription_expiry_date = request.POST.get('subscription_expiry_date')
        
#         if not user_id:
#             error_message = "User ID is empty."
#             print("Error:", error_message)  
#             return render(request, 'error_page.html', {'error_message': error_message})
        
#         try:
#             user = User.objects.get(id=user_id)
#             profile = user.profile
#             profile.is_prime_user = not profile.is_prime_user
            
#             # Update subscription dates
#             if subscription_start_date:
#                 profile.subscription_start_date = subscription_start_date
#             if subscription_expiry_date:
#                 profile.subscription_expiry_date = subscription_expiry_date
            
#             profile.save()
            
#             # Redirect back to the same page
#             return redirect(request.path)
        
#         except User.DoesNotExist:
#             error_message = "User with the specified ID does not exist."
#             print("Error:", error_message)
#             return render(request, 'error_page.html', {'error_message': error_message})
    
#     else:
#         form = PrimeUserForm()
    
#     return render(request, 'become_prime_user.html', {'profiles': profiles, 'form': form})
#------------------------------------
# @superuser_required
# def EditPrimeRole(request):
#     if request.method == 'POST':
#         user_id = request.POST.get('user_id')
#         if not user_id:
#             error_message = "User ID is empty."
#             return render(request, 'error_page.html', {'error_message': error_message})
        
#         try:
#             user = User.objects.get(id=user_id)
#             profile = user.profile
#             profile.is_prime_user = not profile.is_prime_user
            
#             # Convert date strings to datetime objects
#             subscription_start_date = request.POST.get('subscription_start_date')
#             subscription_expiry_date = request.POST.get('subscription_expiry_date')
#             if subscription_start_date:
#                 profile.subscription_start_date = subscription_start_date
#             if subscription_expiry_date:
#                 profile.subscription_expiry_date = subscription_expiry_date
            
#             profile.save()
#             return redirect(request.path)
#         except User.DoesNotExist:
#             error_message = "User with the specified ID does not exist."
#             return render(request, 'error_page.html', {'error_message': error_message})
    
#     else:
#         # Fetch the current profile data
#         profiles = Profile.objects.all()
#         for profile in profiles:
#             profile.subscription_start_date = profile.subscription_start_date.strftime('%Y-%m-%d') if profile.subscription_start_date else ''
#             profile.subscription_expiry_date = profile.subscription_expiry_date.strftime('%Y-%m-%d') if profile.subscription_expiry_date else ''
        
#         form = PrimeUserForm()
#         return render(request, 'become_prime_user.html', {'profiles': profiles, 'form': form})
#--------------------------------------------------------------------------
# @superuser_required
# def EditPrimeRole(request):
#     if request.method == 'POST':
#         user_id = request.POST.get('user_id')
#         if not user_id:
#             error_message = "User ID is empty."
#             return render(request, 'error_page.html', {'error_message': error_message})
        
#         try:
#             user = User.objects.get(id=user_id)
#             profile = user.profile
#             profile.is_prime_user = not profile.is_prime_user
            
#             # Convert date strings to datetime objects
#             subscription_start_date = request.POST.get('subscription_start_date')
#             subscription_expiry_date = request.POST.get('subscription_expiry_date')
            
#             # Check if dates are provided and convert to datetime objects
#             if subscription_start_date:
#                 profile.subscription_start_date = subscription_start_date
#             else:
#                 profile.subscription_start_date = None  # Set to null if date is cleared
                
#             if subscription_expiry_date:
#                 profile.subscription_expiry_date = subscription_expiry_date
#             else:
#                 profile.subscription_expiry_date = None  # Set to null if date is cleared
            
#             profile.save()
#             return redirect(request.path)
#         except User.DoesNotExist:
#             error_message = "User with the specified ID does not exist."
#             return render(request, 'error_page.html', {'error_message': error_message})
    
#     else:
#         profiles = Profile.objects.all()
#         for profile in profiles:
#             profile.subscription_start_date = profile.subscription_start_date.strftime('%Y-%m-%d') if profile.subscription_start_date else ''
#             profile.subscription_expiry_date = profile.subscription_expiry_date.strftime('%Y-%m-%d') if profile.subscription_expiry_date else ''
        
#         form = PrimeUserForm()
#         return render(request, 'become_prime_user.html', {'profiles': profiles, 'form': form})
#--------------------------------------

# @superuser_required
# def EditPrimeRole(request):
#     profiles = Profile.objects.all()
    
#     if request.method == 'POST':
#         user_id = request.POST.get('user_id')
        
#         if not user_id:
#             error_message = "User ID is empty."
#             return render(request, 'error_page.html', {'error_message': error_message})
        
#         try:
#             user = User.objects.get(id=user_id)
#             profile = user.profile
#             profile.is_prime_user = not profile.is_prime_user
            
#             if profile.is_prime_user:
#                 # Set subscription start date to current date
#                 profile.subscription_start_date = timezone.now().date()
#                 # Calculate subscription expiry date as 30 days from start date
#                 profile.subscription_expiry_date = profile.subscription_start_date + timedelta(days=30)
#             else:
#                 # Reset subscription dates if user is not a prime user
#                 profile.subscription_start_date = None
#                 profile.subscription_expiry_date = None
            
#             profile.save()
#             return redirect(request.path)
#         except User.DoesNotExist:
#             error_message = "User with the specified ID does not exist."
#             return render(request, 'error_page.html', {'error_message': error_message})
    
#     else:
#         profiles = Profile.objects.all()
#         for profile in profiles:
#             profile.subscription_start_date = profile.subscription_start_date.strftime('%Y-%m-%d') if profile.subscription_start_date else ''
#             profile.subscription_expiry_date = profile.subscription_expiry_date.strftime('%Y-%m-%d') if profile.subscription_expiry_date else ''
        
#         form = PrimeUserForm()
#         return render(request, 'become_prime_user.html', {'profiles': profiles, 'form': form})
#-----------------------------------------------
# prime feature without 30 days
from datetime import datetime, timedelta

@superuser_required
def EditPrimeRole(request):
    profiles = Profile.objects.all()
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        
        if not user_id:
            error_message = "User ID is empty."
            return render(request, 'error_page.html', {'error_message': error_message})
        
        try:
            user = User.objects.get(id=user_id)
            profile = user.profile
            profile.is_prime_user = not profile.is_prime_user
            
            if profile.is_prime_user:
                # Set subscription start date to current date if not set
                if not profile.subscription_start_date:
                    profile.subscription_start_date = timezone.now().date()
                
                # Get user-inputted expiry date from the form
                expiry_date_str = request.POST.get('subscription_expiry_date')
                
                # Parse user-inputted expiry date and update profile
                if expiry_date_str:
                    new_expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
                    # Only update expiry date if it's in the future
                    if new_expiry_date >= timezone.now().date():
                        profile.subscription_expiry_date = new_expiry_date
                else:
                    # If no expiry date provided, default to 30 days from start date
                    profile.subscription_expiry_date = profile.subscription_start_date + timedelta(days=30)
            else:
                # Reset subscription dates if user is not a prime user
                profile.subscription_start_date = None
                profile.subscription_expiry_date = None
            
            profile.save()
            return redirect(request.path)
        except User.DoesNotExist:
            error_message = "User with the specified ID does not exist."
            return render(request, 'error_page.html', {'error_message': error_message})
    
    else:
        profiles = Profile.objects.all()
        for profile in profiles:
            profile.subscription_start_date = profile.subscription_start_date.strftime('%Y-%m-%d') if profile.subscription_start_date else ''
            profile.subscription_expiry_date = profile.subscription_expiry_date.strftime('%Y-%m-%d') if profile.subscription_expiry_date else ''
        
        form = PrimeUserForm()
        return render(request, 'become_prime_user.html', {'profiles': profiles, 'form': form})

# ---------------------------------------
#prime feature with 30 days 
from datetime import datetime, timedelta

@superuser_required
def EditPrimeRole(request):
    profiles = Profile.objects.all()
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        
        if not user_id:
            error_message = "User ID is empty."
            return render(request, 'error_page.html', {'error_message': error_message})
        
        try:
            user = User.objects.get(id=user_id)
            profile = user.profile
            profile.is_prime_user = not profile.is_prime_user
            
            if profile.is_prime_user:
                # Set subscription start date to current date if not set
                if not profile.subscription_start_date:
                    profile.subscription_start_date = timezone.now().date()
                
                # Get user-inputted expiry date from the form
                expiry_date_str = request.POST.get('subscription_expiry_date')
                
                # Parse user-inputted expiry date and update profile
                if expiry_date_str:
                    new_expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
                    # Only update expiry date if it's in the future
                    if new_expiry_date >= timezone.now().date():
                        profile.subscription_expiry_date = new_expiry_date
                else:
                    # If no expiry date provided, default to 30 days from start date
                    profile.subscription_expiry_date = profile.subscription_start_date + timedelta(days=30)
            else:
                # Reset subscription dates if user is not a prime user
                profile.subscription_start_date = None
                profile.subscription_expiry_date = None
            
            profile.save()
            return redirect(request.path)
        except User.DoesNotExist:
            error_message = "User with the specified ID does not exist."
            return render(request, 'error_page.html', {'error_message': error_message})
    
    else:
        profiles = Profile.objects.all()
        for profile in profiles:
            profile.subscription_start_date = profile.subscription_start_date.strftime('%Y-%m-%d') if profile.subscription_start_date else ''
            profile.subscription_expiry_date = profile.subscription_expiry_date.strftime('%Y-%m-%d') if profile.subscription_expiry_date else ''
        
        form = PrimeUserForm()
        return render(request, 'become_prime_user.html', {'profiles': profiles, 'form': form})


#----------------------------------------


    # def get(self, request, user_id):
    #     user = get_object_or_404(User, id=user_id)
    #     profile = user.profile
    #     form = UserPrivilegeForm(instance=profile)
    #     return render(request, self.template_name, {'form': form, 'user': user})

    # def post(self, request, user_id):
    #     user = get_object_or_404(User, id=user_id)
    #     profile = user.profile
    #     form = UserPrivilegeForm(request.POST, instance=profile)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('user_list')  # Redirect to a page where all users are listed
    #     return render(request, self.template_name, {'form': form, 'user': user})



    
    
# class newpost(CreateView):
#     model = Post
#     template_name = 'new-post.html'
#     fields = '__all__'

#     def form_valid(self, form):
#         category_slug = self.kwargs.get('category_slug')
#         category = get_object_or_404(Category, slug=category_slug)
#         form.instance.category = category
#         return super().form_valid(form)
    
#     def get_success_url(self):
#         return reverse('home')

# class NewPostView(CreateView):
#     template_name = 'new-post.html'  # Create this template

#     def get(self, request):
#         form = NewPostForm()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request):
#         form = NewPostForm(request.POST)
#         if form.is_valid():
#             new_post = form.save()
#             # Redirect to the newly created post's detail page
#             return redirect(new_post.get_absolute_url())

#         return render(request, self.template_name, {'form': form})
# ------------------------------------------

# 07/04/2024 working


# class NewPostView(CreateView):
#     template_name = 'new-post.html'
#     form_class = NewPostForm

#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         post = form.save(commit=False)
#         # post.author = self.request.user  
#         # Assuming you're using User authentication
#         post.save()
#         return redirect(post.get_absolute_url())

from django.contrib.messages.views import SuccessMessageMixin


class NewPostView(SuccessMessageMixin, CreateView):
    template_name = 'new-post.html'
    form_class = NewPostForm
    success_message = "Your post has been created successfully."

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        
        # Print session status
        print("Session before setting:", self.request.session.get('notification'))

        # Set notification session
        self.request.session['notification'] = True
        self.request.session.modified = True

        # Print session status after setting
        print("Session after setting:", self.request.session.get('notification'))

        return redirect(post.get_absolute_url())
    
class NotificationListView(ListView):
    model = Post
    template_name = name='notifiction.html'
    # ordering = ['-id']
    ordering = ['-post_date']
    paginate_by = 10
    
def notify(request):
    if request.method == "POST":
        if 'notification' in request.session:
            del request.session['notification']

            return redirect('notification')
        else:
            print("'notification' key does not exist in the session")

    
    return render(request, 'home.html') 

# ---------------------------------------

    
class NewCategoryView(CreateView, ListView):
    model = Category
    template_name = 'new-category.html'
    context_object_name = 'object_list'  # Set the context object name to 'object_list'

    fields = '__all__'

    def get_success_url(self):
        # Redirect to the home page after creating a new category
        return reverse('home')

    

 

class updatepost(UpdateView):
    model = Post
    template_name = 'edit-post.html'
    fields = '__all__'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        # Replace 'your_category_attribute' with the actual attribute used for the category in your model
        return reverse('detail-article', kwargs={'cat': self.object.category.slug, 'slug': self.object.slug})


class deletepost(DeleteView):
    model = Post
    template_name = "delete-post.html"
    success_url = reverse_lazy('home')
    


# class NotificationClickView(View):
#     def get(self, request, *args, **kwargs):
#         if 'notification' in request.session:
#             del request.session['notification']
#         return redirect('/')  # Redirect to home or any desired URL



# def NotificationListView(request):
#     return render(request, 'notification.html')

class SearchView(View):
    ordering = ['-post_date']  # Sorting by the latest post date

    def post(self, request):
        search = request.POST.get('search')
        # Using Q objects to perform case-insensitive search
        searched_posts = Post.objects.filter(Q(title__icontains=search) | Q(body__icontains=search)).order_by(*self.ordering)
        return render(request, 'search.html', {'search': search, 'searched_posts': searched_posts})

    def get(self, request):
        return render(request, 'search.html', {})
    
    


def prime_category_posts(request):
    prime_category = Category.objects.get(name='Prime')
    if request.user.is_authenticated:
        try:
            user_profile = Profile.objects.get(user=request.user)
            if user_profile.is_prime_user:
                prime_posts = Post.objects.filter(category=prime_category)
                return render(request, 'prime_category_posts.html', {'prime_posts': prime_posts})
            else:
                return render(request, 'access_denied.html')  # Render access denied page
        except Profile.DoesNotExist:
            return render(request, 'access_denied.html')  # Render access denied page
    else:
        return render(request, 'access_denied.html')  # Render access denied page
    
def Plan(request):
    return render(request, 'plan.html')

@login_required
# @superuser_required
def payment(request):
    return render(request,'payment.html')

# def update_profile(request):
#     if request.method == 'POST':
#         # Assuming the user is logged in
#         user_profile = Profile.objects.get(user=request.user)
#         # Set is_prime_user to True
#         user_profile.is_prime_user = True
#         user_profile.save()
#         return redirect('payment')
# -----------------------------------

#working code 
# def update_profile(request):
#     if request.method == 'POST':
#         # Assuming the user is logged in
#         user_profile = Profile.objects.get(user=request.user)
#         # Set is_prime_user to True
#         user_profile.is_prime_user = True
#         user_profile.save()
#         # Redirect to a success page
#         return redirect(reverse('payment_success'))
#     else:
#         # If the request method is not POST, redirect back to the payment page
#         return redirect('payment')
def update_profile(request):
    if request.method == 'POST':
        try:
            # Assuming the user is logged in
            user_profile = Profile.objects.get(user=request.user)
            
            # Set is_prime_user to True
            user_profile.is_prime_user = True
            
            # Set subscription start date to current date if not set
            if not user_profile.subscription_start_date:
                user_profile.subscription_start_date = timezone.now().date()
            
            # Get user-inputted expiry date from the form
            expiry_date_str = request.POST.get('subscription_expiry_date')
            
            # Parse user-inputted expiry date and update profile
            if expiry_date_str:
                new_expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
                # Only update expiry date if it's in the future
                if new_expiry_date >= timezone.now().date():
                    user_profile.subscription_expiry_date = new_expiry_date
            else:
                # If no expiry date provided, default to 30 days from start date
                user_profile.subscription_expiry_date = user_profile.subscription_start_date + timedelta(days=30)
            
            user_profile.save()
            
            # Redirect to a success page
            return redirect(reverse('payment_success'))
        except Profile.DoesNotExist:
            error_message = "Profile does not exist for the logged-in user."
            return render(request, 'error_page.html', {'error_message': error_message})
    else:
        # If the request method is not POST, redirect back to the payment page
        return redirect('payment')
#----------------------------------------------

def payment_success(request):
    return render(request, 'payment_success.html')

# class UpdateUserRoleView(View):
#     template_name = 'edit-role.html'

#     def get(self, request):
#         users = User.objects.all()
#         return render(request, self.template_name, {'users': users})

#     def post(self, request):
#         user_id = request.POST.get('user')
#         role = request.POST.get('role')
        
#         # Update user role based on the selected option
#         user = User.objects.get(pk=user_id)
#         if role == 'staff':
#             user.is_staff = True
#         elif role == 'regular':
#             user.is_staff = False
#         user.save()
        
#         return HttpResponseRedirect(reverse('update-user-role'))
@method_decorator(login_required, name='dispatch')
@method_decorator(superuser_required, name='dispatch')
class UpdateUserRoleView(View):
    template_name = 'edit-role.html'

    def get(self, request):
        users = User.objects.all()
        return render(request, self.template_name, {'users': users})

    def post(self, request):
        user_id = request.POST.get('user')
        role = request.POST.get('role')
        
        user = User.objects.get(pk=user_id)
        if role == 'staff':
            user.is_staff = True
            user.is_superuser = False  # Make sure to set is_superuser to False
            user.save()
            return HttpResponse(f'{user.username} has been promoted to staff role.')
        elif role == 'regular':
            user.is_staff = False
            user.is_superuser = False  # Make sure to set is_superuser to False
            user.save()
            return HttpResponse(f'{user.username} has been demoted to regular user role.')
        elif role == 'superuser':
            user.is_staff = True
            user.is_superuser = True
            user.save()
            return HttpResponse(f'{user.username} has been promoted to superuser.')
        
        return HttpResponseRedirect(reverse('update-user-role'))
    
# @method_decorator(superuser_required, name='dispatch')
@method_decorator(staff_required, name='dispatch')
class StaffDashboard(ListView):
    model = Post
    template_name = name='s-dashboard.html'
    context_object_name = 'userpost'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = User.objects.all()  # Fetch all authors from the User model
        return context

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        if author_id and author_id != 'btn-all':
            return Post.objects.filter(author__id=author_id)
        else:
            return Post.objects.all()
    # ordering = ['-id']
    
    ordering = ['-post_date']
    
@method_decorator(superuser_required, name='dispatch')   
class AdminDashboard(ListView):
    model = Post
    template_name = 'admin-dashboard.html'
    context_object_name = 'userpost'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = User.objects.all()  # Fetch all authors from the User model
        return context

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        if author_id and author_id != 'btn-all':
            return Post.objects.filter(author__id=author_id)
        else:
            return Post.objects.all()


    
# def AuthorPost(request):
#     userpostid=user.id
#     return render(request,'author-post.html')

# class AuthorPost(ListView):
#     model = Post
#     template_name = name='author-post.html'
#     context_object_name = 'userpost'

#     def get_queryset(self):
#         return Post.objects.filter(author_id = self.request.user.id)

         
# class AuthorPost(ListView):
#     model = Post
#     template_name = 'author-post.html'
#     context_object_name = 'userpost'

#     def get_queryset(self):
#         return Post.objects.filter(author_id=self.request.user.id)
# class AuthorPost(ListView):
#     model = Post
#     template_name = 'author-post.html'
#     context_object_name = 'userpost'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['authors'] = Post.objects.all()
#         return context

#     def get_queryset(self):
#         author_id = self.request.GET.get('author')
#         if author_id:
#             return Post.objects.filter(author__id=author_id)
#         else:
#             return Post.objects.none()

# class AuthorPost(ListView):
#     model = Post
#     template_name = 'author-post.html'
#     context_object_name = 'userpost'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['authors'] = User.objects.all()  # Fetch all authors from the User model
#         return context

#     def get_queryset(self):
#         author_id = self.request.GET.get('author')
#         allpost=self.request.GET.get('btn-all')
#         if author_id:
#             return Post.objects.filter(author__id=author_id)
        
#         elif allpost:
#             return Post.objects.all()
class AuthorPost(ListView):
    model = Post
    template_name = 'author-post.html'
    context_object_name = 'userpost'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = User.objects.all()  # Fetch all authors from the User model
        return context

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        if author_id and author_id != 'btn-all':
            return Post.objects.filter(author__id=author_id)
        else:
            return Post.objects.all()
        
# class AllTables(ListView):
#     model = User
#     template_name = 'all-tables.html'

class AllTables(ListView):
    model = User
    template_name = 'all-tables.html'
    context_object_name = 'users'

class UpdateUserView(UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'all-tables.html'  # Replace 'update_user.html' with your actual template name

class DeleteUser(DeleteView):
    model = User
    success_url = reverse_lazy('AllTables')  # Corrected URL name to match 'AllTables'
    template_name = 'all-tables.html'
    
    
class LegalPage(ListView):
    model = Post
    template_name = 'legalpage.html'
    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save form data in the database
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            ContactEntry.objects.create(name=name, email=email, message=message)
            
            # Compose email message
            subject = 'Contact Form Submission'
            message_body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
            sender_email = settings.EMAIL_HOST_USER
            recipient_email = 'aghodakiya98@gmail.com'  # Replace with your email address
            
            # Send email
            send_mail(subject, message_body, sender_email, [recipient_email])
            
            return redirect('success')  # Redirect to success page after sending email
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['message']

#             contact_entry = ContactEntry.objects.create(name=name, email=email, subject=subject, message=message)
#             contact_entry.save()

#         # EmailMessage(
#         #        'Contact Form Submission from {}'.format(name),
#         #        message,
#         #        'form-response@example.com', # Send from (your website)
#         #        ['aghodakiya98@gmail.com'], # Send to (your admin email)
#         #        [],
#         #        reply_to=[email] # Email from the form to get back to
#         #    ).send()

#         return redirect('success')
#     else:
#         form = ContactForm()
#     return render(request, 'legalpage.html', {'form': form})


def success(request):
   return HttpResponse('Success!')

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Save email in the database
            NewsletterSubscription.objects.create(email=email)
            
            # Compose email message for user
            user_subject = 'Newsletter Subscription'
            user_message_body = f'Thank you for subscribing to our newsletter! You will receive updates and news regularly.'
            user_sender_email = settings.EMAIL_HOST_USER
            
            # Send email to user
            send_mail(user_subject, user_message_body, user_sender_email, [email])
            
            # Compose email message for admin
            admin_subject = 'New Newsletter Subscription'
            admin_message_body = f'A new user has subscribed to the newsletter.\nEmail: {email}'
            admin_sender_email = settings.EMAIL_HOST_USER
            admin_recipient_email = 'aghodakiya98@gmail.com'  # Enter your email address here
            
            # Send email to admin
            send_mail(admin_subject, admin_message_body, admin_sender_email, [admin_recipient_email])
            
            return render(request, 'success_message.html')  # You can customize this response as needed
    return HttpResponse('Invalid request')  # Handle invalid requests
    
    
# def subscribe_newsletter(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         if email:
#             NewsletterSubscription.objects.create(email=email)
#             return render(request, 'success_message.html')  # You can customize this response as needed
#     return HttpResponse('Invalid request')  # Handle invalid requests

def PrivacyPolicy(request):
    return render(request,'privacy-policy.html')

def check_for_new_posts(request):
    # Logic to check for new posts (e.g., comparing current post count with previous count)
    has_new_posts = True  # Placeholder logic

    return JsonResponse({'has_new_posts': has_new_posts})

@login_required
def manage_membership(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'make_prime':
            user_id = request.POST.get('user_id')
            try:
                profile = Profile.objects.get(user_id=user_id)
                profile.is_prime_user = True
                profile.set_subscription_dates()  # Update subscription dates
                profile.save()
                messages.success(request, 'User is now a prime member.')
            except Profile.DoesNotExist:
                messages.error(request, 'User profile not found.')

        elif action == 'end_membership':
            user_id = request.POST.get('user_id')
            try:
                profile = Profile.objects.get(user_id=user_id)
                profile.is_prime_user = False
                profile.subscription_start_date = None
                profile.subscription_expiry_date = None
                profile.save()
                messages.success(request, 'Membership ended for the user.')
            except Profile.DoesNotExist:
                messages.error(request, 'User profile not found.')

    return redirect('admin_dashboard') 

# def posttable(request):
#     posts = Post.objects.all()
#     users = User.objects.all()
#     return render(request, 'posttable.html', {'posts': posts})

# def posttableupdate(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
    
#     # Get the author ID from the request data
#     author_id = request.POST.get('author_id')
    
#     # Check if the user exists
#     try:
#         author = User.objects.get(pk=author_id)
#     except User.DoesNotExist:
#         # Handle the case where the user does not exist
#         # For example, redirect to an error page or display a message to the user
#         return HttpResponse("User does not exist", status=404)
    
#     # Update the post with the new author
#     post.author = author
#     # Update other fields as needed
#     post.title = request.POST.get('title')
#     # Save the updated post
#     post.save()
    
#     # Redirect to some page after successful update
#     return redirect('posttable')

# def posttabledelete(request, post_id):
#     # Retrieve the post object or return 404 if not found
#     post = get_object_or_404(Post, pk=post_id)
    
#     # Attempt to delete the post
#     try:
#         post.delete()
#         return redirect('posttable')  # Redirect to the post table page after successful deletion
#     except Exception as e:
#         # Log the exception for debugging purposes
#         print(f"Error deleting post: {e}")
#         # You can return an error response here if needed, or handle the error differently
#         return HttpResponse("An error occurred while deleting the post", status=500)

def posttable(request):
    posts = Post.objects.all()
    users = User.objects.all()
    categories = Category.objects.all()
    return render(request, 'posttable.html', {'posts': posts, 'users': users, 'categories': categories})

def posttableupdate(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')  # Change to 'author' instead of 'author_id'
        category_id = request.POST.get('category')  # Change to 'category' instead of 'category_name'
        
        # Retrieve the User instance based on author_id
        try:
            author = User.objects.get(pk=author_id)
        except User.DoesNotExist:
            return HttpResponse("User does not exist", status=404)
        
        # Retrieve the Category instance based on category_id
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return HttpResponse("Category does not exist", status=404)
        
        # Update post attributes
        post.title = title
        post.author = author
        post.category = category
        post.save()
        
        return redirect('posttable')
    
    return HttpResponse("Invalid Request")

def posttabledelete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('posttable')
    return HttpResponse("Invalid Request")

# -----------------------------------------

def emaildashboard(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        recipients = request.POST.getlist('recipients')
        
        for recipient in recipients:
            send_mail(subject, body, 'aghodakiya98@gmail.com', [recipient])
        
        # Optionally, you can redirect the user after sending emails
        return render(request, 'emaildashboard_success.html')

    subscribers = NewsletterSubscription.objects.all()
    return render(request, 'emaildashboard.html', {'subscribers': subscribers})


@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user, read=False)
    return render(request, 'notifications.html', {'notifications': notifications})

def mark_as_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, read=False).update(read=True)
    return redirect('notifications')
