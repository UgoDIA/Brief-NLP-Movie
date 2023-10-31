import requests
from bs4 import BeautifulSoup
import psycopg2
import os
import dotenv
dotenv.load_dotenv()


def insert_into_database(id_film, title, ranking, presse_score, spectateurs_score):
    connection = psycopg2.connect(
        host=os.getenv("DBHOST"),
        database=os.getenv("DBNAME"),
        user=os.getenv("DBUSER"),
        password=os.getenv("DBPWD"),
    )

    presse_score = presse_score.replace(',', '.')
    spectateurs_score = spectateurs_score.replace(',', '.')

    cursor = connection.cursor()

    insert_query = "INSERT INTO movies (id_movie, movie_title, movie_rank, movie_score_press, movie_score_spectator) VALUES (%s, %s, %s, %s, %s);"

    cursor.execute(insert_query, (id_film, title, ranking,
                   presse_score, spectateurs_score))
    connection.commit()
    cursor.close()
    connection.close()


def scrape_movies_to_db(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    films = soup.find_all(class_='mdl')

    for film in films:
        ranking = film.find(class_="label-ranking")
        title = film.find(class_="meta-title-link")
        score_section = film.find(class_="rating-holder-3")
        presse_section = score_section.find(
            'span', string=lambda text: "presse" in text.lower())
        spectateurs_section = score_section.find(
            'a', string=lambda text: "spectateurs" in text.lower())
        presse_score = presse_section.find_next('span', class_='stareval-note')
        spectateurs_score = spectateurs_section.find_next(
            'span', class_='stareval-note')
        id_film = title['href'].split('_cfilm=')[1].split('.')[0]

        # print("note presse:", presse_score.text.strip())
        # print("note spectateurs:", spectateurs_score.text.strip())
        # print("rang:",ranking.text.strip())
        # print("titre:",title.text.strip())
        # print("id_film:",id_film)
        insert_into_database(id_film, title.text.strip(), ranking.text.strip(
        ), presse_score.text.strip(), spectateurs_score.text.strip())


pages = 2
for page_num in range(1, pages + 1):
    page_url = f"https://www.allocine.fr/film/meilleurs/?page={page_num}"
    scrape_movies_to_db(page_url)
