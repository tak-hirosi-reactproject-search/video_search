from django.urls import path
from .views import VideodataViewSet, BboxdataViewSet, BboxAttributeViewSet, LabelAttributeViewSet, LabelTypeViewSet, match_filename, SearchViewSet
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

searched_list = SearchViewSet.as_view({
    'get' : 'list'
})

urlpatterns = [
    path("video/", video_list),
    path("bbox/", bbox_data_list),
    path("bbox_attr/", bbox_attr_list),
    path("label_attr/", label_attr_list),
    path("label_type/", label_type_list),
    path("search/<str:url>/", searched_list),
    path("serialize/", match_filename),
]


from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)