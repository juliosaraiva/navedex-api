from rest_framework import permissions
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from .models import Naver
from navedex.navers import serializers


class NaverAPIView(ListCreateAPIView):
    serializer_class = serializers.NaverSerializer
    queryset = Naver.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

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


class NaverDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.NaverDetailSerializer
    permission_class = (permissions.IsAuthenticated,)
    queryset = Naver.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
