from django.db import models
from django_db_views.db_view import DBView
from django.db.models import CASCADE, Model
from django.core.validators import FileExtensionValidator

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class uploaded_data(Model):
    file =  models.FileField(upload_to='videos/', null=True, validators=[FileExtensionValidator(allowed_extensions=['mp4'])])

class video_data(Model):
    src_path = models.FilePathField(max_length=200, path=BASE_DIR, verbose_name="SOURCE PATH", null=True)
    name = models.CharField(max_length=100, verbose_name="NAME")
    fps = models.FloatField(verbose_name="FPS", null=True)
    last_frame = models.FloatField(verbose_name="Last Frame", null=True)

class labels_mainclass_type(Model):
    name = models.CharField(max_length=20, verbose_name="Mainclass")

class labels_attributes_type(Model):
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
    type = models.ForeignKey(to="labels_attributes_type", on_delete=CASCADE, verbose_name="Type")
    index = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=30, verbose_name="Attributes")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["type", "name"],
                name = "unique attribute"
            )
        ]
 
class bbox_data(Model):
    video = models.ForeignKey(to="video_data", on_delete=CASCADE, verbose_name="Type", null=True)
    frame_num = models.PositiveBigIntegerField(verbose_name="Frame", null=True)
    obj_id = models.PositiveSmallIntegerField(verbose_name="Object ID", null=True)
    image = models.ImageField(blank=True, null=True, upload_to="images/", verbose_name="Image")
    mainclass = models.ForeignKey(to="labels_mainclass_type", on_delete=CASCADE, verbose_name="Mainclass", null=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["video", "frame_num", "obj_id"],
                name = "unique object"
            )
        ]    

class bbox_attributes(Model):
    bbox = models.ForeignKey(to="bbox_data", on_delete=CASCADE, verbose_name="BBOX ID", null=True)
    attributes = models.ForeignKey(to="labels_attributes", on_delete=CASCADE, verbose_name="Attributes", null=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["bbox_id", "attributes"],
                name = "unique box attributes"
            )
        ]  

class search_result(DBView):
    bbox = models.ForeignKey(to="bbox_data", on_delete=models.DO_NOTHING, verbose_name="BBOX ID")
    obj_id = models.PositiveSmallIntegerField(verbose_name="Object ID")
    image = models.ImageField(blank=True, null=True, upload_to="images/", verbose_name="Image")
    fps = models.FloatField(verbose_name="FPS", null=True)
    last_frame = models.FloatField(verbose_name="Last Frame", null=True)

