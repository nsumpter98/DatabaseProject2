from missing_data.models import Person
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, FloatField, Subquery, OuterRef, Value, F,  IntegerField
from django.db.models.expressions import Case, When
from django.db.models.functions import Coalesce
from rest_framework import permissions
from .serializer import PersonSerializer


class MissingDataApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        person = Person.objects.all()
        serializer = PersonSerializer(person, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Development(APIView):
    def post(self, request):
        # delete all records
        # if auth code is correct
        if request.data['auth_code'] == 'markcanada':
            Person.objects.all().delete()
            print("All records deleted")
            return Response(status=status.HTTP_204_NO_CONTENT)


class MeanSubstitute(APIView):
    def get(self, request):
        # Calculate average product_rating and age for non-NULL values
        average_product_rating = \
        Person.objects.exclude(product_rating__isnull=True).aggregate(avg_product_rating=Avg('product_rating'))[
            'avg_product_rating']
        average_age = Person.objects.exclude(age__isnull=True).aggregate(avg_age=Avg('age'))['avg_age']

        # Annotate queryset with default values for NULL product_rating and age, specifying output_field for Coalesce
        persons = Person.objects.annotate(
            default_product_rating=Coalesce('product_rating', Value(average_product_rating), output_field=FloatField()),
            default_age=Coalesce('age', Value(average_age), output_field=IntegerField())
        ).values(
            'customer_id', 'education','gender', 'occupation', 'marital_status','product_rating', 'age', 'default_product_rating', 'default_age'
        )



        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data[0:10])
