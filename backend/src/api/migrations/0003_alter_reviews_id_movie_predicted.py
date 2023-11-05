# Generated by Django 4.2.6 on 2023-11-04 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_movies_movie_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='id_movie',
            field=models.ForeignKey(db_column='id_movie', on_delete=django.db.models.deletion.CASCADE, to='api.movies'),
        ),
        migrations.CreateModel(
            name='Predicted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_score', models.DecimalField(decimal_places=1, max_digits=2)),
                ('predicted_score', models.DecimalField(decimal_places=1, max_digits=2)),
                ('polarity', models.IntegerField(max_length=2)),
                ('id_review', models.ForeignKey(db_column='id_review', on_delete=django.db.models.deletion.CASCADE, to='api.reviews')),
            ],
            options={
                'db_table': 'prections',
            },
        ),
    ]
