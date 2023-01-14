from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Character
from .serializer import CharacterSerializer

class CharacterList(ListCreateAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

class CharacterDetail(RetrieveUpdateDestroyAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer