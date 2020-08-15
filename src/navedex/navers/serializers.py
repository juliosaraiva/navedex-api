from rest_framework import serializers

from navedex.navers.models import Naver

from navedex.projects.models import Project
from navedex.projects.serializers import ProjectSerializer


class NaverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate',
                  'admission_date', 'job_role')
        read_only_fields = ('id',)


class NaverCreateSerializer(serializers.ModelSerializer):
    """Create a New Naver"""
    projects = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Project.objects.all(),
        required=False
    )

    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate',
                  'admission_date', 'job_role', 'projects')
        read_only_fields = ('id',)

    def create(self, validate_data):
        return Naver.objects.create(**validate_data)


class NaverDetailSerializer(serializers.ModelSerializer):
    """Show details about Naver"""
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate',
                  'admission_date', 'job_role', 'projects')
        read_only_fields = ('id',)
