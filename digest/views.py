from .models import Post, Digest 
from .serializers import DigestSerializer
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response

class CreateDigestView(APIView):
    """
    Фильтрует записи для пользователя, создает новый дайджест и отдает его в json.
    Обрабатывает GET-запрос на URL вида api/digest/?userid=2&rating=8, где:
    userid - уникальный айди пользователя
    rating - значение рейтинга для фильтра записей, которые имеют значение рейтинга выше, чем указанный
    """
    def get_user(self, id): # Функция для проверки и получения объекта пользователя по его id
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        userid = self.request.query_params.get('userid') # Получаем значение id из параметров URL-запроса
        if self.request.query_params.get('rating'): # Получаем значение rating из параметров URL-запроса, если его не было в запросе, то считаем, что рейтинг равен нулю
            rating = self.request.query_params.get('rating')
        else:
            rating = 0
        user = self.get_user(userid)
        posts = Post.objects.filter(subscription__user=userid).filter(rating__gt=rating) # Кверисет постов с фильтрами - из подписок этого пользователя и рейтинг постов вышем, чем указанный
        new_digest = Digest(user=user)
        new_digest.save() # Сохраняем созданный дайджест
        new_digest.posts.set(posts) # Добавляем в созданный дайджест все отфильтрованные посты
        serializer = DigestSerializer(new_digest) # Сериализуем созданный дайджест в формат json
        return Response(serializer.data)
