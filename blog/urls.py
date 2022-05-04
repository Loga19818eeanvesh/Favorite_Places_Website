from django.urls import path

from . import views

urlpatterns = [
    path('', views.StartingPageView.as_view(), name='starting_page'),      # ourdomain/
    path('create/',views.CreatePostView.as_view(),name='create'),
    path('posts/', views.AllPostsView.as_view(), name='posts_page'),     # ourdomain/posts
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail_page'),      # ourdomain/posts/<slug>
    path("read-later/", views.ReadLaterView.as_view(), name="read-later"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("delete-post",views.DeletePostView.as_view(),name="delete-post"),
    path("user-posts/<int:id>",views.user_posts,name="user-posts"),
    path("all-users/",views.all_users,name="all-users")
]