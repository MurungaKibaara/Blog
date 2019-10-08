from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

SECRET_KEY= 'secret'

from .models import Article, Author
from .serializers import ArticleSerializer, AuthorSerializer

class ArticleView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        permission_classes = (IsAuthenticated)
        author = get_object_or_404(Author, id=self.request.data.get('author_id'))
        return serializer.save(author=author)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        permission_classes = (IsAuthenticated)
        return self.create(request, *args, **kwargs)

class SingleArticleView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class AuthorView(APIView):

    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response({'Error': "Please provide email/password"}, status="400")
        
        try:
            email = request.data['email']
            password = request.data['password']
        except KeyError:
            return Response({'Error': "Keys Missing"}, status="400")


        try:
            author = Author.objects.get(email=email, password=password)
        except Author.DoesNotExist:
            return Response({'Error': "Invalid username/password"}, status="400")

        if author: 
            payload = {
                'id': author.id,
                'email': author.email,
            }

            jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}

            return HttpResponse(json.dumps(jwt_token), status=200, content_type="application/json")

        else:
            return Response(json.dumps({'Error': "Invalid credentials"}),status=400,content_type="application/json")
