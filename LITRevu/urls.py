"""
URL configuration for LITRevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import authentification.views
import blog.views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentification.views.login_page, name='login-page'),
    path('logout/', authentification.views.logout_user, name='logout-user'),
    path('blog/home/', blog.views.home, name="home"),
    path('signup/', authentification.views.sign_up, name="sign-up"),
    path('ask_ticket/', blog.views.ticket_view, name="ask-for-ticket"),
    path('create_review/', blog.views.review_view, name="create-review"),
    path('home/<int:id>/create_review_response', blog.views.review_response_view, name="create-review-response"),
    path('posts/', blog.views.posts_view, name="posts-view"),
    path('blog/ticket/<int:id>/update/', blog.views.ticket_update, name="ticket-update"),
    path('blog/ticket/<int:id>/delete/', blog.views.ticket_delete, name='ticket-delete'),
    path('blog/review/<int:id>/update/', blog.views.review_update, name="review-update"),
    path('blog/review/<int:id>/delete/', blog.views.review_delete, name='review-delete'),
    path('blog/abonnements/', blog.views.abonnements_view, name="abonnements-view"),
    path('blog/abonnements/<int:id>/desabonner/', blog.views.desabonnements_view, name="desabonnements-view"),


]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
