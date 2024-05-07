from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django.urls import reverse

# Create your models here.

class Gamer(AbstractUser):
    user = models.CharField(max_length=15, blank=True, null=True)

class Category(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name='Категории')

    def __str__(self):
        return self.name

class Subclass(models.Model):

    tanks = 'TK'
    hils = 'HL'
    dd = 'DD'
    merchants = 'MH'
    guild_masters = 'GM'
    quest_givers = 'QM'
    blacksmiths = 'BS'
    tanners = 'TN'
    potion_makers = 'PM'
    spell_masters = 'SM'

    SUBCLASS_TYPES = [
        (tanks, 'Танки'),
        (hils, 'Хилы'),
        (dd, 'ДД'),
        (merchants, 'Торговцы'),
        (guild_masters, 'Гилдмастеры'),
        (quest_givers, 'Квестгиверы'),
        (blacksmiths, 'Кузнецы'),
        (tanners, 'Кожевники'),
        (potion_makers, 'Зельевары'),
        (spell_masters, 'Мастера заклинаний'),
    ]

    subclass_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    text = RichTextField()
    author = models.ForeignKey(Gamer, on_delete=models.CASCADE, verbose_name="Автор")
    category = models.ManyToManyField(Category, through='SubclassCategory', verbose_name="Категория")

    def __str__(self):
        return f'id-{self.pk}: {self.title}'

    def get_absolute_url(self):
        return reverse('subclass_detail', args=[str(self.pk)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class SubclassCategory(models.Model):
    subclass = models.ForeignKey(Subclass, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Response(models.Model):
    author = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    text_response = models.TextField(max_length=255)
    response_subclass = models.ForeignKey(Subclass, on_delete=models.CASCADE)
    date_in = models.DateTimeField(auto_now_add=True)
    response = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('myresponse', args=[str(self.response_subclass.id)])