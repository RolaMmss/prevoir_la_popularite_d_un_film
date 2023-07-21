import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import AllocineMovieItem

class AllocineSpider(CrawlSpider):
    name = "allocine_spider"
    allowed_domains = ["allocine.fr"]

    # Spécifiez les colonnes pour le CSV
    fields = ['title', 'boxoffice']

    
    DEPTH_LIMIT = 5

    # Spécifiez les colonnes pour le CSV
    fields = ['title', 'boxoffice']
    # URL de la première page
    base_url = 'https://www.allocine.fr/films/decennie-2020/annee-2022'
    num_pages = 200

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
            yield response.follow(film_link, callback=self.parse_film, meta={'title': title.strip()})

    def parse_film(self, response):
        # Extraire le titre du film à partir des informations stockées dans la méta
        title = response.meta['title']
        # Extraire le numéro du film à partir de l'URL
        film_id = response.url.split("cfilm=")[-1].split(".html")[0]
        # Construire l'URL du box office
        box_office_url = f"https://www.allocine.fr/film/fichefilm-{film_id}/box-office/"
        # Suivre le lien du box office pour accéder à la page du box office
        yield scrapy.Request(box_office_url, callback=self.parse_box_office, meta={'title': title})

    def parse_box_office(self, response):
        # Extraire le box office fr de la première semaine
        box_office = response.css("td[data-heading='Entrées']::text").get()

        allocine_movies_items = AllocineMovieItem()
        allocine_movies_items['title'] = response.meta['title']
        allocine_movies_items['boxoffice'] = box_office.strip() if box_office else None

        yield allocine_movies_items
    

