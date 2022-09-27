from django.db import models

from django.db.models import CASCADE, Model

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class video_data(Model):
    #id = models.BigAutoField(help_text="Video ID", verbose_name="VIDEO ID", primary_key=True)
    src_path = models.FilePathField(max_length=200, path=BASE_DIR, verbose_name="SOURCE PATH", null=True)
    name = models.CharField(max_length=100, verbose_name="NAME")
    
    fps = models.FloatField(verbose_name="FPS", null=True)
    last_frame = models.FloatField(verbose_name="Last Frame", null=True)
    # crop_imgs_dir_path = models.FilePathField(max_length=100)

class labels_mainclass_type(Model):
    # id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name="Mainclass")

class labels_attributes_type(Model):
    # id = models.BigAutoField(unique=True, verbose_name="ID")
    mainclass = models.ForeignKey(to="labels_mainclass_type", on_delete=CASCADE, verbose_name="Mainclass")
    type = models.CharField(max_length=20, verbose_name="Type")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["mainclass", "type"],
                name = "unique frame"
            )
        ]

class labels_attributes(Model):
    # id = models.BigAutoField(verbose_name="Attribute ID", unique=True)
    type = models.ForeignKey(to="labels_attributes_type", on_delete=CASCADE, verbose_name="Type")
    index = models.PositiveSmallIntegerField()
    value = models.CharField(max_length=30, verbose_name="Attributes")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["type", "index"],
                name = "unique attribute"
            )
        ]
 
class bbox_data(Model):
    # id = models.BigAutoField(unique=True, verbose_name="ID")
    video = models.ForeignKey(to="video_data", on_delete=CASCADE, verbose_name="Type")
    frame_num = models.PositiveBigIntegerField(verbose_name="Frame")
    obj_id = models.PositiveSmallIntegerField(verbose_name="Object ID")
    crop_img_path = models.FilePathField(path=BASE_DIR, max_length=200)
    mainclass = models.ForeignKey(to="labels_mainclass_type", on_delete=CASCADE, verbose_name="Mainclass")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["video", "frame_num", "obj_id"],
                name = "unique object"
            )
        ]    

class bbox_attributes(Model):
    bbox = models.ForeignKey(to="bbox_data", on_delete=CASCADE, verbose_name="BBOX ID")
    attributes = models.ForeignKey(to="labels_attributes", on_delete=CASCADE, verbose_name="Attributes")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["bbox_id", "attributes"],
                name = "unique box attributes"
            )
        ]  

# class video_data(Model):
#     id = models.BigAutoField(help_text="Video ID", verbose_name="VIDEO ID", primary_key=True)
#     src_path = models.FilePathField(path=BASE_DIR, verbose_name="SOURCE PATH")
#     name = models.CharField(max_length=50, verbose_name="NAME")
#     start_date = models.DateTimeField(blank=True, null=True, verbose_name="시작시간")
#     #차후 추가 예정
#     # end_date = models.DateTimeField(blank=True, null = True)
#     # img_height = models.PositiveIntegerField()
#     # img_width = models.PositiveIntegerField()
    
    
#     VIDEO_STATE = [
#         ("ORI", "UPDATEED ORIGIN"),
#         ("ING_OBJ", "DETECTING OBJECT"),
#         ("ED_OBJ", "DETECTED OBJECT"),
#         ("ING_MUL", "DETECTING MULTICLASS"),
#         ("ED_MUL", "DETECTING MULTICLASS"),
#     ]
#     state = models.CharField(max_length=10, choices=VIDEO_STATE, verbose_name="STATE")
    
# class video_frame(Model):
#     id = models.BigAutoField(help_text="Frame ID", verbose_name="FRAME ID", primary_key=True)
#     video = models.ForeignKey("video_data", related_name="video data", on_delete=CASCADE, verbose_name="VIDEO ID")
#     num = models.BigIntegerField(help_text="frame number", verbose_name="FRAME NUMBER")
        
#     VIDEO_STATE = [
#         ("ORI", "ORIGIN"),
#         ("DET_OBJ", "DETECTED OBJECT"),
#         ("TRK_OBJ", "TRACKED OBJECT"),
#         ("INF_MUL", "INFORENCE MULTICLASS"),
#     ]
#     state = models.CharField(max_length=10, choices=VIDEO_STATE, verbose_name="STATE")
    
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["video", "num"],
#                 name = "unique frame"
#             )
#         ]
        

# class bbox_location(Model):
#     frame
