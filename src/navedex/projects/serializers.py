from rest_framework import serializers

from .models import Project

from navedex.navers.models import Naver


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ProjectDetailSerializer(serializers.ModelSerializer):
    navers = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Naver.objects.all()
    )

    class Meta:
        model = Project
        fields = ('id', 'name', 'navers')
        read_only_fields = ('id',)
