from .models import Post, Digest 
from .serializers import DigestSerializer
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CreateDigestView(APIView):
    """
    Фильтрует записи для пользователя, создает новый дайджест и отдает его в json.
    Обрабатывает GET-запрос на URL вида api/digest/?userid=2&rating=8, где:
    userid - уникальный айди пользователя
    rating - значение рейтинга для фильтра записей
    """
    serializer_class = DigestSerializer

    def get_user(self, id): # Функция для проверки и получения объекта пользователя по его id
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            raise Http404
    
    @swagger_auto_schema(manual_parameters=[
            openapi.Parameter('userid', openapi.IN_QUERY,
                      description='Уникальный айди пользователя',
                      type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('rating', openapi.IN_QUERY,
                      description='Значение рейтинга',
                      type=openapi.TYPE_INTEGER)])
    def get(self, request, format=None):
        userid = self.request.query_params.get('userid') # Получаем значение id из параметров URL-запроса
        if self.request.query_params.get('rating'): # Получаем значение rating из параметров URL-запроса, если его не было в запросе, то считаем, что рейтинг равен нулю
            rating = self.request.query_params.get('rating')
        else:
            rating = 0
        user = self.get_user(userid)
        
        # Кверисет постов с фильтрами - подписки этого пользователя и рейтинг постов выше или равно, чем указанный, исключая посты, если пользователь их уже видел 
        posts = Post.objects.exclude(viewed__id=userid).filter(subscription__user=userid).filter(rating__gte=rating) 
        
        new_digest = Digest(user=user)
        new_digest.save() # Сохраняем созданный дайджест
        new_digest.posts.set(posts) # Добавляем в созданный дайджест все отфильтрованные посты
        
        for post in posts:
            post.viewed.add(user) # Отмечаем выбранные для дайджеста посты как просмотренные этим пользователем

        serializer = DigestSerializer(new_digest) # Сериализуем созданный дайджест в формат json
        return Response(serializer.data)
