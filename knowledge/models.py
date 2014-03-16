from django.db import models
import dbarray

# Create your models here.

class Knowledge(models.Model):
    title = models.CharField(max_length=1000)
    keyword = models.CharField(max_length=1000)
    abstract = models.TextField(max_length=1000)
    content = models.TextField(max_length=50000)
    images = models.TextField(max_length=2000)
    min = models.IntegerField(10)
    max = models.IntegerField(10)
    apply_sex = models.TextField(10)

class KnowledgeCollection(models.Model):
    user_id = models.IntegerField(10,null=True)
    collection_list = models.CharField(max_length=20000,null=True)

class PushInfo(models.Model):
    user_id = models.IntegerField(10)
    knowledge_info = dbarray.IntegerArrayField(null=True)
    merchant_info = dbarray.IntegerArrayField(null=True)
