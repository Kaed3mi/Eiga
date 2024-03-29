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
import app.views.blog as blog
import app.views.blog_bangumi as blog_bangumi

urlpatterns = [
    path('vue/', vueViews.VueViews.as_view()),
    # user
    path('user_register/', user.UserRegister.as_view()),
    path('user_login/', user.UserLogin.as_view()),
    path('user_query/', user.UserInfoQuery.as_view()),
    path('upload_avatar/', user.upload_avatar, name='upload_avatar'),
    path('user_search/', user.UserSearch.as_view()),
    path('user_info_update/', user.UserUpdateInfo.as_view()),
    # bangumi
    path('bangumi_query/', bangumi.BangumiQuery.as_view()),
    path('bangumi_delete/', bangumi.BangumiDelete.as_view()),
    path('bangumi_character_query/', bangumi_character.BangumiCharacterQuery.as_view()),
    path('bangumi_search/', bangumi.BangumiSearch.as_view()),
    path('bangumi_relationship_query/', bangumi_relationship.BangumiRelationshipQuery.as_view()),
    path('bangumi_score_query/', score.BangumiScoreQuery.as_view()),
    path('bangumi_select/', bangumi.BangumiSelect.as_view()),
    path('bangumi_update/', bangumi.BangumiUpdate.as_view()),
    path('bangumi_charater_update/', bangumi_character.BangumiCharaterUpdate.as_view()),
    path('bangumi_bangumi_update/', bangumi_relationship.BangumiBangumiUpdate.as_view()),
    path('bangumi_insert/', bangumi.BangumiInsert.as_view()),
    path('character_bangumi_query/', bangumi_character.CharacterBangumiQuery.as_view()),
    # comment
    path('comment_query/', comment.CommentQuery.as_view()),
    path('comment_search/', comment.CommentSearch.as_view()),
    path('comment_insert/', comment.CommentInsert.as_view()),
    path('comment_delete/', comment.CommentDelete.as_view()),
    # score
    path('score_insert/', score.ScoreInsert.as_view()),
    path('score_update/', score.ScoreUpdate.as_view()),
    path('score_query/', score.ScoreQuery.as_view()),
    path('get_user_scores/', score.GetUserScores.as_view()),
    path('bangumi_rank_query/', score.BangumiRankQuery.as_view()),
    path('my_bangumi_query/', score.MyBangumiQuery.as_view()),
    # character
    path('character_search/', character.CharacterSearch.as_view()),
    path('character_query/', character.CharacterQuery.as_view()),
    path('character_delete/', character.CharacterDelete.as_view()),
    path('character_update/', character.CharacterUpdate.as_view()),
    path('character_select/', character.CharacterSelect.as_view()),
    path('character_create/', character.CharacterCreate.as_view()),
    # blog
    path('blog_insert/', blog.BlogInsert.as_view()),
    path('blog_delete/', blog.BlogDelete.as_view()),
    path('blog_search/', blog.BlogSearch.as_view()),
    path('blog_update/', blog.BlogUpdate.as_view()),
    path('blog_query/', blog.BlogQuery.as_view()),
    path('user_blog_query/', blog.UserBlogQuery.as_view()),
    path('blog_bangumi_query/', blog_bangumi.BlogBangumiQuery.as_view()),
    path('bangumi_blog_query/', blog_bangumi.BangumiBlogQuery.as_view()),
    path('blog_bangumi_update/', blog_bangumi.BlogBangumiUpdate.as_view())
]
# import app.views.user as user
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path("admin/
