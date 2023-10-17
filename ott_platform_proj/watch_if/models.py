from django.db import models
from star_ratings.models import Rating
from django.contrib.auth.models import User, AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Movies(models.Model):
    category = models.ForeignKey(Category,default=1, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    description = models.TextField()
    duration = models.PositiveIntegerField(default=0)
    release_date = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=50)
    image = models.ImageField(upload_to='content/images/')
    video_url = models.CharField(max_length=255,blank=True)
    content_creator =  models.ForeignKey(User,default=1, on_delete=models.CASCADE)
    rating = Rating.objects.create()


    def __str__(self):
        return self.title


class Tv_shows(models.Model):
    category = models.ForeignKey(Category,default=1, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    description = models.TextField()
    language = models.CharField(max_length=50)
    image = models.ImageField(upload_to='content/images/')
    content_creator = models.ForeignKey(User,default=1, on_delete=models.CASCADE)
    rating = Rating.objects.create()
    # video_url = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

class Kids(models.Model):
    category = models.ForeignKey(Category,default=1, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    description = models.TextField()
    duration = models.PositiveIntegerField(default=0)

    language = models.CharField(max_length=50)
    image = models.ImageField(upload_to='content/images/')
    content_creator = models.ForeignKey(User,default=1, on_delete=models.CASCADE)
    rating = Rating.objects.create()
    video_url = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return self.title
class Season(models.Model):

    tv_show = models.ForeignKey(Tv_shows, on_delete=models.CASCADE)
    season_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.tv_show} - Season {self.season_number}"

class Episode(models.Model):
    tv_show = models.ForeignKey(Tv_shows, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    release_date = models.DateTimeField(auto_now_add=False)
    duration = models.PositiveIntegerField(default=0)
    video_url = models.URLField(max_length=255,blank=True)
    episode_number = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return f" Episode {self.episode_number}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='user_profiles/', blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user

class UserFavorite(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    # Add more fields if needed

class UserVideoActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    watch_later = models.BooleanField(default=False)
    viewed_history = models.BooleanField(default=False)
    # Add more fields if needed


class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Subscription(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.subscriber} subscribed to {self.content_object}'


class ViewedContent(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.subscriber} viewed {self.content_object}'

class Favorite(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Define your content model


class CustomAdminUser(AbstractUser):
    phone_number = models.CharField(max_length=15, default='')  # Set your desired default value
    # Add other custom fields if needed
    # Specify related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='custom_users_groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='custom_users_permissions'
    )

    def __str__(self):
        return self.username


class WatchlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')


class Watchlist2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    series = models.ForeignKey(Tv_shows, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'series')

    def __str__(self):
        return f"Watchlist2 Item for {self.user.username}"