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

    return math.floor(nombre_items), math.floor(nombre_items_rest)

# Create your views here.
@api_view(['GET'])
def getTrainDataset(request):
    percentTrain = request.query_params.get('percentTrain')

    totalReviews = Reviews.objects.all().count()
    TrainSize, TestSize = nombre_items_du_pourcentage(total_items=totalReviews, pourcentage=percentTrain)

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

    print("Total reviews:", totalReviews)
    print("Train size:", TrainSize)
    print("Test size:", TestSize)

    print("datas:", serializedTrainReview.data)

    dataframeTrain = pd.DataFrame(serializedTrainReview.data)
    dataframeTrain.to_csv("Trainset.csv", index=False)

    print("ok train dataframe")    

    dataframeTest = pd.DataFrame(serializedTestReview.data)
    dataframeTest.to_csv("Testset.csv", index=False)

    print("ok test dataframe")    

    return JsonResponse({"trainset": Trainset, "testset": Testset},  safe=True)


from transformers import CamembertTokenizer
def tokenizer(review):
    modelName = "camembert/camembert-large"
    tokenizer = CamembertTokenizer.from_pretrained(modelName)
    reviewContent = review['review_content']
    return tokenizer.encode(reviewContent)