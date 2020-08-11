from rest_framework import serializers

from navedex.navers.models import Naver
from navedex.projects.models import Project


class NaverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate',
                  'admission_date', 'job_role')
        read_only_fields = ('id',)


class NaverDetailSerializer(serializers.ModelSerializer):
    """Naver Detail Serializer"""
    projects = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Project.objects.all()
    )

    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate',
                  'admission_date', 'job_role', 'projects')
        read_only_fields = ('id',)
