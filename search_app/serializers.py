from rest_framework import serializers
from .models import bbox_attributes, labels_attributes, labels_attributes_type, labels_mainclass_type, video_data
from .models import bbox_data

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
    bbox_id = serializers.IntegerField()
    image = serializers.ImageField()
    frame_num = serializers.IntegerField()
    obj_id = serializers.IntegerField()