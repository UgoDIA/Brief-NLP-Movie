from api.models import *
from rest_framework.decorators import api_view
from api.serializers import  JoinSerialiser
from django.http import JsonResponse
import pandas as pd
import math
from decimal import Decimal

def nombre_items_du_pourcentage(total_items, pourcentage):
    pourcentage = int(pourcentage)
    total_items = int(total_items)

    if pourcentage < 0 or pourcentage > 100:
        raise ValueError("Le pourcentage doit être compris entre 0 et 100.")
    
    nombre_items = (pourcentage / 100) * total_items
    reste = 100 - pourcentage
    nombre_items_rest = (reste / 100) * total_items

    return nombre_items, nombre_items_rest

# Create your views here.
@api_view(['GET'])
def getTrainDataset(request):
    percentTrain = request.query_params.get('percentTrain')


    totalMovie = Reviews.objects.all().count()
    TrainSize, TestSize = nombre_items_du_pourcentage(total_items=totalMovie, pourcentage=percentTrain)

    reviewsTrain = Reviews.objects.all()[0:TrainSize]
    serializedTrainReview = JoinSerialiser(reviewsTrain, many=True)

    reviewsTest = Reviews.objects.all()[TrainSize:TestSize]
    serializedTestReview = JoinSerialiser(reviewsTest, many=True)

    Trainset = {}
    Trainset["tokenizedContent"] = []
    Trainset["score"] = []

    Testset = {}
    Testset["tokenizedContent"] = []
    Testset["score"] = []

    for review in serializedTrainReview.data:
        Trainset["tokenizedContent"].append(review['review_content'])
        Trainset["score"].append(math.floor(Decimal(review["review_score"])))

    for review in serializedTestReview.data:
        Testset["tokenizedContent"].append(review['review_content'])
        Testset["score"].append(math.floor(Decimal(review["review_score"])))

    dataframeTrain = pd.DataFrame(Trainset)
    dataframeTrain.to_csv("Trainset.csv")

    dataframeTrain = pd.DataFrame(Testset)
    dataframeTrain.to_csv("Testset.csv")

    return JsonResponse({"trainset": Trainset, "testset": Testset},  safe=True)


from transformers import CamembertTokenizer
def tokenizer(review):
    modelName = "camembert/camembert-large"
    tokenizer = CamembertTokenizer.from_pretrained(modelName)
    reviewContent = review['review_content']
    return tokenizer.encode(reviewContent)