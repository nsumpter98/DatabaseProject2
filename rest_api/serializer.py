from missing_data.models import Person
from rest_framework import serializers

class PersonSerializer(serializers.ModelSerializer):
    # Explicitly declare the annotated fields
    default_product_rating = serializers.FloatField(read_only=True)
    default_age = serializers.IntegerField(read_only=True)
    default_education = serializers.CharField(read_only=True)
    default_occupation = serializers.CharField(read_only=True)
    default_marital_status = serializers.CharField(read_only=True)
    class Meta:
        model = Person
        fields = [
            'customer_id',
            'education',
            'gender',
            'occupation',
            'marital_status',
            'product_rating',
            'default_product_rating',
            'age',
            'default_age',
            'default_education',
            'default_occupation',
            'default_marital_status'
        ]