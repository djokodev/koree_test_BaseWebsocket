from rest_framework import serializers
from myapp.models import Data

class DataSerializers(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'