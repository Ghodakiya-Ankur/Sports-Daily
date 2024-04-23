# sdmember/views.py
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, EditProfileForm
from sdblogapp.models import *
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from sdblog.settings import EMAIL_HOST_USER
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import OTP
from django.urls import reverse
from twilio.rest import Client
import os
import random
from django.db import transaction
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView


class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    success_message = "Your account has been created successfully. You can now log in."

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        email = self.request.POST.get('email')
        phone = self.request.POST.get('phone_number')

        # Generate random OTP
        otp = str(random.randint(100000, 999999))

        # Store OTP in the database along with user's email and phone number
        expiry_time = timezone.now() + timezone.timedelta(minutes=1)
        OTP.objects.create(user=user, otp=otp, expiry_time=expiry_time)

        # Send OTP via email
        send_mail("User Data:", f"Verify Your Mail by the OTP: {otp}", settings.EMAIL_HOST_USER, [email], fail_silently=True)

        # Send OTP via SMS using Twilio
        send_otp_sms(phone, otp)  # Pass the same OTP for SMS

        messages.success(self.request, 'User saved Successfully')

        # Pass OTP to the verification template for displaying to the user
        return render(self.request, 'registration/verify_otp.html', {'otp': otp})

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check for and delete expired OTPs
        expired_otps = OTP.objects.filter(expiry_time__lt=timezone.now())
        expired_otps.delete()
        return context
    # def send_otp_sms(phone_number, otp):
#     account_sid = "AC9213a47561dd259923b4e87795145fc7"
#     auth_token = "a279acde1e910e6ec321546e04f25f08"
#     verify_sid = "VAf2cae864ae61adbbd7404a6eb11519fb"
    
#     client = Client(account_sid, auth_token)

#     verification = client.verify.v2.services(verify_sid) \
#       .verifications \
#       .create(to=phone_number, channel="sms", code=otp)
#     print(verification.status)
# ------------------------------------------------------

#this is final otp system code 
# def send_otp_sms(phone_number, otp):
#     # Twilio account credentials
#     account_sid = "AC9213a47561dd259923b4e87795145fc7"
#     auth_token = "a279acde1e910e6ec321546e04f25f08"
#     twilio_phone_number = "+12108710951"

#     # Initialize Twilio client
#     client = Client(account_sid, auth_token)

#     try:
#         # Sending SMS with OTP
#         message = client.messages.create(
#             body=f"Your OTP is: {otp}",
#             from_=twilio_phone_number,
#             to=phone_number
#         )
#         print(f"SMS sent successfully to {phone_number}. SID: {message.sid}")
#         return True  # Return True indicating successful SMS delivery
#     except Exception as e:
#         print(f"Error occurred while sending SMS: {e}")
#         return False  # Return False indicating failure to send SMS
def send_otp_sms(phone_number, otp):
    # Twilio account credentials
    account_sid = "AC9213a47561dd259923b4e87795145fc7"
    auth_token = "a279acde1e910e6ec321546e04f25f08"
    twilio_phone_number = "+12108710951"

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    try:
        # Customizing SMS with OTP message
        message_body = f"Your custom OTP message: {otp}"
        
        # Sending SMS with OTP
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=phone_number
        )
        print(f"SMS sent successfully to {phone_number}. SID: {message.sid}")
        return True  # Return True indicating successful SMS delivery
    except Exception as e:
        print(f"Error occurred while sending SMS: {e}")
        return False  # Return False indicating failure to send SMS"
#----------------------------------------------------------------------
# def send_otp_sms(phone_number, otp):
#     # Twilio account credentials
#     account_sid = "AC9213a47561dd259923b4e87795145fc7"
#     auth_token = "a279acde1e910e6ec321546e04f25f08"
#     verify_sid = "VAf2cae864ae61adbbd7404a6eb11519fb"
    
#     client = Client(account_sid, auth_token)

#     # Sending SMS with OTP
#     try:
#         verification = client.verify.v2.services(verify_sid) \
#             .verifications \
#             .create(to=phone_number, channel="sms", code=otp)
#         print(verification.status)  # Print Twilio verification status for debugging
#     except Exception as e:
#         print(f"Error occurred while sending SMS: {e}")  # Print error message if SMS sending fails

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp_entered = request.POST.get('otp')

        try:
            # Retrieve the OTP entry from the database based on OTP value
            otp_obj = OTP.objects.get(otp=otp_entered)

            # Compare entered OTP with stored OTP
            if otp_obj.otp == otp_entered:
                # Check if 'phone_number' key exists in the session before deleting it
                if 'phone_number' in request.session:
                    del request.session['phone_number']
                otp_obj.delete()

                messages.success(request, 'OTP verified. You are now logged in.')
                return render(request, 'registration/verification_success.html')

            else:
                # Invalid OTP, display error message
                messages.error(request, 'Invalid OTP. Please try again.')
                return render(request, 'registration/error.html')

        except OTP.DoesNotExist:
            # OTP entry does not exist or OTP is incorrect, display error message
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'registration/error.html')

    return render(request, 'registration/verify_otp.html')

# class UserRegisterView(CreateView):
#     form_class = CustomUserCreationForm
#     template_name = 'registration/register.html'
#     success_url = reverse_lazy('login')

#     def form_valid(self, form):
#         # Save the user and set the password
#         user = form.save(commit=False)
#         user.set_password(form.cleaned_data['password'])
#         user.save()
#         return super().form_valid(form)
from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def verify_otp(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         otp_entered = request.POST.get('otp')
        
#         try:
#             # Retrieve the OTP entry from the database based on email and OTP value
#             otp_obj = OTP.objects.get(otp=otp_entered)
            
#             # No need to check for expiry_time
            
#             # Mark OTP as verified or perform necessary actions
#             # For example: otp_obj.verified = True
#             # otp_obj.save()
            
#             # Redirect to a success page or perform other actions
#             return render(request, 'registration/verification_success.html')
            
#         except OTP.DoesNotExist:
#             # OTP entry does not exist or OTP is incorrect, display error message
#             messages.error(request, 'Invalid OTP. Please try again.')
#             return render(request, 'registration/error.html')  # Redirect to the error.html template
    
#     # If request method is not POST or if the form data is invalid, render the OTP verification page
#     return render(request, 'registration/verify_otp.html')



# def error_otp(request):
#     return render(request, 'registration/error.html')
    
# class UserRegisterView(SuccessMessageMixin, CreateView):
#     form_class = CustomUserCreationForm
#     template_name = 'registration/register.html'
#     success_url = reverse_lazy('login')
#     success_message = "Your account has been created successfully. You can now log in."

#     def form_valid(self, form):
#         # Save the user and set the password
#         user = form.save(commit=False)
#         user.set_password(form.cleaned_data['password'])
#         user.save()

#         email = self.request.POST.get('email')  # Accessing request object
#         otp = random.randint(100000, 999999)
        
#         # Sending email notification
#         send_mail("User Data:", f"Verify Your Mail by the OTP: {otp}", EMAIL_HOST_USER, [email], fail_silently=True)
        
#         messages.success(self.request, 'User saved Successfully')

#         # Render the verify.html template with the generated OTP
#         return render(self.request, 'registration/verify_otp.html', {'otp': otp})  

#     def form_invalid(self, form):
#         # Add error messages to the form
#         for field, errors in form.errors.items():
#             for error in errors:
#                 messages.error(self.request, f"{field}: {error}")
#         return super().form_invalid(form)

#------------------------------------------------------
# class UserRegisterView(SuccessMessageMixin, CreateView):
#     form_class = CustomUserCreationForm
#     template_name = 'registration/register.html'
#     success_url = reverse_lazy('login')
#     success_message = "Your account has been created successfully. You can now log in."

#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.set_password(form.cleaned_data['password'])
#         user.save()

#         email = self.request.POST.get('email')
        
#         self.request.session['phone_number'] = self.request.POST.get('phone_number')
#         phone = self.request.session.get('phone_number')
#         otp = random.randint(100000, 999999)
        
#         send_mail("User Data:", f"Verify Your Mail by the OTP: {otp}", EMAIL_HOST_USER, [email], fail_silently=True)
        
#         expiry_time = timezone.now() + timezone.timedelta(minutes=1)
        
#         OTP.objects.create(user=user, otp=otp, expiry_time=expiry_time)
        
#         send_otp_sms(phone)
        
        
#         messages.success(self.request, 'User saved Successfully')

#         return render(self.request, 'registration/verify_otp.html', {'otp': otp})
    
      

#     def form_invalid(self, form):
#         for field, errors in form.errors.items():
#             for error in errors:
#                 messages.error(self.request, f"{field}: {error}")
#         return super().form_invalid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Check for and delete expired OTPs
#         expired_otps = OTP.objects.filter(expiry_time__lt=timezone.now())
#         expired_otps.delete()
#         return context
    
#     def verify_otp(request, self):
#         if request.method == 'POST':
#             email = request.POST.get('email')
#             otp_entered = request.POST.get('otp')
            
#             try:
#                 # Retrieve the OTP entry from the database based on OTP value
#                 otp_obj = OTP.objects.get(otp=otp_entered)
#                 phone_number = self.request.session.get('phone_number', None)
#                 print(phone_number)
#                 phone_verification_status = verify_otp_sms(phone_number, otp_entered)
#                 if phone_verification_status == 'approved' or otp_obj:
#                     # Clear the OTP and registration-related session variables after successful verification
#                     del self.request.session['phone_number']

#                     messages.success(request, 'OTP verified. You are now logged in.')
                
#                 # No need to check for expiry_time
                
#                 # Mark OTP as verified or perform necessary actions
#                 # For example: otp_obj.verified = True
#                 # otp_obj.save()
                
#                 # Redirect to a success page or perform other actions
#                 # Now, delete the OTP entry from the database
#                     otp_obj.delete()
#                     return render(request, 'registration/verification_success.html')
                
#             except OTP.DoesNotExist:
#                 # OTP entry does not exist or OTP is incorrect, display error message
#                 messages.error(request, 'Invalid OTP. Please try again.')
#                 return render(request, 'registration/error.html')  # Redirect to the error.html template
        
#         # If request method is not POST or if the form data is invalid, render the OTP verification page
#         return render(request, 'registration/verify_otp.html')
# class UserRegisterView(SuccessMessageMixin, CreateView):
#     form_class = CustomUserCreationForm
#     template_name = 'registration/register.html'
#     success_url = reverse_lazy('login')
#     success_message = "Your account has been created successfully. You can now log in."

#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.set_password(form.cleaned_data['password'])
#         user.save()

#         email = self.request.POST.get('email')
#         phone = self.request.POST.get('phone_number')

#         # Generate random OTP
#         otp = str(random.randint(100000, 999999))

#         # Store OTP in the database along with user's email and phone number
#         expiry_time = timezone.now() + timezone.timedelta(minutes=1)
#         OTP.objects.create(user=user, otp=otp, expiry_time=expiry_time)

#         # Send OTP via email
#         send_mail("User Data:", f"Verify Your Mail by the OTP: {otp}", settings.EMAIL_HOST_USER, [email], fail_silently=True)

#         # Send OTP via SMS using Twilio
#         send_otp_sms(phone, otp)

#         messages.success(self.request, 'User saved Successfully')

#         # Pass OTP to the verification template for displaying to the user
#         return render(self.request, 'registration/verify_otp.html', {'otp': otp})

#     def form_invalid(self, form):
#         for field, errors in form.errors.items():
#             for error in errors:
#                 messages.error(self.request, f"{field}: {error}")
#         return super().form_invalid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Check for and delete expired OTPs
#         expired_otps = OTP.objects.filter(expiry_time__lt=timezone.now())
#         expired_otps.delete()
#         return context

# def send_otp_sms(phone_number, otp):
#     account_sid = "AC9213a47561dd259923b4e87795145fc7"
#     auth_token = "a279acde1e910e6ec321546e04f25f08"
#     verify_sid = "VAf2cae864ae61adbbd7404a6eb11519fb"
    
#     client = Client(account_sid, auth_token)

#     verification = client.verify.v2.services(verify_sid) \
#         .verifications \
#         .create(to=phone_number, channel="sms", code=otp)
    
#     print(verification.status)
# #------------------------------------------------------
#send sms

# def send_otp_sms(phone_number, otp):
#     account_sid = "AC9213a47561dd259923b4e87795145fc7"
#     auth_token = "a279acde1e910e6ec321546e04f25f08"
#     verify_sid = "VAf2cae864ae61adbbd7404a6eb11519fb"
    
#     client = Client(account_sid, auth_token)

#     verification = client.verify.v2.services(verify_sid) \
#       .verifications \
#       .create(to=phone_number, channel="sms", code=otp)
#     print(verification.status)
    
# def verify_otp_sms(phone_number, entered_otp):
#     account_sid = "ACa976f99952fbbb1edb4fbac7488c25b8"
#     auth_token = "08a880cdfcc2deaca1c2fc927b2a7c9b"
#     verify_sid = "VA271c6a27f997618790efa8b7a5082852"

#     client = Client(account_sid, auth_token)

#     try:
#         verification_check = client.verify.v2.services(verify_sid) \
#             .verification_checks \
#             .create(to=phone_number, code=entered_otp)
#         return verification_check.status
#     except Exception as e:
#         # Handle any exceptions that may occur during the verification check
#         print(f"Error during OTP verification: {e}")
#         return None
    



    
# def verify_otp(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         otp_entered = request.POST.get('otp')

#         try:
#             # Retrieve the OTP entry from the database based on OTP value
#             otp_obj = OTP.objects.get(otp=otp_entered)

#             # Compare entered OTP with stored OTP
#             if otp_obj.otp == otp_entered:
#                 # Clear the OTP and registration-related session variables after successful verification
#                 del request.session['phone_number']
#                 otp_obj.delete()

#                 messages.success(request, 'OTP verified. You are now logged in.')
#                 return render(request, 'registration/verification_success.html')

#             else:
#                 # Invalid OTP, display error message
#                 messages.error(request, 'Invalid OTP. Please try again.')
#                 return render(request, 'registration/error.html')

#         except OTP.DoesNotExist:
#             # OTP entry does not exist or OTP is incorrect, display error message
#             messages.error(request, 'Invalid OTP. Please try again.')
#             return render(request, 'registration/error.html')

#     return render(request, 'registration/verify_otp.html')


# ------------------------------------------------------
# class UserRegisterView(SuccessMessageMixin, CreateView):
#     form_class = CustomUserCreationForm
#     template_name = 'registration/register.html'
#     success_url = reverse_lazy('login')
#     success_message = "Your account has been created successfully. You can now log in."

#     def form_valid(self, form):
#         # Save the user and set the password
#         user = form.save(commit=False)
#         user.set_password(form.cleaned_data['password'])
#         user.save()

#         email = self.request.POST.get('email')
#         otp = random.randint(100000, 999999)
        
#         # Sending email notification
#         send_mail("User Data:", f"Verify Your Mail by the OTP: {otp}", EMAIL_HOST_USER, [email], fail_silently=True)
        
#         # Calculate expiry time for OTP (e.g., 15 minutes from now)
#         expiry_time = timezone.now() + timezone.timedelta(minutes=1)
        
#         # Store OTP in the database
#         otp_instance = OTP.objects.create(user=user, otp=otp, expiry_time=expiry_time)
        
#         messages.success(self.request, 'User saved Successfully')

#         # Render the verify.html template with the generated OTP
#         return render(self.request, 'registration/verify_otp.html', {'otp': otp})  

#     def form_invalid(self, form):
#         # Add error messages to the form
#         for field, errors in form.errors.items():
#             for error in errors:
#                 messages.error(self.request, f"{field}: {error}")
#         return super().form_invalid(form)
    
    
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')

    
# class UserEditView(LoginRequiredMixin, UpdateView):
#     model=Profile
#     form_class = EditProfileForm
#     template_name = 'registration/edit-profile.html'
#     success_url = reverse_lazy('home')
    
#     def get_object(self):
#         return self.request.user

class UserEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'registration/edit-profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user  # Assuming the user has a profile associated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_prime_user'] = self.request.user.profile.is_prime_user
        return context
    
def logout_view(request):
    logout(request)
    # Redirect to a success page or any other page after logout
    return redirect('landingpage/')

#-----------------------------------------

# Download the helper library from https://www.twilio.com/docs/python/install
# import os
# from twilio.rest import Client

# # Set environment variables for your credentials
# # Read more at http://twil.io/secure
# account_sid = "AC9213a47561dd259923b4e87795145fc7"
# auth_token = "a279acde1e910e6ec321546e04f25f08"
# verify_sid = "VAf2cae864ae61adbbd7404a6eb11519fb"
# verified_number = "+1 2108710951"

# client = Client(account_sid, auth_token)

# verification = client.verify.v2.services(verify_sid) \
#   .verifications \
#   .create(to=verified_number, channel="sms")
# print(verification.status)

# otp_code = input("Please enter the OTP:")

# verification_check = client.verify.v2.services(verify_sid) \
#   .verification_checks \
#   .create(to=verified_number, code=otp_code)
# print(verification_check.status)
    
    




#-----------------------------------------------

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')