from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # взаимодействие с моделью Recipe
    # создать новый рецепт
    path('new/', views.new_recipe, name='new_recipe'),
    # страница рецепта
    path('<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('<int:recipe_id>/edit', views.recipe_edit, name='recipe_edit'),
    path('<int:recipe_id>/delete', views.recipe_delete, name='recipe_delete'),

    # страница всех рецептов, созданных определенным пользователем
    path('<username>/', views.profile, name='profile'),
    # страница с рецептами авторов, на которых подписан пользователь
    path('subscription/', views.follow_index, name='subscription_index'),

    # страница избранного
    path('favorite/', views.favorite_index, name='favorite_index'),

    # страница списка покупок
    path('order/', views.order_index, name='order_index'),

]
