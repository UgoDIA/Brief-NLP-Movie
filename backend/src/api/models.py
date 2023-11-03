from django.db import models


class Movies(models.Model):
    id_movie = models.IntegerField(primary_key=True)
    movie_title = models.CharField(max_length=200,blank=True, null=True)
    movie_rank = models.IntegerField()
    movie_score_press = models.DecimalField(max_digits=2, decimal_places=1)
    movie_score_spectator = models.DecimalField(max_digits=2, decimal_places=1)
    nlp_score = models.DecimalField(db_column='NLP_score', max_digits=2, decimal_places=1, blank=True, null=True)
    nlp_rank = models.IntegerField(db_column='NLP_rank', blank=True, null=True)
    
    class Meta:
        db_table = 'movies'


class Reviews(models.Model):
    id_review = models.AutoField(primary_key=True)
    review_score = models.DecimalField(max_digits=2, decimal_places=1)
    review_content = models.TextField(blank=True, null=True)
    # polarity = models.IntegerField(blank=True, null=True)
    id_movie = models.ForeignKey(Movies, models.CASCADE, db_column='id_movie')

    class Meta:
        db_table = 'reviews'
