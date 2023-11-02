from api.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import MoviesSerializer, JoinSerialiser
from django.http import HttpResponse, JsonResponse

# Create your views here.
@api_view(['GET'])
def getTrainDataset(request):
    print('Will return dataset to train model as pandas dataframe where each review represents a line')
    reviews = Reviews.objects.select_related("id_movie").all()
    serializedMovies = JoinSerialiser(reviews, many=True)
    return JsonResponse(serializedMovies.data,  safe=False)
