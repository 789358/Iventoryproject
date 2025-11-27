from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import signup_view, contact_view
from .views import (
    login_view, home_view,
    ItemListView, ItemCreateView, ItemUpdateView, ItemDeleteView,
    MyLogoutView
)

urlpatterns = [
    path('', home_view, name='home'),  
    path('login/', login_view, name='login'),  
    path('signup/', signup_view, name='signup'),
    path('signup/success/', views.signup_success_view, name='signup_success'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('contact/', contact_view, name='contact'), 
    path('items/', ItemListView.as_view(), name='item_list'),
    path('items/add/', ItemCreateView.as_view(), name='item_add'),
    path('items/edit/<int:pk>/', ItemUpdateView.as_view(), name='item_edit'),
    path('items/delete/<int:pk>/', ItemDeleteView.as_view(), name='item_delete'),
]
