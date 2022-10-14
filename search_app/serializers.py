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
    
class SearchSerializer(serializers.ModelSerializer):
    bbox_id = serializers.IntegerField()
    image = serializers.ImageField(use_url=True)
    frame_num = serializers.IntegerField()
    obj_id = serializers.IntegerField()
    
    def get_image(self, search_result):
        request = self.context.get('request')
        image = search_result.image.url
        return request.build_absolute_uri(image)

class SearchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = bbox_attributes.objects.select_related('bbox','bbox__video', 'attributes')
        fields = ["bbox_id", "bbox.image", "bbox__video__fps", "bbox__obj_id"]
        