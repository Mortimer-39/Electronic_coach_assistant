from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле email обязательно для заполнения')
        email = self.normalize_email(email)

        # Убираем username из обязательных параметров, если мы его не используем
        user = self.model(
            email=email, 
            first_name=first_name,
            last_name=last_name, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user  # ВАЖНО: всегда возвращай объект user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True) # Суперюзер должен быть активным

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name, last_name, password, **extra_fields)


class CustomUser(AbstractUser):
    # 1. Email делаем основным идентификатором
    email = models.EmailField('Email адрес', unique=True, max_length=150)

    # 2. Убираем username совсем или делаем его необязательным
    username = None

    first_name = models.CharField('Имя', max_length=64)
    last_name = models.CharField('Фамилия', max_length=64)

    # 3. CRM для тренеров подразумевает телефон как главный контакт
    phone_number = models.CharField('Номер телефона', max_length=20, blank=True, null=True)

    # Исправляем опечатку adress -> address
    address = models.CharField('Адрес', max_length=255, blank=True, null=True)

    # 4. Скидка. Для CRM лучше использовать PositiveSmallIntegerField (экономия места)
    discount = models.PositiveSmallIntegerField(
        'Скидка (%)',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    # 5. Роли (Критично для CRM тренера)
    class Role(models.TextChoices):
        COACH = 'CH', 'Тренер'
        CLIENT = 'CL', 'Клиент'
        ADMIN = 'AD', 'Администратор'

    role = models.CharField(
        max_length=2, 
        choices=Role.choices,
        default=Role.CLIENT
    )

    objects = CustomUserManager() # Привязываем наш кастомный менеджер

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
