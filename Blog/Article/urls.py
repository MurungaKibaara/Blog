from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import ArticleView, SingleArticleView, AuthorView

app_name = "articles"

urlpatterns = [
    path('articles', ArticleView.as_view()),
    path('articles/<int:pk>', ArticleView.as_view()),
    path('articles/<int:pk>', SingleArticleView.as_view()),

    path('login', AuthorView.as_view()),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]