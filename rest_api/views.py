from missing_data.models import Person
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, FloatField, Value, IntegerField, Count, CharField
import statistics
from django.db.models.functions import Coalesce
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

class MedianSubstitute(APIView):
    def get(self, request):
        # Fetch product_rating and age values, excluding NULLs, and sort them
        product_ratings = list(
            Person.objects.exclude(product_rating__isnull=True).values_list('product_rating', flat=True).order_by(
                'product_rating'))
        ages = list(Person.objects.exclude(age__isnull=True).values_list('age', flat=True).order_by('age'))

        # Calculate median values
        median_product_rating = statistics.median(product_ratings) if product_ratings else None
        median_age = statistics.median(ages) if ages else None

        # Annotate queryset with default values for NULL product_rating and age
        persons = Person.objects.annotate(
            default_product_rating=Coalesce('product_rating', Value(median_product_rating), output_field=FloatField()),
            default_age=Coalesce('age', Value(median_age), output_field=IntegerField())
        )

        # Assuming you want to use this in a serializer or similar
        persons_values = persons.values(
            'customer_id', 'education', 'gender', 'occupation', 'marital_status', 'product_rating', 'age',
            'default_product_rating', 'default_age'
        )

        serializer = PersonSerializer(persons_values, many=True)
        return Response(serializer.data[0:10])

class ModeSubstitute(APIView):
    def calculate_mode(self, model, field_name):
        # Calculate the most frequent (mode) value for a given field
        return model.objects.values(field_name) \
            .exclude(**{f"{field_name}__isnull": True}) \
            .annotate(count=Count(field_name)) \
            .order_by('-count') \
            .first().get(field_name)
    def get(self, request):
        # Calculate modes for categorical fields
        mode_education = self.calculate_mode(Person, 'education')
        mode_occupation = self.calculate_mode(Person, 'occupation')
        mode_marital_status = self.calculate_mode(Person, 'marital_status')

        # Annotate queryset with mode values for NULL fields
        persons = Person.objects.annotate(
            default_education=Coalesce('education', Value(mode_education), output_field=CharField()),
            default_occupation=Coalesce('occupation', Value(mode_occupation), output_field=CharField()),
            default_marital_status=Coalesce('marital_status', Value(mode_marital_status), output_field=CharField())
        )

        # If you need to work with values directly (e.g., for a serializer), include the annotated fields
        persons_values = persons.values(
            'customer_id',
            'education',
            'gender',
            'occupation',
            'marital_status',
            'product_rating',
            'age',
            'default_education',
            'default_occupation',
            'default_marital_status'
        )

        serializer = PersonSerializer(persons_values, many=True)
        return Response(serializer.data[0:10])
