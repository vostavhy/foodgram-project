from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # взаимодействие с моделью Recipe
    # создать новый рецепт
    path('new/', views.recipe_create, name='recipe_create'),
    # страница рецепта
    path('recipe/<int:pk>/', views.recipe_index, name='recipe_index'),
    path('recipe/<int:pk>/edit', views.recipe_edit, name='recipe_edit'),
    path('recipe/<int:pk>/delete', views.recipe_delete, name='recipe_delete'),

    # страница всех рецептов, созданных определенным пользователем
    path('user/<username>/', views.index, name='profile_index'),

    # страница с рецептами авторов, на которых подписан пользователь
    path('subscription/', views.subscription_index, name='subscription_index'),

    # страница избранного
    path('favorite/', views.favorite_index, name='favorite_index'),

    # страница списка покупок
    path('purchase/', views.purchase_index, name='purchase_index'),
    # загрузить список покупок
    path('purchase_download/', views.download_purchase_list, name='download_purchase_list')

]
