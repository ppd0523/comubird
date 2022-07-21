from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, agreement, password=None):
        if not email:
            raise ValueError('Users must have an Email address')

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            agreement=agreement,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, agreement=True, password=None):
        user = self.create_user(
            email,
            nickname=nickname,
            password=password,
            agreement=agreement,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=100,
        unique=True,
        null=False,
        blank=False,
    )
    nickname = models.CharField(max_length=20, unique=True, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    # pfp = models.ImageField(blank=True, null=True, upload_to=upload_pfp)
    agreement = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ('nickname', 'agreement')

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
