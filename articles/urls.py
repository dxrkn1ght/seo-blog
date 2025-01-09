from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('create-post/', views.create_post, name='create-post'),
    path('create-author/', views.create_author, name='create-author'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('detail/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='detail'),
    path('category/<str:category>/', views.article_by_category, name='category')

]