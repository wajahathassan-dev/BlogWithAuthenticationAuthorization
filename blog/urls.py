from django.urls import path
from blog import views

urlpatterns = [
    path('api/register/', views.UserRegistrationView.as_view(), name='register'),
    path('api/posts/', views.Post.as_view(), name='get-all-or-add-post'),
    path('api/posts/<int:id>', views.SpecificPost.as_view(), name='get-update-delete-post'),
]