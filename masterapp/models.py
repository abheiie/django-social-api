from django.db import models

# Create your models here.



class Couser(models.Model):
    """
    This is main model for users of application
    """
    username = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    password = models.CharField(max_length=10, null=True, blank=True)
    fullname = models.CharField(max_length=30, null=True, blank=True)
    avatar = models.ImageField(upload_to='images/', default="")
    dob = models.DateField(null=True, blank= True)
    about = models.CharField(max_length=200, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    followings_count = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    bookmarks_count = models.PositiveIntegerField(default=0)
    posts_count = models.PositiveIntegerField(default=0)
    is_account_verified = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.username


class Contact(models.Model):
    follower = models.ForeignKey( Couser, related_name='followings', on_delete=models.CASCADE)
    following = models.ForeignKey(
        Couser, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return u'%s follows %s' % (self.follower.username, self.following.username)


