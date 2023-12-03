import requests
from bs4 import BeautifulSoup
import psycopg2
import os
import dotenv
import re
import pandas as pd
from sqlalchemy import create_engine
dotenv.load_dotenv()

db = {
    "host": os.getenv("DBHOST"),
    "database": os.getenv("DBNAME"),
    "user": os.getenv("DBUSER"),
    "password": os.getenv("DBPWD"),
}

engine = create_engine(f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}/{db['database']}")

df_movies = pd.DataFrame(columns=["id_movie", "movie_title", "movie_rank", "movie_score_press", "movie_score_spectator"])
df_reviews = pd.DataFrame(columns=["review_score", "review_content", "id_movie"])

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
        
        title = title.text.strip()
        ranking = ranking.text.strip()
        presse_score = presse_score.text.strip()
        spectateurs_score = spectateurs_score.text.strip()
        
        presse_score = presse_score.replace(',', '.')
        spectateurs_score = spectateurs_score.replace(',', '.')
        

        print("titre:",title)
        print("rang:",ranking)
        
        df_movies.loc[len(df_movies)] = [id_film, title, ranking, presse_score, spectateurs_score]

        scrape_reviews(id_film)
        
    print("fin")


def scrape_reviews(id_movie):
    review_url = f"https://www.allocine.fr/film/fichefilm-{id_movie}/critiques/spectateurs/?page=1"
    
    first_page = requests.get(review_url)
    first_soup = BeautifulSoup(first_page.content, "html.parser")
    
    last_page_element = first_soup.find('your-last-page-element')

    last_page_element = first_soup.select('.pagination-item-holder span.item')[-1]

    if last_page_element:
        max_pages = int(last_page_element.text)
    else:
        max_pages = 10
    max_pages = 1
    print('total pages:',max_pages)
    
    for page_num in range(1, max_pages + 1):
        review_url = f"https://www.allocine.fr/film/fichefilm-{id_movie}/critiques/spectateurs/?page={page_num}"
        page = requests.get(review_url)
        soup = BeautifulSoup(page.content, "html.parser")
        reviews_list = soup.find_all('div', class_=['hred','review-card'])
        print('page num:',page_num)

        for review in reviews_list:
            score_element = review.find('span', class_='stareval-note')
            score = score_element.text.strip()

            content_element = review.find('div', class_='content-txt')
            content = content_element.text.strip()
            content = content.replace('spoiler:', '')
            content = ' '.join(content.split())
            score = score.replace(',', '.')
            
            df_reviews.loc[len(df_reviews)] = [score, content, id_movie]   

# with engine.connect() as connection:
#     connection.execute("TRUNCATE movies RESTART IDENTITY CASCADE")

pages = 2
for page_num in range(1, pages + 1):
    page_url = f"https://www.allocine.fr/film/meilleurs/?page={page_num}"
    scrape_movies_to_db(page_url)
    
print(len(df_movies))
print(len(df_reviews))
    
df_movies.to_sql('movies', engine, index=False, if_exists='append')
df_reviews.to_sql('reviews', engine, index=False, if_exists='append')
