from django.urls import path
from .views import VideodataViewSet, BboxdataViewSet, BboxAttributeViewSet, LabelAttributeViewSet, LabelTypeViewSet, call_serializer, search, search_serializerViewSet

# Blog 목록 보여주기
video_list = VideodataViewSet.as_view({
    'get': 'list',
    #'post' : 'create'
})

bbox_data_list = BboxdataViewSet.as_view({
    'get' : 'list',
    #'post' : 'create'
})

bbox_attr_list = BboxAttributeViewSet.as_view({
    'get' : 'list',
    #'post' : 'create'
})

label_attr_list = LabelAttributeViewSet.as_view({
    'get' : 'list'
})

label_type_list = LabelTypeViewSet.as_view({
    'get' : 'list'
})

searched_list = search_serializerViewSet.as_view({
    'get' : 'list'
})

urlpatterns = [
    path("video/", video_list),
    path("bbox/", bbox_data_list),
    path("bbox_attr/", bbox_attr_list),
    path("label_attr/", label_attr_list),
    path("label_type/", label_type_list),
    path("search/", searched_list),
    path("serialize/", call_serializer),
    # path("", search, name = search)
]