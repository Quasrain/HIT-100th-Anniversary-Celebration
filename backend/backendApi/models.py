from django.db import models


class Comment(models.Model):
    UID = models.AutoField(primary_key = True)
    Department = models.CharField(max_length = 50)
    Grade = models.CharField(max_length = 50)
    Identity = models.CharField(max_length = 50)
    Name = models.CharField(max_length = 50)
    Post = models.CharField(max_length = 500)
    Phone = models.IntegerField(default = 0)
    Count = models.IntegerField(default = 0)

    class Meta:
        db_table = 'comment'
