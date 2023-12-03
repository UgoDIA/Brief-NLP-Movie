# Generated by Django 4.2.6 on 2023-12-03 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_reviews_new_review_score_bert'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='nlp_rank_bert',
            field=models.IntegerField(blank=True, db_column='NLP_rank_bert', null=True),
        ),
        migrations.AddField(
            model_name='movies',
            name='nlp_score_bert',
            field=models.DecimalField(blank=True, db_column='NLP_score_bert', decimal_places=1, max_digits=2, null=True),
        ),
    ]