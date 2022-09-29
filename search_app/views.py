from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import LabelsAttributeSerializer,LabelsTypeSerializer, VideoSerializer, BboxSerializer, BboxAttributeSerializer
import os
import json
from search_app.models import video_data, bbox_data, bbox_attributes, labels_attributes, labels_attributes_type, labels_mainclass_type
import pandas as pd

def set_bbox(filepath, video_id):
    df = pd.read_csv(filepath)
    data_df = df.values.tolist()

    label_mainclass_id = list(labels_mainclass_type.objects.values('id'))[0]["id"]
    label_mainclass_obj = labels_mainclass_type.objects.get(id = label_mainclass_id)

    for i in range(len(data_df)):    
        filename = data_df[i][0].split('/')
        video_name_jpg = filename[1].split("_")
        video_name = video_name_jpg[2].split(".")
        bbox = bbox_data(video = video_id, frame_num = video_name_jpg[0], obj_id = video_name[0], crop_img_path = filename[1], mainclass = label_mainclass_obj)
        bbox.save()
        bbox_instance_id = list(bbox_data.objects.filter(video = video_id, frame_num = video_name_jpg[0], obj_id = video_name[0]).values('id'))[0]["id"]
        bbox_instance_obj = bbox_data.objects.get(id = bbox_instance_id)
        label_list = []

        for j in range(len(data_df[0])):
            if j in range(1, 5):
                type_index = -1
                type_str = ''

                if data_df[i][j] == "long_sleeve" or data_df[i][j] == "long_pants":
                    type_index = 0
                elif data_df[i][j] == "short_sleeve" or data_df[i][j] == "short_pants":
                    type_index = 1
                elif data_df[i][j] == "sleveless" or data_df[i][j] == "skirts":
                    type_index = 2
                elif data_df[i][j] == "onepiece":
                    type_index = 3
                elif data_df[i][j] == "red":
                    type_index = 0
                elif data_df[i][j] == "orange":
                    type_index = 1
                elif data_df[i][j] == "yellow":
                    type_index = 2
                elif data_df[i][j] == "green":
                    type_index = 3
                elif data_df[i][j] == "blue":
                    type_index = 4
                elif data_df[i][j] == "purple":
                    type_index = 5
                elif data_df[i][j] == "pink":
                    type_index = 6
                elif data_df[i][j] == "brown":
                    type_index = 7
                elif data_df[i][j] == "white":
                    type_index = 8
                elif data_df[i][j] == "grey":
                    type_index = 9
                elif data_df[i][j] == "black":
                    type_index = 10

                if j == 1:
                    type_str = 'top_type'
                elif j == 2:
                    type_str = 'top_color'
                elif j == 3:
                    type_str = 'bottom_type'
                elif j == 4:
                    type_str = 'bottom_color'
                
                if type_index in range(0, 11):
                    label_attribute_type_id = list(labels_attributes_type.objects.filter(mainclass = label_mainclass_obj, type = type_str).values('id'))[0]["id"]
                    label_attribute_type_obj = labels_attributes_type.objects.get(id = label_attribute_type_id)
                    label_attribute_id = list(labels_attributes.objects.filter(type = label_attribute_type_obj, index = type_index).values('id'))[0]["id"]
                    label_attribute_obj = labels_attributes.objects.get(id = label_attribute_id)
                    label_list.append(label_attribute_obj)

        for k in range(len(label_list)):
            bbox_attribute_instance = bbox_attributes(bbox = bbox_instance_obj, attributes = label_list[k])
            bbox_attribute_instance.save()

def set_video_data(filepath):
    name = os.path.splitext('/')
    src_path = '/workspace/test_jhlee/search_module'

    df = pd.read_csv(filepath)
    data_df = df.values.tolist()
    filename = data_df[0][0].split('/')
    video_instance = video_data(src_path = src_path, name = filename[0], fps = data_df[0][5], last_frame = data_df[0][6])
    video_instance.save()            
    video_id = list(video_data.objects.all().values('id'))[0]["id"]
    video_obj = video_data.objects.get(id = video_id)

    return video_obj

def call_serializer(filepath):
    filepath = '/workspace/test_jhlee/search_module/test.csv'
    video_id = set_video_data(filepath)
    set_bbox(filepath, video_id)

    return HttpResponse('<h1> Serialized </h1>')

def search(request):
    attr = '/workspace/test_jhlee/search_module/test.json'
    condition = "intersect"
    
    with open(attr, 'r') as file:
        data = json.load(file)
        
    video_id_list = data["video_id"]
    top_type_list = data["top_type"]
    top_color_list = data["top_color"]
    bottom_type_list = data["bottom_type"]
    bottom_color_list = data["bottom_color"]
    
    string_query_toptype = []
    string_query_topcolor = []
    string_query_bottomtype = []
    string_query_bottomcolor = []

    for i in range(len(video_id_list)):
        for j in range(len(top_type_list)):
            string_query_toptype.append("select bbox_id, crop_img_path, frame_num, obj_id from search_app_video_data inner join search_app_bbox_data on search_app_video_data.id = search_app_bbox_data.video_id inner join search_app_bbox_attributes on search_app_bbox_data.id = search_app_bbox_attributes.bbox_id inner join search_app_labels_attributes on search_app_bbox_attributes.attributes_id = search_app_labels_attributes.id " 
            +" where search_app_labels_attributes.value=" 
            + "'" + top_type_list[j] + "'"
            +" and search_app_video_data.id=" 
            +str(video_id_list[i])
            )
        
        for k in range(len(top_color_list)):
            string_query_topcolor.append("select bbox_id, crop_img_path, frame_num, obj_id from search_app_video_data inner join search_app_bbox_data on search_app_video_data.id = search_app_bbox_data.video_id inner join search_app_bbox_attributes on search_app_bbox_data.id = search_app_bbox_attributes.bbox_id inner join search_app_labels_attributes on search_app_bbox_attributes.attributes_id = search_app_labels_attributes.id " 
            +"where search_app_labels_attributes.value=" 
            + "'" + top_color_list[k] + "'"
            +" and search_app_labels_attributes.type_id=" 
            +"2" 
            +" and search_app_video_data.id=" 
            +str(video_id_list[i])
            )
        
        for l in range(len(bottom_type_list)):
            string_query_bottomtype.append("select bbox_id, crop_img_path, frame_num, obj_id from search_app_video_data inner join search_app_bbox_data on search_app_video_data.id = search_app_bbox_data.video_id inner join search_app_bbox_attributes on search_app_bbox_data.id = search_app_bbox_attributes.bbox_id inner join search_app_labels_attributes on search_app_bbox_attributes.attributes_id = search_app_labels_attributes.id " 
            +"where search_app_labels_attributes.value=" 
            + "'" + bottom_type_list[l] + "'"
            +" and search_app_video_data.id=" 
            +str(video_id_list[i])
            )
        
        for m in range(len(bottom_color_list)):
            string_query_bottomcolor.append("select bbox_id, crop_img_path, frame_num, obj_id from search_app_video_data inner join search_app_bbox_data on search_app_video_data.id = search_app_bbox_data.video_id inner join search_app_bbox_attributes on search_app_bbox_data.id = search_app_bbox_attributes.bbox_id inner join search_app_labels_attributes on search_app_bbox_attributes.attributes_id = search_app_labels_attributes.id " 
            +"where search_app_labels_attributes.value=" 
            + "'" + bottom_color_list[m] + "'"
            +" and search_app_labels_attributes.type_id=" 
            +"4" 
            +" and search_app_video_data.id=" 
            +str(video_id_list[i])
            )
    
    q1 = ' union '.join(string_query_toptype)
    q2 = ' union '.join(string_query_topcolor)
    q3 = ' union '.join(string_query_bottomtype)
    q4 = ' union '.join(string_query_bottomcolor)
    
    raw_query = q1 + ' intersect ' + q2  + ' ' + condition + ' ' + q3 + ' intersect ' + q4 + ";"
      
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        row = cursor.fetchall()
    
    print(row)
    
    
    return HttpResponse('<h1> searching </h1>')


# Blog의 목록, detail 보여주기, 수정하기, 삭제하기 모두 가능
class VideodataViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = video_data.objects.all()
    serializer_class = VideoSerializer

class BboxdataViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = bbox_data.objects.all()
    serializer_class = BboxSerializer

class BboxAttributeViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = bbox_attributes.objects.all()
    serializer_class = BboxAttributeSerializer

class LabelAttributeViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = labels_attributes.objects.all()
    serializer_class = LabelsAttributeSerializer

class LabelTypeViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = labels_attributes_type.objects.all()
    serializer_class = LabelsTypeSerializer
