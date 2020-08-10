from rest_framework import serializers

from navedex.navers.models import Naver


class NaverSerializer(serializers.ModelSerializer):
    """Serializer for Navers Objects"""

    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate',
                  'admission_date', 'job_role')
