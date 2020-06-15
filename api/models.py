from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from functools import reduce
# Create your models here.
class Movie(models.Model):
	title = models.CharField(max_length=72)
	description = models.TextField(max_length=360)

	def ratings_count(self):
		ratings = Rating.objects.filter(movie=self)
		return len(ratings)

	def average_rating(self):
		ratings = Rating.objects.filter(movie=self)
		total = sum(list(map(lambda x: x.stars, ratings))) 
		return total/len(ratings) if len(ratings) > 0 else 0


class Rating(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

	class Meta:
		unique_together = (('user', 'movie'),)
		index_together = (('user', 'movie'),)