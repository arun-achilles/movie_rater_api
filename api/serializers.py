from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Movie, Rating, Review
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'password']
		extra_kwargs = {'password': {'write_only': True, 'required': True}}

	def create(self, validated_data):
		user = User.objects.create_user(**validated_data)
		Token.objects.create(user=user)
		return user

class RatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Rating
		fields = ['id', 'stars', 'user', 'movie']

class ReviewSerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)
	class Meta:
		model = Review
		fields = ['id', 'comment', 'user', 'movie']		

class MovieSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movie
		fields = ['id', 'title', 'description', 'ratings_count', 'average_rating']

class MovieDetailSerializer(serializers.ModelSerializer):
	reviews = ReviewSerializer(many=True, read_only=True)
	class Meta:
		model = Movie
		fields = ['id', 'title', 'description', 'ratings_count', 'average_rating', 'reviews']

