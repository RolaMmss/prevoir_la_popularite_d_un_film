import scrapy
from ..items import AllocineFilmsItem
import re 

# Set the CSV file name and column order
CUSTOM_SETTINGS = {
    'CSV_OUTPUT_FILE': 'movies_test.csv',
    'CSV_FIELDS_TO_EXPORT': ['titre', 'date', 'genre', 'duree', 'realisateur', 'distributeur', 'acteurs',
                             'nationalites', 'langue_d_origine', 'type_film', 'annee_production','nombre_article', 
                             'recompenses', 'description', 'film_id' ],  

    }

class FilmsSpider(scrapy.Spider):
    name = "films_spider"
    custom_settings = CUSTOM_SETTINGS

    allowed_domains = ["allocine.fr"]

    # URL de la première page
    base_url = 'https://www.allocine.fr/films'
    num_pages = 8000

    def start_requests(self):
        # Générer les URL de pagination
        for page in range(1, self.num_pages + 1):
            url = f"{self.base_url}/?page={page}"
            yield scrapy.Request(url, callback=self.parse)
            
    def parse(self, response):
        # Récupérer les titres de films sur la page actuelle
        titles = response.css("a.meta-title-link::text").getall()

        # Récupérer les liens des films sur la page actuelle
        film_links = response.css("a.meta-title-link::attr(href)").getall()

        # Combinaison des titres et des liens des films
        for title, film_link in zip(titles, film_links):
            # Suivre le lien du film pour accéder à la page du film
            yield response.follow(film_link, callback=self.parse_movie, meta={'title': title.strip()})
            
    # foncton pour scraper la date :
    def extract_date(self, response):
        # Essayer d'abord de trouver l'élément contenant la classe "date"
        date_element = response.xpath('//div[@class="meta-body-item meta-body-info"]//span[@class="date"]/text()').get()
        if date_element:
            return date_element.strip()
        # Si la première tentative échoue, essayer de trouver l'élément contenant la classe "xXx date blue-link"
        date_element = response.css('div.meta-body-item.meta-body-info span.date.blue-link::text').get()
        if date_element:
            return date_element.strip()
        # Si aucune date n'a été trouvée, renvoyer None ou une valeur par défaut
        return None

    def parse_movie(self, response):
        
        items = AllocineFilmsItem()
        
        titre = response.xpath('(//div[@class="titlebar titlebar-page"]//div[@class="titlebar-title titlebar-title-lg"]//text())').get() 
        date  = self.extract_date(response)
        realisateur = response.css('span.light + span.blue-link::text').get()
        distributeur = response.xpath('//span[contains(text(), "Distributeur")]/following-sibling::span/text()').get()
        acteurs = response.css('div.meta-body-item.meta-body-actor span:not(.light)::text').getall()
        duree =  response.xpath('//div[@class="meta-body-item meta-body-info"]/span[@class="spacer"]/following-sibling::text()[1]').get()
        genre = response.css('div.meta-body-item.meta-body-info span::text').getall()
        nationalites = response.xpath('//span[contains(@class, "nationality")]/text()').get()
        type_film = response.xpath('//span[@class="what light" and contains(text(), "Type de film")]/following-sibling::span[@class="that"]/text()').get()
        langue_d_origine = response.xpath('//span[@class="what light" and contains(text(), "Langues")]/following-sibling::span[@class="that"]/text()').get()
        recompenses = response.xpath('//span[@class="what light" and contains(text(), "Récompenses")]/following-sibling::span/text()').get()
        annee_production = response.xpath('//span[@class="what light" and contains(text(), "Année de production")]/following-sibling::span[@class="that"]/text()').get()
        nombre_article = response.xpath('(//section[@class="section ovw"]//a[@class="end-section-link "])[2]//text()').get()
        description = response.xpath('//div[@class="content-txt "]//text()').get()
 
        # Extraire le "film_id" à partir de l'URL en utilisant une expression régulière
        film_id = None
        film_id_match = re.search(r'cfilm=(\d+)', response.url)
        if film_id_match:
            film_id = film_id_match.group(1)

        # Ajouter le "film_id" à l'item
        items['film_id'] = film_id if film_id else None

            
        items['titre'] = titre if titre else None
        items['date'] = date if date else None
        items['duree'] = duree if duree else None
        items['type_film'] = type_film if type_film else None
        items['realisateur'] = realisateur if realisateur else None
        items['genre'] = genre if genre else None
        items['acteurs'] = acteurs if acteurs else None
        items['annee_production'] = annee_production if annee_production else None
        items['langue_d_origine'] = langue_d_origine if langue_d_origine else None
        items['nationalites'] = nationalites if nationalites else None
        items['nombre_article'] = nombre_article if nombre_article else None
        items['distributeur'] = distributeur if distributeur else None
        items['recompenses'] = recompenses if recompenses else None
        items['description'] = description if description else None


        yield items


        

    
