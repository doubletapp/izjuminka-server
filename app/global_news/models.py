# # -*- coding: utf-8 -*
#
# from django.db.models
# from datetime import datetime
#
#
# class Sites(models.Model):
#     name = models.CharField(max_length=60)
#     website = models.URLField()
#
#     def __unicode__(self):
#         return self.name
#
#
# class Rss(models.Model):
#     name = models.ForeignKey(Sites)
#     rss = models.URLField()
#     last_update = models.DateTimeField(default=datetime(1980, 1, 1))
#
#     def __unicode__(self):
#         return self.name.name
#
#
# class News(models.Model):
#     rss = models.ForeignKey(Rss)
#     title = models.CharField(max_length=400)
#     category = models.CharField(max_length=400)
#     link = models.URLField()
#     description = models.TextField()
#     # image = models.ImageField(upload_to='/tmp')
#     datatime = models.DateTimeField()
#     mongo_key = models.TextField()
#
#     # def __unicode__(self):
#     #   return self.rss.name + " " + self.title + " " +  self.description
