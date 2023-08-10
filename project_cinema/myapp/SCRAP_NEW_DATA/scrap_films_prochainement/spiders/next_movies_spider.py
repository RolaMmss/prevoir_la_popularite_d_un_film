import scrapy
# from myapp.SCRAP_NEW_DATA.scrap_films_prochainement.items import ScrapFilmsProchainementItem
import re 
from datetime import datetime, timedelta
# from utils import convert_to_dd_mm_aaaa


def convert_to_dd_mm_aaaa(date_str):
    if date_str:
        try:
            # Set the locale manually for the script
            locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')
            date_obj = datetime.strptime(date_str, '%d %B %Y')
            formatted_date = date_obj.strftime('%Y-%m-%d')
            return formatted_date
        except ValueError:
            return None
    return None

class ScrapFilmsProchainementItem(scrapy.Item):
    titre = scrapy.Field()
    date = scrapy.Field()
    realisateur = scrapy.Field()
    duree = scrapy.Field()
    type_film = scrapy.Field()
    description = scrapy.Field()
    genre = scrapy.Field()
    acteurs = scrapy.Field()
    annee_production = scrapy.Field()
    langue_d_origine = scrapy.Field()
    nationalites = scrapy.Field()
    distributeur = scrapy.Field()
    film_id_allocine = scrapy.Field()
    image = scrapy.Field()
    

class BoxOfficeItem(scrapy.Item):
    film_id_allocine = scrapy.Field()
    boxoffice = scrapy.Field()

# Set the CSV file name and column order
CUSTOM_SETTINGS = {
    'CSV_OUTPUT_FILE': 'next_movies.csv',
    'CSV_FIELDS_TO_EXPORT': ['titre', 'date', 'genre', 'duree', 'realisateur', 'distributeur', 'acteurs',
                             'nationalites', 'langue_d_origine', 'type_film', 'annee_production', 
                             'recompenses', 'description', 'film_id_allocine'],  

    }


class NextMoviesSpider(scrapy.Spider):
    name = "next_movies_spider"
    allowed_domains = ["allocine.fr"]
    custom_settings = CUSTOM_SETTINGS

    allowed_domains = ["allocine.fr"]

    # URL de la première page
    base_url = 'https://www.allocine.fr/film/agenda'
    num_weeks = 2
    
    def start_requests(self):
        today = datetime.today()
        current_weekday = today.weekday()  # 0 (lundi) à 6 (dimanche)
        wednesday = today - timedelta(days=current_weekday - 2)  # Mercredi de cette semaine
        
        for week in range(self.num_weeks):
            week_str = wednesday.strftime('%Y-%m-%d')
            url = f"{self.base_url}/sem-{week_str}/"
            yield scrapy.Request(url, callback=self.parse)
            
            wednesday += timedelta(weeks=1)  # Incrémenter d'une semaine
            
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
        
        items = ScrapFilmsProchainementItem()
        
        titre = response.xpath('(//div[@class="titlebar titlebar-page"]//div[@class="titlebar-title titlebar-title-lg"]//text())').get() 
        date_dflt  = self.extract_date(response)
        if date_dflt is not None:
            date_dflt = date_dflt.strip()
            date = convert_to_dd_mm_aaaa(date_dflt)
        realisateur = response.css('span.light + span.blue-link::text').get()
        distributeur = response.xpath('//span[contains(text(), "Distributeur")]/following-sibling::span/text()').get()
        acteurs = response.css('div.meta-body-item.meta-body-actor span:not(.light)::text').getall()
        duree =  response.xpath('//div[@class="meta-body-item meta-body-info"]/span[@class="spacer"]/following-sibling::text()[1]').get()
        genre = response.css('div.meta-body-item.meta-body-info span::text').getall()
        nationalites = response.xpath('//span[contains(@class, "nationality")]/text()').get()
        type_film = response.xpath('//span[@class="what light" and contains(text(), "Type de film")]/following-sibling::span[@class="that"]/text()').get()
        langue_d_origine = response.xpath('//span[@class="what light" and contains(text(), "Langues")]/following-sibling::span[@class="that"]/text()').get()
        annee_production = response.xpath('//span[@class="what light" and contains(text(), "Année de production")]/following-sibling::span[@class="that"]/text()').get()
        description = response.xpath('//div[@class="content-txt "]//text()').get()
        image_url = response.css('img.thumbnail-img::attr(src)').get()
 

        
        #Extraire le "film_id" à partir de l'URL en utilisant une expression régulière
        film_id_match = re.search(r'cfilm=(\d+)', response.url)
        if film_id_match:
            film_id = film_id_match.group(1)

        items['film_id_allocine'] = film_id if film_id else None
    
        items['image'] = image_url if image_url else None
            
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
        items['distributeur'] = distributeur if distributeur else None
        items['description'] = description if description else None


        yield items



        

    



        

    

