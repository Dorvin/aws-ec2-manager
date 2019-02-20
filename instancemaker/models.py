from django.db import models

# Create your models here.

class Room(models.Model):
    room_name = models.CharField(max_length=200, default="default room name")
    room_code = models.CharField(max_length=200, default="-1")
    date_generated = models.DateTimeField('date generated')
    server_ip = models.CharField(max_length=200, default="0.0.0.0")
    instance_id = models.CharField(max_length=200, default="i-0")