import os
import uuid
import hashlib

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount 

class ProfileModel(models.Model):
	class Meta:
		app_label = ''
		
	"Profile Information"
	first_name = models.TextField(max_length=128, blank=True, null=True)
	last_name = models.TextField(max_length=128, blank=True, null=True)
	phone = models.TextField(blank=True, null=True, max_length=250)
	timezone = models.TextField(max_length=50, null=True, blank=True)
	language = models.TextField(max_length=50, blank=True, null=True)
	location_latitude = models.TextField(max_length=50, blank=True, null=True)
	location_longitude = models.TextField(max_length=50, blank=True, null=True)
	profile_img = models.FileField(upload_to='documents/%Y/%m/%d',blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.first_name

def avatar_upload(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("avatars", filename)

class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name = 'profile')

	#avatar = models.ImageField(upload_to=avatar_upload, blank=True)
	#title = models.CharField(max_length=100, blank=True)
	#location = models.CharField(max_length=100, blank=True)
	
	def __unicode__(self):
		return "{}'s profile".format(self.user.username)

	class Meta:
		db_table = 'user_profile'

	def account_verified(self):
		if self.user.is_authenticated:
			result = EmailAddress.objects.filter(email=self.user.email)
			if len(result):
				return result[0].account_verified
		return False
		
	def profile_image_url(self):
		li_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='linkedin')

		if len(li_uid):
			return "https://graph.facebook.com/{}/picture?width=40&height=40".format(li_uid[0].uid)
		return "https://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())	

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])