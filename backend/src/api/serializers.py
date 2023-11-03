from rest_framework import serializers
from django.core import serializers as DJSerializer
from api.models import Movies, Reviews
from transformers import CamembertTokenizer

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
    tokenized = serializers.defaultdict(source="review_content")

    # tk = json.dump(tokenizer(tokenized))
    class Meta:
        model = Reviews
        fields = "__all__"