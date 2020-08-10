from rest_framework import generics, permissions

from .models import Naver
from .serializers import NaverSerializer
# from .permissions import IsOwner


class NaverAPIView(generics.ListCreateAPIView):
    serializer_class = NaverSerializer
    queryset = Naver.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
