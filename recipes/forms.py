from django import forms

from .models import Recipe


# класс формы для создания рецептов
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'tags', 'preparation_time', 'description', 'image')
