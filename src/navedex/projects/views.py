from rest_framework import viewsets, permissions

from .models import Project
from .serializers import (
    ProjectSerializer,
    ProjectPostSerializer,
    ProjectDetailSerializer
)


class ProjectAPIView(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectPostSerializer
        if self.action == 'retrieve':
            return ProjectDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__exact=name)

        return queryset.filter(owner=self.request.user)
