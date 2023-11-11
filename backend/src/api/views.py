from transformers import TFCamembertForSequenceClassification
from rest_framework.decorators import api_view
from transformers import CamembertTokenizer
from django.http import JsonResponse
from api.models import *
import tensorflow as tf
import joblib as memory
import pandas as pd
import numpy as np

from api.utils import *

MAX_SEQ_LEN = 400
model_name = "camembert-base"
tokenizer = CamembertTokenizer.from_pretrained(model_name)
data_storage = "data/"
model_storage = "data/models/"

# @request.query: percentTrain
@api_view(['GET'])
def generateTrainTest(request):
    percentTrain = request.query_params.get('percentTrain')
    serializedTrainReview, serializedTestReview, totalsReview = getTrainAndTestReviewFromDB(percentTrain)

    print("total reviews:", totalsReview)
    print('trainset size:', len(serializedTrainReview))
    print('testset size:', len(serializedTestReview))

    dataframeTrain = pd.DataFrame(serializedTrainReview)
    # dataframeTrain.assign(polarity=lambda row : find_polarity(row), axis=1)
    dataframeTrain.loc[:,'polarity'] = dataframeTrain.apply(lambda row : find_polarity(row), axis=1)
    #Create new column polarity & apply lambda function to each row 
    dataframeTrain.to_csv(data_storage + "Trainset.csv", index=False)
    
    dataframeTest = pd.DataFrame(serializedTestReview)
    dataframeTest.loc[:,'polarity'] = dataframeTrain.apply(lambda row : find_polarity(row), axis=1)
    dataframeTest.to_csv(data_storage + "Testset.csv", index=False)

    ProcessDatasets()
    return JsonResponse({"trainset": serializedTrainReview, "testset": serializedTestReview},  safe=True)


def ProcessDatasets():
    # TODO: same for testset
    trainset = pd.read_csv(data_storage + 'Trainset.csv')
    trainset["review_content"] = trainset["review_content"].replace(r'^s*$', float('NaN'), regex = True) 
    trainset.dropna(inplace = True) 
    print("PROCESS SHAPE Before encode:", trainset["review_content"].shape)

    # guardrails for empty str reviews_content
    trainReviews = np.array(trainset["review_content"][~trainset["review_content"].isna()])
    labels_train  = np.array(trainset['polarity'])

    print("PROCESS SHAPE:", trainReviews.shape, labels_train.shape)
    encoded_train = encode_reviews(tokenizer, trainReviews, MAX_SEQ_LEN)
    
    memory.dump({
        "encoded_train": encoded_train,
        "labels_train": labels_train
    }, data_storage + "encodedTrainset.z")

    return JsonResponse({"message": "done"}, safe=True)

@api_view(['GET'])
def readTokenizedEncodedReviews(request):
    datas = memory.load(data_storage + "encodedTrainset.z")
    encoded_train = datas["encoded_train"]
    labels = datas["labels_train"]
    print("INFOS PRINT")
    print(encoded_train["input_ids"].shape, encoded_train["attention_mask"].shape)
    print(labels.shape)
    print(datas)
    return JsonResponse({"message": "done"})



@api_view(['GET'])
def compileModel(request):
    model = TFCamembertForSequenceClassification.from_pretrained("jplu/tf-camembert-base")
    opt = tf.keras.optimizers.Adam(learning_rate=5e-6, epsilon=1e-08)
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)    

    model.compile(optimizer=opt, loss=loss_fn, metrics=['accuracy'])
    memory.dump(model, model_storage + "compiledModel.z")
    
    # initial_weights = model.get_weights()
    modelSummary = model.summary()
    memory.dump(modelSummary, model_storage + "modelSummary.z")

    return JsonResponse({"message": "done"})


@api_view(['GET'])
def TrainModel(request):
    print("Train model")
    # Todo: Bug here
    # model = memory.load(model_storage + 'compiledModel.z')

    encodedDatasets = memory.load(data_storage + "encodedTrainset.z")
    print(encodedDatasets)

    reviews = encodedDatasets["encoded_train"]
    labels  = encodedDatasets["labels_train"]

    model = TFCamembertForSequenceClassification.from_pretrained("jplu/tf-camembert-base")
    print("load optimizer")
    opt = tf.keras.optimizers.Adam(learning_rate=5e-6, epsilon=1e-08)
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)    

    print("compile model")
    model.compile(optimizer=opt, loss=loss_fn, metrics=['accuracy'])

    # ! REVIEW to get test & validation sets
    # history = model.fit(
    #     reviews, labels, epochs=1, batch_size=4, 
    #     validation_data=(encoded_valid, y_val), verbose=1
    # )

    print('review to train:', reviews["input_ids"].shape, reviews["attention_mask"].shape)
    print('labels on train:', labels.shape)

    history = model.fit(reviews, labels, epochs=1, batch_size=4, verbose=1)

    print("memory model")
    memory.dump(history, model_storage + "history.z")
    memory.dump(model,  model_storage + "trainedModel.z")
    print("end train")
    return JsonResponse({"message": "done"})

@api_view(['POST'])
def predict(request):
    review_id = request.data.get("review_id")
    print("Review id:", review_id)

    review = Reviews.objects.get(id_review = review_id)
    print("review: ", review)

    model = memory.load(model_storage + "trainedModel.z")
    scores = model.predict()
    y_pred = np.argmax(scores, axis=1)

    return JsonResponse({"prediction": y_pred})