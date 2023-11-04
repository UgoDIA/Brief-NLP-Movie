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

class ReviewToCSVSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ["review_score", "review_content","id_review"]