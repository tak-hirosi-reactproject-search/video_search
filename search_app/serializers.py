from rest_framework import serializers
from .models import uploaded_data, video_data, bbox_data, bbox_attributes, labels_attributes, labels_attributes_type, labels_mainclass_type

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = video_data
        fields = '__all__'

class BboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = bbox_data
        fields = '__all__'

class BboxAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = bbox_attributes
        fields = '__all__'

class LabelsAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = labels_attributes
        fields = '__all__'

class LabelsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = labels_attributes_type
        fields = '__all__'

class LabelsMainClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = labels_mainclass_type
        fields = '__all__'
    
class SearchSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.ImageField(use_url=True)
    frame_num = serializers.IntegerField()
    obj_id = serializers.IntegerField()
    
class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        file = uploaded_data