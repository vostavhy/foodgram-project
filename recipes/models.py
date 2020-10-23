from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields import files

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    name = models.TextField()
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    preparation_time = models.IntegerField()  # время приготовления в минутах
    image = models.ImageField(upload_to='recipes_images/')  # поле для рисунка
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)


