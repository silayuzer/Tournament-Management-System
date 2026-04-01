from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_filds):
        if not email:
            raise ValueError("The Email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_filds)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
        ROLE_CHOICES = (
            ("organizer", "Organizer"),
            ("player", "Player")
        )
        email=models.EmailField(unique=True)
        role=models.CharField(max_length=20, choices=ROLE_CHOICES, default="player")
        first_name=models.CharField(max_length=150)
        last_name=models.CharField(max_length=150)

        is_active=models.BooleanField(default=True)
        is_staff=models.BooleanField(default=False)
        date_joined=models.DateTimeField(default=timezone.now)
        objects=UserManager()

        USERNAME_FIELD="email"
        REQUIERED_FIELDS=["username"]

        def __str__(self):
            full_name = f"{self.first_name} {self.last_name}".strip()
            return full_name if full_name else self.email
        
import uuid
from django.utils.timezone import now
from datetime import timedelta

class EmailConfirmation(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    token=models.UUIDField(default=uuid.uuid4, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return now()>self.created_at + timedelta(hours=24)
    
    def __str__(self):
        return f"EmailConfirmation for {self.user.email}"
    
class PasswordResetToken(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    token=models.UUIDField(default=uuid.uuid4, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now()>self.created_at + timedelta(hours=24)