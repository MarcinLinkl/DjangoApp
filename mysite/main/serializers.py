from rest_framework  import serializers

from .models import GPW


class Akcje_GPWSerializer(serializers.ModelSerializer):
    x = serializers.DateField(source="date")
    o = serializers.DecimalField(max_digits=20, decimal_places=4,source="open")
    h = serializers.DecimalField(max_digits=20, decimal_places=4,source="high")
    l = serializers.DecimalField(max_digits=20, decimal_places=4,source="low")
    c = serializers.DecimalField(max_digits=20, decimal_places=4,source="close")

    class Meta:
        model = GPW
        fields = ("x","o","h","l","c")