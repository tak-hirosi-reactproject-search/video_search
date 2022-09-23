from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import VideoSerializer, BboxSerializer, BboxAttributeSerializer, LabelsAttributeSerializer, LabelsTypeSerializer, LabelsMainClassSerializer

# Create your views here.
@api_view(["GET"])
def HelloAPI(request):
    return Response("hello world")

class VideoAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VideoSerializer

    def get_object(self):
        return self.request.user

class BboxAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VideoSerializer

    def get_object(self):
        return self.request.user