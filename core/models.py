from django.db import models
from django.contrib.auth.models import User
import hashlib
import redis
import uuid

def make_uuid():
    return str(uuid.uuid4())

class UserUrl(models.Model):
	user = models.ForeignKey(User)
	url = models.URLField()
	sequence = models.CharField(max_length=50, null=True)

	def save(self, *args, **kwargs):
		r= redis.Redis()
		if self.sequence == None:
			h = hashlib.new('md5')
			h.update(self.url)
			self.sequence = h.hexdigest()[:5]
		r.set(sequence,url)
		super(UserUrl, self).save()

class UserKey(models.Model):
	user = models.ForeignKey(User)
	key = models.TextField(default=make_uuid, editable=False)


class UserBrand(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=100)
	regex = models.CharField(max_length=500)

class Hit(models.Model):
	url = models.ForeignKey(UserUrl)
	time = models.DateTimeField(auto_now_add=True)