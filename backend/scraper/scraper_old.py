import requests
from bs4 import BeautifulSoup
import psycopg2
import os
import dotenv
import re
from sqlalchemy import create_engine
dotenv.load_dotenv()


def insert_into_movies_table(id_film, title, ranking, presse_score, spectateurs_score):
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
        print("titre:",title.text.strip())
        print("rang:",ranking.text.strip())
        # print("id_film:",id_film)
        insert_into_movies_table(id_film, title.text.strip(), ranking.text.strip(
        ), presse_score.text.strip(), spectateurs_score.text.strip())
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
    max_pages = 10
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
            # content = re.sub(r'\s{2,}', ' ', content)
            content = ' '.join(content.split())
            # print(f"Score: {score}")
            # print(f"Content: {content}")
            

            insert_into_reviews_table(score, content, id_movie)



def insert_into_reviews_table(score, content, id_movie):
    connection = psycopg2.connect(
        host=os.getenv("DBHOST"),
        database=os.getenv("DBNAME"),
        user=os.getenv("DBUSER"),
        password=os.getenv("DBPWD"),
    )
    score = score.replace(',', '.')

    cursor = connection.cursor()

    insert_query = "INSERT INTO reviews ( review_score, review_content,id_movie) VALUES (%s, %s, %s);"

    cursor.execute(insert_query, (score, content, id_movie))
    connection.commit()
    cursor.close()
    connection.close()
    

pages = 2
for page_num in range(1, pages + 1):
    page_url = f"https://www.allocine.fr/film/meilleurs/?page={page_num}"
    scrape_movies_to_db(page_url)
    
