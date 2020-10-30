from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # взаимодействие с моделью Recipe
    # создать новый рецепт
    path('new/', views.new_recipe, name='new_recipe'),
    # страница рецепта
    path('<int:recipe_id>/', views.recipe_index, name='recipe_index'),
    path('<int:recipe_id>/edit', views.recipe_edit, name='recipe_edit'),
    path('<int:recipe_id>/delete', views.recipe_delete, name='recipe_delete'),

    # страница всех рецептов, созданных определенным пользователем
    path('user/<username>/', views.index, name='profile_index'),

    # страница с рецептами авторов, на которых подписан пользователь
    path('subscription/', views.follow_index, name='subscription_index'),

    # страница избранного
    path('favorite/', views.index, name='favorite_index'),

    # страница списка покупок
    path('purchase/', views.purchase_index, name='order_index'),

]
