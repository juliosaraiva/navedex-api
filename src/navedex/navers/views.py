from rest_framework import viewsets, permissions

from .models import Naver
from navedex.navers import serializers
from navedex.navers import permissions as perm


class NaverViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NaverSerializer
    queryset = Naver.objects.all()

    permission_classes = (permissions.IsAuthenticated, perm.IsOwner)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.NaverCreateSerializer
        if self.action == 'retrieve':
            return serializers.NaverDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        name = self.request.query_params.get("name")
        admission_date = self.request.query_params.get("admission_date")
        job_role = self.request.query_params.get("job_role")
        queryset = self.queryset
        if name:
            queryset = queryset.filter(name__exact=name)

        if admission_date:
            queryset = queryset.filter(admission_date__exact=admission_date)

        if job_role:
            queryset = queryset.filter(job_role__exact=job_role)

        return queryset.filter(owner=self.request.user)
