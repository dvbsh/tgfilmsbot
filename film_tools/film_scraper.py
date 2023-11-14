import requests
from bs4 import BeautifulSoup


async def get_filminfo(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    page = requests.get(url, headers=headers).text

    soup = BeautifulSoup(page, 'html.parser')

    all_data = soup.find('div', class_='redesign_schema')
    scores = soup.find_all('div', class_='wrapper_movies_scores_score')
    img = f'https://www.film.ru/{(soup.find("a", class_="wrapper_block_stack wrapper_movies_poster")).find("img")["src"]}'
    title = soup.find('div', class_='wrapper_movies_top_main_right').find('h1')
    duration_raw = all_data.find(itemprop="duration").get("content")[2:]
    duration_str = f'{duration_raw[:duration_raw.find("H")]} ч. {duration_raw[duration_raw.find("H") + 1:duration_raw.find("M")]} мин.'


    data = {
        'name': f'{all_data.find(itemprop="name").get("content")} / {all_data.find(itemprop="alternateName").get("content")}',
        'image': img,
        'genre': all_data.find(itemprop="genre").get("content"),
        'country': all_data.find(itemprop="countryOfOrigin").get("content"),
        'year': all_data.find(itemprop="dateCreated").get("content"),
        'desc': all_data.find(itemprop="description").get("content"),
        'duration': duration_str, 
        'score': scores[1].text[:4].strip()
    }

    return data