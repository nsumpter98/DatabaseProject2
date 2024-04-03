from missing_data.models import Person
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializer import PersonSerializer

class MissingDataApiView(APIView):
    #permission_classes = [permissions.IsAuthenticated]

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