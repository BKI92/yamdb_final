from rest_framework import serializers

from api.models import Category, Genre, Title


class CategorySlugRelatedField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return {'name': value.name, 'slug': value.slug}

    def to_internal_value(self, data):
        category = Category.objects.get(slug=data)
        return category


class GenreSlugRelatedField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return {'name': value.name, 'slug': value.slug}

    def get_genres_slugs(self):
        genres_slugs = [genre.slug for genre in Genre.objects.all()]
        return genres_slugs


class AuthorSlugRelatedField(serializers.SlugRelatedField):
    def to_representation(self, author):
        return author.username


