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

    # взаимодействие с моделью User
    # страница всех рецептов, созданных определенным пользователем
    path('<username>/', views.profile, name='profile'),
    # подписаться
    path('<username>/follow', views.profile_follow, name='profile_follow'),
    # отписаться
    path('<username>/unfollow', views.profile_unfollow, name='profile_unfollow'),
    # страница с рецептами авторов, на которых подписан пользователь
    path('follow/', views.follow_index, name='follow_index'),

    # взаимодействие с моделью Favorite - список избранного
    # добавить рецепт в избранное
    path('<int:recipe_id>/favorite_add', views.favorite_add, name='favorite_add'),
    path('<int:recipe_id>/favorite_delete', views.favorite_delete, name='favorite_delete'),
    # страница избранного
    path('favorite/', views.favorite_index, name='favorite_index'),

    # взаимодействие с моделью Order - список покупок
    # добавить рецепт в список покупок
    path('<int:recipe_id>/order_add', views.order_add, name='order_add'),
    path('<int:recipe_id>/order_delete', views.order_delete, name='order_delete'),
    # страница списка покупок
    path('order/', views.order_index, name='order_index'),
]
