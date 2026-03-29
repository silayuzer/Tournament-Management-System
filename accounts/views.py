from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import RegistrationForm
from .models import User, EmailConfirmation
from .models import PasswordResetToken



# Create your views here.
def login_view(request):
    if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("password")

        user=authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect("/admin/")
            return redirect("/")
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.set_password(form.cleaned_data["password"])
            user.save()

            confirmation=EmailConfirmation.objects.create(user=user)
            confirm_link=request.build_absolute_uri(
                reverse("accounts:confirm_email", args=[confirmation.token])
            )
            print("EMAIL DEBUG:", user.email)
            send_mail(
                subject="Confirm your account",
                message=f"Please confirm your account by clicking the following link:\n{confirm_link}",
                from_email=None,
                recipient_list=[user.email],
            )
            return HttpResponse("Registration successful! Please check your email to confirm your account.")
    else:
        form=RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})

def confirm_email(request, token):
    confirmation = get_object_or_404(EmailConfirmation, token=token)
    if confirmation.is_expired():
        confirmation.delete()
        return HttpResponse("Confirmation link has expired.")
    user = confirmation.user
    user.is_active = True
    user.save()
    confirmation.delete()  
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect("homepage")


User=get_user_model()
def forgot_password(request):
    if request.method == "POST":
        email=request.POST.get("email")
        user=User.objects.filter(email=email).first()
        
        if user:
            reset=PasswordResetToken.objects.create(user=user)
            reset_link=request.build_absolute_uri(
                reverse("accounts:reset_password", args=[reset.token])
            )
            send_mail(
                "Password Reset",
                f"Reset your password using the following link:\n{reset_link}",
                None,
                [email],
            )
        return HttpResponse("If an account with that email exists, a password reset link has been sent.")
    return render(request, "accounts/forgot_password.html")

def reset_password(request, token):
    reset=get_object_or_404(PasswordResetToken, token=token)
    if reset.is_expired():
        reset.delete()
        return HttpResponse("Password reset link has expired.")
    
    if request.method == "POST":
        password=request.POST.get("password")
        confirm=request.POST.get("confirm_password")

        if password!=confirm:
            messages.error(request, "Passwords do not match.")
        else:
            user=reset.user
            user.set_password(password)
            user.save()
            reset.delete()
            return redirect("accounts:login")
    return render(request, "accounts/reset_password.html", {"token": token})

