from rest_framework import viewsets, permissions

from .models import Project
from navedex.projects import serializers


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return serializers.ProjectCreateSerializer
        if self.action == 'retrieve':
            return serializers.ProjectDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__exact=name)

        return queryset.filter(owner=self.request.user)
