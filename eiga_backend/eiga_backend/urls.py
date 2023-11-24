"""
URL configuration for eiga_backend project.

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
from django.conf.urls.static import static
from django.urls import path
import app.views.vueViews as vueViews
import app.views.user as user
from eiga_backend import settings
import app.views.bangumi as bangumi
import app.views.character as character
import app.views.bangumi_character as bangumi_character
import app.views.character as character

urlpatterns = [
    path('vue/', vueViews.VueViews.as_view()),
    path('user_register/', user.UserRegister.as_view()),
    path('user_login/', user.UserLogin.as_view()),
    path('user_query/', user.UserInfoQuery.as_view()),
    path('upload_avatar/', user.upload_avatar, name='upload_avatar'),
    path('bangumi_query/', bangumi.BangumiQuery.as_view()),
    path('bangumi_character_query/', bangumi_character.BangumiCharacterQuery.as_view()),
    path('character_query/', character.CharacterQuery.as_view())
    path('bangumi_search/', bangumi.BangumiSearch.as_view()),
    path('character_search/', character.CharacterSearch.as_view()),
    path('user_search/', user.UserSearch.as_view()),
]
# import app.views.user as user
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("user_register/", user.UserRegister.as_view())
# ]
