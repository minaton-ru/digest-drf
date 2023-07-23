from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="Digest API",
      default_version='v1',
      description="API для получения дайджеста новостей из источников с фильтром по популярности, работает на Django Rest Framework",
      terms_of_service="https://github.com/minaton-ru/digest-drf",
      contact=openapi.Contact(email="minaton@yandex.ru"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('digest/', views.CreateDigestView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), 
         name='schema-swagger-ui'),
]
