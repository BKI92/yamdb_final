from django.db import models

# Create your models here.
from users.models import CustomUser


class UserCode(models.Model):
    email = models.EmailField(primary_key=True, unique=True)
    confirmation_code = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200, unique=True)
    year = models.IntegerField(blank=True, default=0)
    description = models.CharField(max_length=400, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name="titles", blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name='titles', blank=True)

    def __str__(self):
        return str(self.pk)


class Review(models.Model):
    SCORES = zip(range(1, 11), range(1, 11))
    text = models.TextField()
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name="reviews")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name="reviews")
    score = models.IntegerField(choices=SCORES)
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return str(self.pk)


class Comment(models.Model):
    text = models.CharField(max_length=200)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name="comments")
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name="comments")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return str(self.pk)
