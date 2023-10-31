import requests
from bs4 import BeautifulSoup
    
def scrape_movies(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    films = soup.find_all(class_='mdl') 
    

    for film in films:
        ranking = film.find(class_="label-ranking")
        title = film.find(class_="meta-title-link")
        score_section = film.find(class_="rating-holder-3")
        presse_section = score_section.find('span', string=lambda text: "presse" in text.lower())
        spectateurs_section = score_section.find('a', string=lambda text: "spectateurs" in text.lower())
        presse_score = presse_section.find_next('span', class_='stareval-note')
        spectateurs_score = spectateurs_section.find_next('span', class_='stareval-note')
        ref_movie = 
        print("Presse:", presse_score.text.strip())
        print("Spectateurs:", spectateurs_score.text.strip())
        print("rang:",ranking.text.strip())
        print("titre:",title.text.strip())
        
# def scrape_reviews(url):
    


pages = 1

for page_num in range(1, pages + 1):
    page_url = f"https://www.allocine.fr/film/meilleurs/?page={page_num}"
    scrape_movies(page_url)
    




