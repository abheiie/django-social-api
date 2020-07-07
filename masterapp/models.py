from django.db import models

# Create your models here.



class Couser(models.Model):
    """
    This is main model for users of application
    """
    username = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=40, null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    password = models.CharField(max_length=30, null=True, blank=True)
    fullname = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField(upload_to='images/', default="")
    dob = models.DateField(null=True, blank= True)
    about = models.CharField(max_length=300, null=True, blank=True)
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
    """
    This model is for storing who followers and following
    """
    follower = models.ForeignKey( Couser, related_name='followings', on_delete=models.CASCADE)
    following = models.ForeignKey( Couser, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return u'%s follows %s' % (self.follower.username, self.following.username)


class Category(models.Model):
    """
    For storing categories of posts
    """
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    For storing posts
    """
    title = models.CharField(max_length=100, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to='images/', default="", null=True, blank=True)
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE, null=True, blank=True)
    couser = models.ForeignKey(Couser, related_name='posts', on_delete=models.CASCADE)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    bookmarks_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Like(models.Model):
    """
    for storing likes on posts
    """
    couser = models.ForeignKey(Couser, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Bookmark(models.Model):
    """
    For storing bookmarks of posts
    """
    couser = models.ForeignKey(Couser, related_name='bookmarks', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='bookmarks', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Comment(models.Model):
    """
    For storing Comments of posts
    """
    body = models.CharField(max_length=100, null=True, blank=True)
    couser = models.ForeignKey(Couser, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)



class EntityType(models.Model):
    """
    For storing entity type eg(post, user, comment) used during report on these entities
    """
    name=models.CharField(max_length=200, null=True, blank=True)


class ReportType(models.Model):
    """
    For storing predefined report types
    """
    detail=models.CharField(max_length=200, null=True, blank=True)

    
class Report(models.Model):
    """
    For Storing reports on different entities
    """
    reporter = models.ForeignKey(Couser, related_name='couser_reporters',on_delete=models.CASCADE, null=True, blank=True)
    entity_type = models.CharField(max_length=40, null=True, blank=True)
    report_type = models.ForeignKey(ReportType, related_name='couser_report_types',on_delete=models.CASCADE, null=True, blank=True)
    post =  models.ForeignKey(Post, related_name='post_posts',on_delete=models.CASCADE, null = True, blank = True, default = None)
    couser = models.ForeignKey(Couser, related_name='report_cousers',on_delete=models.CASCADE, null = True, blank = True, default = None)
    comment = models.ForeignKey(Comment, related_name='report_comments',on_delete=models.CASCADE, null = True, blank = True, default = None)
    custome_report = models.CharField(max_length=200, null=True, blank=True)

