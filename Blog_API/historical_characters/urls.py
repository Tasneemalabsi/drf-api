from django.urls import path
from .views import CharacterList, CharacterDetail

urlpatterns = [
    path('', CharacterList.as_view(), name='characters_list'),
    path('<int:pk>/', CharacterDetail.as_view(), name='characters_detail'),
    ]