# Generated by Django 4.0.8 on 2022-10-18 08:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='search_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obj_id', models.PositiveSmallIntegerField(verbose_name='Object ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Image')),
                ('fps', models.FloatField(null=True, verbose_name='FPS')),
                ('last_frame', models.FloatField(null=True, verbose_name='Last Frame')),
            ],
            options={
                'db_table': 'search_result',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='labels_mainclass_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Mainclass')),
            ],
        ),
        migrations.CreateModel(
            name='video_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(null=True, upload_to='videofiles/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])])),
                ('fps', models.FloatField(null=True, verbose_name='FPS')),
                ('last_frame', models.FloatField(null=True, verbose_name='Last Frame')),
            ],
        ),
        migrations.CreateModel(
            name='labels_attributes_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20, verbose_name='Type')),
                ('mainclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search_app.labels_mainclass_type', verbose_name='Mainclass')),
            ],
        ),
        migrations.CreateModel(
            name='labels_attributes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveSmallIntegerField()),
                ('name', models.CharField(max_length=30, verbose_name='Attributes')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search_app.labels_attributes_type', verbose_name='Type')),
            ],
        ),
        migrations.CreateModel(
            name='bbox_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame_num', models.PositiveBigIntegerField(null=True, verbose_name='Frame')),
                ('obj_id', models.PositiveSmallIntegerField(null=True, verbose_name='Object ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Image')),
                ('mainclass', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='search_app.labels_mainclass_type', verbose_name='Mainclass')),
                ('video', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='search_app.video_data', verbose_name='Type')),
            ],
        ),
        migrations.CreateModel(
            name='bbox_attributes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attributes', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='search_app.labels_attributes', verbose_name='Attributes')),
                ('bbox', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='search_app.bbox_data', verbose_name='BBOX ID')),
            ],
        ),
        migrations.AddConstraint(
            model_name='labels_attributes_type',
            constraint=models.UniqueConstraint(fields=('mainclass', 'type'), name='unique frame'),
        ),
        migrations.AddConstraint(
            model_name='labels_attributes',
            constraint=models.UniqueConstraint(fields=('type', 'name'), name='unique attribute'),
        ),
        migrations.AddConstraint(
            model_name='bbox_data',
            constraint=models.UniqueConstraint(fields=('video', 'frame_num', 'obj_id'), name='unique object'),
        ),
        migrations.AddConstraint(
            model_name='bbox_attributes',
            constraint=models.UniqueConstraint(fields=('bbox_id', 'attributes'), name='unique box attributes'),
        ),
    ]
