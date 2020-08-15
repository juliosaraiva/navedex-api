from rest_framework import serializers

from .models import Project

from navedex.navers.models import Naver


class NaverDetail(serializers.ModelSerializer):
    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate',
                  'admission_date', 'job_role')
        read_only_fields = ('id',)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ProjectCreateSerializer(serializers.ModelSerializer):
    navers = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Naver.objects.all(),
        required=False
    )

    class Meta:
        model = Project
        fields = ('id', 'name', 'navers')
        read_only_fields = ('id',)

    def create(self, validate_data):
        return Project.objects.create(**validate_data)


class ProjectDetailSerializer(serializers.ModelSerializer):

    navers = NaverDetail(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'navers')
        read_only_fields = ('id',)

    def to_representation(self, instance):
        return super().to_representation(instance)
