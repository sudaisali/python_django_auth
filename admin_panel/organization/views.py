from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import *
from rest_framework.views import APIView

from rest_framework import status

# Create your views here.




# class Organization(GenericAPIView):
#     serializer_class = OrganizationSerializer
    
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()  # Saving without any additional arguments
        
#         return Response("Data saved", status=200)


class CreateOrganizationView(APIView):
    def post(self, request, format=None):
        serializer = CombinedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)