from rest_framework import permissions
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from .models import Naver
from .serializers import (
    NaverSerializer,
    NaverDetailSerializer
)


class NaverAPIView(ListCreateAPIView):
    serializer_class = NaverSerializer
    queryset = Naver.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class NaverDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = NaverDetailSerializer
    permission_class = (permissions.IsAuthenticated,)
    queryset = Naver.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
