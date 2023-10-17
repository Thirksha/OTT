from django.urls import path
from .views import home,logo,watchif, register, add_episode,register_subscriber,add_series,edit_content_movies,delete_movies,edit_content_kids, add_content_movies,add_content_kids,delete_kids, content_creator_home, admin, admin_home, add_user, toggle_user_status, user_list
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from . import views

urlpatterns = [
    path('home', home, name='home_path'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/register/', register, name='register'),
    path('account/register_subscriber/', register_subscriber, name='register_subscriber'),

    path('', logo, name='title_name_watchif'),

    path('watchif', watchif, name='watchif'),

    path('cchome/', content_creator_home, name='content_creator_home'),  # Corrected URL name
    path('accounts/add_content/', add_content_movies, name='add_content'),  # Corrected URL name
    path('edit_content_movies/<int:movies_id>/', edit_content_movies, name='edit_content_movies'),
    path('delete_movies/<int:movies_id>', delete_movies, name='delete_movies'),

path('kids_content/', views.kids_content_view, name='kids_content'),
path('kids_details/<int:kids_id>/', views.kids_details, name='kids_details'),
path('accounts/add_content_kids/', add_content_kids, name='add_content_kids'),  # Corrected URL name
path('edit_content_kids/<int:kids_id>/', edit_content_kids, name='edit_content_kids'),
path('delete_kids/<int:kids_id>', delete_kids, name='delete_kids'),


path('tv_shows/', views.tv_shows_view, name='tv_shows'),
path('tv_shows_details/<int:tv_shows_id>/', views.tv_shows_details, name='tv_shows_details'),
path('account/add_series/', add_series, name='add_series'),  # Corrected URL name
path('accounts/add_episode/<int:tv_show_id>/<int:season_id>/', add_episode, name='add_episode'),




    path('account/password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('account/password-change/done', PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('content_creator_homepg/', views.content_creator_homepg, name='content_creator_homepg'),
    path('movies/', views.movies_view, name='movies'),





    #path('kids_content/', views.kids_content_view, name='kids_content'),
    path('movies/<int:movies_id>/', views.movies_details, name='movies_details'),


    path('ott_admin/', admin, name='admin'),
    path('admin_home/', admin_home, name='admin_home'),
    path('user_list/creator/', user_list, name='user_list'),
    path('superadmin/add_users/', add_user, name='add_user'),
    path('toggle_status/<int:user_id>/', toggle_user_status, name='toggle_user_status'),
]



