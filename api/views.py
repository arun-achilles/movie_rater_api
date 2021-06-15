from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Movie, Rating, Review
from .serializers import MovieSerializer, RatingSerializer, UserSerializer, ReviewSerializer, MovieDetailSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (AllowAny, )

	def create(self, request, *args, **kwargs):
		response = super().create(request, *args, **kwargs)
		token, created = Token.objects.get_or_create(user_id=response.data["id"])
		response.data["token"] = str(token)
		return response


class MovieViewSet(viewsets.ModelViewSet):
	queryset = Movie.objects.all()
	serializer_class = MovieSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated, )

	action_serializers = {
        'retrieve': MovieDetailSerializer,
    }

	def get_serializer_class(self):

		if hasattr(self, 'action_serializers'):
			return self.action_serializers.get(self.action, self.serializer_class)

		return super(MovieViewSet, self).get_serializer_class	

	@action(detail=True, methods=['POST'])
	def rate_movie(self, request, pk=None, *args, **kwargs):
		if 'stars' in request.data:
			movie = Movie.objects.get(id=pk)
			stars = request.data['stars']
			user = request.user
			try:
				rating = Rating.objects.get(user=user.id, movie=movie.id)
				rating.stars = stars
				rating.save()
				serializer = RatingSerializer(rating, many=False)
				return Response({'message': 'You rating is updated', 'result': serializer.data}, status=status.HTTP_200_OK)
			except:
				rating = Rating.objects.create(user=user, movie=movie, stars=stars)
				serializer = RatingSerializer(rating, many=False)
				return Response({'message': 'You rating is created', 'result': serializer.data}, status=status.HTTP_200_OK)
		else:
			return Response({'message': 'failed to rate'}, status=status.HTTP_400_BAD_REQUEST)

	@action(detail=True, methods=['POST'])
	def review_movie(self, request, pk=None, *args, **kwargs):
		if 'review' in request.data:
			movie = Movie.objects.get(id=pk)
			comment = request.data['review']
			user = request.user
			try:
				review = Review.objects.get(user=user.id, movie=movie.id)
				review.comment = comment
				review.save()
				serializer = ReviewSerializer(review, many=False)
				return Response({'message': 'You review is updated', 'result': serializer.data}, status=status.HTTP_200_OK)
			except Exception as e:
				review = Review.objects.create(user=user, movie=movie, comment=comment)
				serializer = ReviewSerializer(review, many=False)
				return Response({'message': 'You review is created', 'result': serializer.data}, status=status.HTTP_200_OK)
		else:
			return Response({'message': 'failed to add review'}, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
	queryset = Rating.objects.all()
	serializer_class = RatingSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated, )

	def update(self, request, *args, **kwargs):
		response = {'message': 'You cant update rating like that'}
		return Response(response, status=status.HTTP_400_BAD_REQUEST)

	def create(self, request, *args, **kwargs):
		response = {'message': 'You cant create rating like that'}
		return Response(response, status=status.HTTP_400_BAD_REQUEST)

class ReviewViewSet(viewsets.ModelViewSet):
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated, )

	def update(self, request, *args, **kwargs):
		response = {'message': 'You cant update rating like that'}
		return Response(response, status=status.HTTP_400_BAD_REQUEST)

	def create(self, request, *args, **kwargs):
		response = {'message': 'You cant create rating like that'}
		return Response(response, status=status.HTTP_400_BAD_REQUEST)		