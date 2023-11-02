from rest_framework import serializers
from api.models import Movies, Reviews



class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews 
        fields = "__all__"

class MoviesSerializer(serializers.ModelSerializer):
    reviews = ReviewsSerializer(read_only = True)
    class Meta:
        model = Movies
        fields ="__all__"

class JoinSerialiser(serializers.ModelSerializer):
    id_movie = serializers.CharField(source="id_movie.movie_title")

    class Meta:
        model = Reviews
        fields = "__all__"