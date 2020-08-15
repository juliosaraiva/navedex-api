from rest_framework import serializers

from .models import Project

from navedex.navers.models import Naver
from navedex.navers.serializers import NaverSerializer


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ProjectPostSerializer(serializers.ModelSerializer):
    navers = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Naver.objects.all()
    )

    class Meta:
        model = Project
        fields = ('id', 'name', 'navers')
        read_only_fields = ('id',)


class ProjectDetailSerializer(serializers.ModelSerializer):
    navers = NaverSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'navers')
        read_only_fields = ('id',)
