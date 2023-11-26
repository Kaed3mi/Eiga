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
import app.views.bangumi_relationship as bangumi_relationship
import app.views.character as character
import app.views.bangumi_character as bangumi_character
import app.views.comment as comment
import app.views.score as score

urlpatterns = [
    path('vue/', vueViews.VueViews.as_view()),
    # user
    path('user_register/', user.UserRegister.as_view()),
    path('user_login/', user.UserLogin.as_view()),
    path('user_query/', user.UserInfoQuery.as_view()),
    path('upload_avatar/', user.upload_avatar, name='upload_avatar'),
    path('user_search/', user.UserSearch.as_view()),
    # bangumi
    path('bangumi_query/', bangumi.BangumiQuery.as_view()),
    path('bangumi_character_query/', bangumi_character.BangumiCharacterQuery.as_view()),
    path('bangumi_search/', bangumi.BangumiSearch.as_view()),
    path('bangumi_relationship_query/', bangumi_relationship.BangumiRelationshipQuery.as_view()),
    path('bangumi_score_query/', score.BangumiScoreQuery.as_view()),
    # comment
    path('comment_query/', comment.CommentQuery.as_view()),
    path('comment_search/', comment.CommentSearch.as_view()),
    path('comment_insert/', comment.CommentInsert.as_view()),
    # score
    path('score_insert/', score.ScoreInsert.as_view()),
    path('score_update/', score.ScoreUpdate.as_view()),
    path('score_query/', score.ScoreQuery.as_view()),
    path('get_user_scores/', score.GetUserScores.as_view()),
    # character
    path('character_search/', character.CharacterSearch.as_view()),
    path('character_query/', character.CharacterQuery.as_view()),
    path('character_update/', character.CharacterUpdate.as_view()),
]
# import app.views.user as user
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path("admin/