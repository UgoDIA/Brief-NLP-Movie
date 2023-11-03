from api.serializers import ReviewToCSVSerialiser
from api.models import Reviews
from decimal import Decimal
import numpy as np
import math

def nombre_items_du_pourcentage(total_items, pourcentage):
    pourcentage = int(pourcentage)
    total_items = int(total_items)

    if pourcentage < 0 or pourcentage > 100:
        raise ValueError("Le pourcentage doit être compris entre 0 et 100.")
    
    nombre_items = (pourcentage / 100) * total_items
    reste = 100 - pourcentage
    nombre_items_rest = (reste / 100) * total_items

    return math.floor(nombre_items), math.floor(nombre_items_rest)

def encode_reviews(tokenizer, reviews, max_length):
    token_ids = np.zeros(shape=(len(reviews), max_length), dtype=np.int32)
    for i, review in enumerate(reviews):
        encoded = tokenizer.encode(review, max_length=max_length)
        token_ids[i, 0:len(encoded)] = encoded
    attention_mask = (token_ids != 0).astype(np.int32)
    return {"input_ids": token_ids, "attention_mask": attention_mask}

def find_polarity(row):
    if Decimal(row['review_score']) <= 2.0:
        return -1
    elif Decimal(row['review_score']) >= 4.0:
        return 1
    else:
        return 0
    
def getTrainAndTestReviewFromDB(percentTrain):
    totalReviews = Reviews.objects.all().count()
    TrainSize, TestSize = nombre_items_du_pourcentage(total_items=totalReviews, pourcentage=percentTrain)

    print("Train size:", TrainSize)
    print("Test size:", TestSize)

    reviewsTrain = Reviews.objects.all()[0:TrainSize]
    serializedTrainReview = ReviewToCSVSerialiser(reviewsTrain, many=True)

    reviewsTest = Reviews.objects.all().order_by('-id_review')[:TestSize]
    serializedTestReview = ReviewToCSVSerialiser(reviewsTest, many=True)

    print(serializedTestReview)
    return serializedTrainReview.data, serializedTestReview.data, totalReviews