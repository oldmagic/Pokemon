from bs4 import BeautifulSoup
import requests
import os
from tqdm import tqdm

src = requests.get('https://pokemondb.net/pokedex/national')
soup = BeautifulSoup(src.content, 'html.parser')
generations = soup.find_all('div', attrs={'class': 'infocard-list infocard-list-pkmn-lg'})
pk_name = soup.find_all('a', attrs={'class': 'ent-name'})

num_pokemons = sum(len(gen.find_all('div', attrs={'class': 'infocard'})) for gen in generations)

with tqdm(total=num_pokemons) as pbar:
    for generation in generations:
        pokemons = generation.find_all('div', attrs={'class': 'infocard'})

        for pokemon in pokemons:
            pokemon_name = pokemon.select("span.infocard-lg-data a.ent-name")[0].text
            img_tag = pokemon.select_one("span.infocard-lg-img a img.img-fixed.img-sprite")
            if img_tag:
                img_url = img_tag['src']
                img_content = requests.get(img_url).content
                with open(f'pokemons/{pokemon_name}.jpg', 'wb') as f:
                    f.write(img_content)
            else:
                print(f"No image found for {pokemon_name}")
                
            pbar.update(1)
