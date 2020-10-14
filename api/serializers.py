from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from api import serializer_fields
from api.models import UserCode, Genre, Title, Review, Comment
from api.models import Category
from users.models import CustomUser
import datetime as dt


class UserCodeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email',)
        model = UserCode


class MyTokenObtainPairSerializer(serializers.Serializer):

    def validate(self, data):
        email = self.context['request'].data.get('email')
        if dt.datetime.now(dt.timezone.utc) - UserCode.objects.get(
                email=email).created >= dt.timedelta(minutes=10000):
            raise serializers.ValidationError(
                f"Your verification code is outdated.")
        new_user = CustomUser.objects.get(email=email)
        refresh = self.get_token(new_user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')

    def validate_username(self, data):
        username = self.context['request'].data.get('username')
        if CustomUser.objects.filter(username=username):
            raise serializers.ValidationError(
                f"User with this username already exist.")
        return data


class SpecificUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')

    def validate(self, attrs):
        slug = self.context['request'].data.get('slug')
        if not slug:
            raise serializers.ValidationError(
                f"Slug is the requirement field.")
        if Genre.objects.filter(slug=slug):
            raise serializers.ValidationError(
                f"Category with this slug already exist.")
        return attrs


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')

    def validate(self, attrs):
        slug = self.context['request'].data.get('slug')
        if not slug:
            raise serializers.ValidationError(
                f"Slug is the requirement field.")
        if Genre.objects.filter(slug=slug):
            raise serializers.ValidationError(
                f"Genre with this slug already exist.")
        return attrs


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField('get_rating')
    category = serializer_fields.CategorySlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug')
    genre = serializer_fields.GenreSlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        title_id = obj.id
        reviews = Review.objects.filter(title=title_id)
        if reviews:
            total_rating = [review.score for review in reviews]
            avg_rating = sum(total_rating) / len(total_rating)
            return avg_rating


class ReviewSerializer(serializers.ModelSerializer):
    author = serializer_fields.AuthorSlugRelatedField(slug_field='id',
                                                      read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, attrs):
        method = self.context['request'].method
        if Review.objects.filter(author=self.context['request'].user,
                                 title=self.get_title()) and method != 'PATCH':
            raise serializers.ValidationError(
                f"You  have already created review on this title.")

        return attrs

    def get_title(self):
        title = get_object_or_404(Title, id=self.context.get('view').kwargs.get(
            'title_id'))
        return title


class CommentSerializer(serializers.ModelSerializer):
    author = serializer_fields.AuthorSlugRelatedField(slug_field='id',
                                                      read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
