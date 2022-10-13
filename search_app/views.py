from django.http import HttpResponse
from django.db import connection
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import LabelsAttributeSerializer,LabelsTypeSerializer, VideoSerializer, BboxSerializer, BboxAttributeSerializer, SearchSerializer
import urllib.parse as uparse
from search_app.models import video_data, bbox_data, bbox_attributes, labels_attributes, labels_attributes_type, labels_mainclass_type
import pandas as pd
import os

from django.conf import settings
from django.conf.urls.static import static

def set_bbox(filepath, video_id):
    # print(video_id)
    df = pd.read_csv(filepath)
    data_df = df.values.tolist()

    label_mainclass_id = list(labels_mainclass_type.objects.values('id'))[0]["id"]
    label_mainclass_obj = labels_mainclass_type.objects.get(id = label_mainclass_id)

    for i in range(len(data_df)):    

        label_list = []
        for j in range(len(data_df[0])):
            if j in range(3, 7):
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

                if j == 3:
                    type_str = 'top_type'
                elif j == 4:
                    type_str = 'bottom_type'
                elif j == 5:
                    type_str = 'top_color'
                elif j == 6:
                    type_str = 'bottom_color'
                
                if type_index in range(0, 11):
                    label_attribute_type_id = list(labels_attributes_type.objects.filter(mainclass = label_mainclass_obj, type = type_str).values('id'))[0]["id"]
                    label_attribute_type_obj = labels_attributes_type.objects.get(id = label_attribute_type_id)
                    label_attribute_id = list(labels_attributes.objects.filter(type = label_attribute_type_obj, index = type_index).values('id'))[0]["id"]
                    label_attribute_obj = labels_attributes.objects.get(id = label_attribute_id)
                    label_list.append(label_attribute_obj)

        filename = data_df[i][2].split("/")
        video_name_jpg = filename[1].split("_")
        video_name = video_name_jpg[2].split(".") 
        bbox = bbox_data(video = video_id, 
                         frame_num = video_name_jpg[0], 
                         obj_id = video_name[0], 
                         image = f'images/{data_df[i][2]}', 
                         mainclass = label_mainclass_obj)
        bbox.save()
        bbox_instance_id = list(bbox_data.objects.filter(video = video_id, frame_num = video_name_jpg[0], obj_id = video_name[0]).values('id'))[0]["id"]
        bbox_instance_obj = bbox_data.objects.get(id = bbox_instance_id)

        for k in range(len(label_list)):
            bbox_attribute_instance = bbox_attributes(bbox = bbox_instance_obj, attributes = label_list[k])
            bbox_attribute_instance.save()
            

def set_video_data(filepath):
    src_path = '/videometadata/csvfiles'

    df = pd.read_csv(filepath)
    data_df = df.values.tolist()
    filename = data_df[0][2].split('/')
    video_instance = video_data(src_path = src_path, name = filename[0], fps = data_df[0][0], last_frame = data_df[0][1])
    video_instance.save()            
    video_id = list(video_data.objects.all().values('id'))[0]["id"]
    video_obj = video_data.objects.get(id = video_id)

    return video_obj

def call_serializer(filepath):
    video_id = set_video_data(filepath)
    set_bbox(filepath, video_id)

def match_filename(self):
    filecount = video_data.objects.values("name").count()
    filelist = []
    for j in range(filecount):
        filelist.append(list(video_data.objects.all().values('name'))[j]["name"])
        
    dir_file = []
    dir_path = '/videometadata/csvfiles' 
    count = 0
    for (root, directories, files) in os.walk(dir_path):
        for file in files:  
           file_name, extension = os.path.splitext(file)
           if extension == ".csv":
               dir_file.append(file_name) 
               count += 1                  

    if count != filecount:
        for i in range(len(dir_file)):
            if dir_file[i] not in filelist:
                call_serializer(dir_path + '/' + dir_file[i] + extension)
        return HttpResponse('<h1> Serialized </h1>')
    else:
        return HttpResponse('<h1> serialize할 파일이름 없음 </h1>')

def search(video_id_list, top_type_list, top_color_list, bottom_type_list, bottom_color_list, con):
        
    condition = con[0]
    string_query_toptype = []
    string_query_topcolor = []
    string_query_bottomtype = []
    string_query_bottomcolor = []
    
    for i in range(len(video_id_list)):
        for j in range(len(top_type_list)):
            string_query_toptype.append("select bbox_id, image, frame_num, obj_id from search_app_video_data inner join search_app_bbox_data on search_app_video_data.id = search_app_bbox_data.video_id inner join search_app_bbox_attributes on search_app_bbox_data.id = search_app_bbox_attributes.bbox_id inner join search_app_labels_attributes on search_app_bbox_attributes.attributes_id = search_app_labels_attributes.id " 
            +" where search_app_labels_attributes.name=" 
            + "'" + top_type_list[j] + "'"
            +" and search_app_video_data.id=" 
            +str(video_id_list[i])
            )
        
        for k in range(len(top_color_list)):
            string_query_topcolor.append("select bbox_id, image, frame_num, obj_id from search_app_video_data inner join search_app_bbox_data on search_app_video_data.id = search_app_bbox_data.video_id inner join search_app_bbox_attributes on search_app_bbox_data.id = search_app_bbox_attributes.bbox_id inner join search_app_labels_attributes on search_app_bbox_attributes.attributes_id = search_app_labels_attributes.id " 
            +"where search_app_labels_attributes.name=" 
            + "'" + top_color_list[k] + "'"
            +" and search_app_labels_attributes.type_id=" 
            +"2" 
            +" and search_app_video_data.id=" 
            +str(video_id_list[i])
            )
        
        for l in range(len(bottom_type_list)):
            string_query_bottomtype.append("select bbox_id, image, frame_num, obj_id from search_app_video_data inner join search_app_bbox_data on search_app_video_data.id = search_app_bbox_data.video_id inner join search_app_bbox_attributes on search_app_bbox_data.id = search_app_bbox_attributes.bbox_id inner join search_app_labels_attributes on search_app_bbox_attributes.attributes_id = search_app_labels_attributes.id " 
            +"where search_app_labels_attributes.name=" 
            + "'" + bottom_type_list[l] + "'"
            +" and search_app_video_data.id=" 
            +str(video_id_list[i])
            )
        
        for m in range(len(bottom_color_list)):
            string_query_bottomcolor.append("select bbox_id, image, frame_num, obj_id from search_app_video_data inner join search_app_bbox_data on search_app_video_data.id = search_app_bbox_data.video_id inner join search_app_bbox_attributes on search_app_bbox_data.id = search_app_bbox_attributes.bbox_id inner join search_app_labels_attributes on search_app_bbox_attributes.attributes_id = search_app_labels_attributes.id " 
            +"where search_app_labels_attributes.name=" 
            + "'" + bottom_color_list[m] + "'"
            +" and search_app_labels_attributes.type_id=" 
            +"4" 
            +" and search_app_video_data.id=" 
            +str(video_id_list[i])
            )
            
    raw_query = ""
    q1 = 'select * from(' + ' union '.join(string_query_toptype) + ')'
    raw_query += q1
    q2 = 'select * from(' + ' union '.join(string_query_topcolor) + ')'
    raw_query += ' intersect ' + q2
    if len(string_query_bottomtype) != 0:
        q3 = 'select * from(' + ' union '.join(string_query_bottomtype) + ')'
        raw_query +=' ' + condition + ' ' + q3 
    if len(string_query_bottomcolor) != 0:
        q4 = 'select * from(' + ' union '.join(string_query_bottomcolor) + ')'
        raw_query += ' intersect ' + q4    
    raw_query += ";"

    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        row = cursor.fetchall()

    result_set = []
    for i in range(len(row)):
        temp_dict = {}
        temp_dict["bbox_id"] = row[i][0]
        temp_dict["image"] = f'{static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)}{row[i][1]}'
        temp_dict["frame_num"] = row[i][2]
        temp_dict["obj_id"] = row[i][3]
        result_set.append(temp_dict)
        
    return result_set

def get_data(data):
    video_id_list = []
    top_type_list = []
    top_color_list = []
    bottom_type_list = []
    bottom_color_list = []
    condition = []

    for i in range(len(data)):
        if data[i][0] == 'video_id':
            video_id_list.append(data[i][1])
        elif data[i][0] == "top_type":
            top_type_list.append(data[i][1])
        elif data[i][0] == "top_color":
            top_color_list.append(data[i][1])
        elif data[i][0] == "bottom_type":
            bottom_type_list.append(data[i][1])
        elif data[i][0] == "bottom_color":
            bottom_color_list.append(data[i][1])
        elif data[i][0] == "condition":
            condition.append(data[i][1])
    
    result_set = search(video_id_list, top_type_list, top_color_list, bottom_type_list, bottom_color_list, condition)
    search_serializer = SearchSerializer(result_set, many = True)

    return search_serializer.data
   

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

class SearchViewSet(viewsets.ModelViewSet):
    queryset = bbox_data.objects.all()

    def list(self, request, url):
        data = uparse.parse_qsl(url, keep_blank_values=True)
        queryset = get_data(data)
        return Response(queryset)


