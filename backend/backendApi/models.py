from django.db import models


class Comment(models.Model):
    UID = models.AutoField(primary_key = True)
    Name = models.CharField(max_length = 50)
    Tag = models.CharField(max_length = 50)
    Comment = models.CharField(max_length = 500)
    Year = models.IntegerField()
    Checked = models.BooleanField(default = False)
    Count = models.IntegerField(default = 0)

    class Meta:
        db_table = 'comment'