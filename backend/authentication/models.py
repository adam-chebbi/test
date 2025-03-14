from django.db import models, transaction
from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator
from core.utils import generate_unique_id
from django.db import IntegrityError

class Profile(models.Model):
    ROLES = (
        ('SUPER-ADMIN', 'Super Admin'),
        ('ADMIN', 'Admin'),
        ('MODERATOR', 'Moderator'),
        ('USER', 'User'),
        ('GUEST', 'Guest'),
    )

    id = models.CharField(
        primary_key=True,
        max_length=20,
        default=generate_unique_id('PRF'),
        editable=False
    )
    name = models.CharField(max_length=20, choices=ROLES, default='USER')
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    createdById = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='created_profiles')
    lastModifiedById = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='modified_profiles')

    class Meta:
        db_table = 'Profile'

    def save(self, *args, **kwargs):
        if not self.id:
            with transaction.atomic():
                self.id = generate_unique_id("PRF", Profile)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class User(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=20,
        default=generate_unique_id('USR'),
        editable=False
    )
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    name = models.CharField(max_length=101, blank=True)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    username = models.CharField(max_length=50, unique=True)
    profileName = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='users')
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    createdById = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='created_users')
    lastModifiedById = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='modified_users')
    isActive = models.BooleanField(default=True)

    class Meta:
        db_table = 'User'

    def save(self, *args, **kwargs):
        if not self.id:
            with transaction.atomic():
                self.id = generate_unique_id("USR", User)
                if not self.username:
                    self.username = self.email.split('@')[0]
                self.name = f"{self.firstName} {self.lastName.upper()}"
        else:
            self.name = f"{self.firstName} {self.lastName.upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.username})"

class Login(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=20,
        default=generate_unique_id('LGN'),
        editable=False
    )
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logins')
    token1 = models.CharField(max_length=255)  # Hashed email + password
    token2 = models.CharField(max_length=255)  # Hashed username + password
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    createdById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_logins')
    lastModifiedById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_logins')
    isActive = models.BooleanField(default=True)

    class Meta:
        db_table = 'Login'

    def save(self, *args, **kwargs):
        if not self.id:
            with transaction.atomic():
                self.id = generate_unique_id("LGN", Login)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Login for {self.userId.username}"

class Session(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=20,
        default=generate_unique_id('SES'),
        editable=False
    )
    code = models.CharField(max_length=50, unique=True)
    action = models.CharField(max_length=100)
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModifiedDate = models.DateTimeField(auto_now=True)
    createdById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_sessions')
    lastModifiedById = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_sessions')
    isActive = models.BooleanField(default=True)

    class Meta:
        db_table = 'Session'

    def save(self, *args, **kwargs):
        if not self.id:
            with transaction.atomic():
                self.id = generate_unique_id("SES", Session)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Session {self.code} - {self.action}"