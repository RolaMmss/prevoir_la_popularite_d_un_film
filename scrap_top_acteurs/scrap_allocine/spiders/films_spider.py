import scrapy
from ..items import AllocineFilmsItem
from ..utils import convert_to_minutes, convert_to_dd_mm_aaaa
from scrapy.settings import Settings

# Set the CSV file name and column order
CUSTOM_SETTINGS = {
    'CSV_OUTPUT_FILE': 'movies_tous.csv',
    'CSV_FIELDS_TO_EXPORT': ['titre', 'date', 'genre', 'durée', 'réalisateur', 'distributeur', 'acteurs', 'titre_original', 
                             'nationalités', 'langue_d_origine', 'type_film', 'annee_production', 'budget', 'box_office_total', 'note_presse', 
                             'note_spectateurs', 'nombre_article', 'recompenses', 'description' ],  
    'MONGODB_COLLECTION': 'movies_tous',

    }

class FilmsSpider(scrapy.Spider):
    name = "films_spider"
    custom_settings = CUSTOM_SETTINGS

    allowed_domains = ["allocine.fr"]

    # URL de la première page
    base_url = 'https://www.allocine.fr/films'
    num_pages = 550

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

    def parse_movie(self, response):
        
        items = AllocineFilmsItem()
        
        titre = response.xpath('(//div[@class="titlebar titlebar-page"]//div[@class="titlebar-title titlebar-title-lg"]//text())').get() 
        date_dflt = response.css('span.date.blue-link::text').get()
        if date_dflt is not None:
            date_dflt = date_dflt.strip()
        date = convert_to_dd_mm_aaaa(date_dflt)
        réalisateur = response.css('span.light + span.blue-link::text').get()
        distributeur = response.css('div.item span.that.blue-link::text').get()
        acteurs = response.css('div.meta-body-item.meta-body-actor span:not(.light)::text').getall()
        duree_dflt =  response.xpath('//div[@class="meta-body-item meta-body-info"]/span[@class="spacer"]/following-sibling::text()[1]').get()
        duree = convert_to_minutes(duree_dflt)
        genre = response.css('div.meta-body-item.meta-body-info span::text').getall()
        titre_original = response.xpath('//span[@class="light" and contains(text(), "Titre original")]/following-sibling::text()').get()
        nationalités = response.xpath('//span[@class="what light" and contains(text(), "Nationalités")]/following-sibling::span[@class="that"]//following-sibling::span/text()').getall()
        type_film = response.xpath('//span[@class="what light" and contains(text(), "Type de film")]/following-sibling::span[@class="that"]/text()').get()
        langue_d_origine = response.xpath('//span[@class="what light" and contains(text(), "Langues")]/following-sibling::span[@class="that"]/text()').get()
        budget = response.xpath('//span[@class="what light" and contains(text(), "Budget")]/following-sibling::span[@class="that"]/text()').get()
        recompenses = response.xpath('//span[@class="what light" and contains(text(), "Récompenses")]/following-sibling::span/text()').get()
        annee_production = response.xpath('//span[@class="what light" and contains(text(), "Année de production")]/following-sibling::span[@class="that"]/text()').get()
        note_presse = response.xpath('(//div[@class="rating-item-content"]//div[@class="stareval stareval-medium stareval-theme-default"]//span[@class="stareval-note"])[1]//text()').get()
        note_spectateurs = response.xpath('(//div[@class="rating-item-content"]//div[@class="stareval stareval-medium stareval-theme-default"]//span[@class="stareval-note"])[2]//text()').get()
        nombre_article = response.xpath('(//section[@class="section ovw"]//a[@class="end-section-link "])[2]//text()').get()
        description = response.xpath('//div[@class="content-txt "]//text()').get()
        box_office_total = response.xpath('//span[@class="what light" and contains(text(), "Box Office France")]/following-sibling::span/text()').get()
        
        
        if box_office_total:
            items['box_office_total'] = box_office_total.strip()
        else:
            items['box_office_total'] = None  # Ou une valeur par défaut si nécessaire
            
        items['titre'] = titre
        items['date'] = date if date else None

        if titre_original is not None:
            items['titre_original'] = titre_original.replace('\n', '').strip()
        else:
            items['titre_original'] = None 
            
        items['durée'] = duree

        if type_film:
            items['type_film'] = type_film.strip()
        else:
            items['type_film'] = None

        items['réalisateur'] = réalisateur
        
        items['genre'] = [genre.strip() for genre in genre[4:]]
        items['acteurs'] = acteurs
        if annee_production is not None:
            items['annee_production'] = annee_production.strip()
        else:
            items['annee_production'] = None 

        if langue_d_origine :
            items['langue_d_origine'] = langue_d_origine.strip()
        else:
            items['langue_d_origine'] = None

        if nationalités:
            items['nationalités'] = [nat.strip() for nat in nationalités]
        else:
            items['nationalités'] = None

        items['note_presse'] = note_presse 
        items['note_spectateurs'] = note_spectateurs
        items['nombre_article'] = nombre_article
        items['distributeur'] = distributeur

        # if boxofficefrtotal:
        #     items['boxofficefrtotal'] = boxofficefrtotal
        # else: items['boxofficefrtotal'] = None

        if budget is not None:
            items['budget'] = budget.strip()
        else:
            items['budget'] = None 
        
        if recompenses is not None:
            items['recompenses'] = recompenses.strip()
        else:
            items['recompenses'] = None  

        items['description'] = description.replace('\n', '').strip()

        yield items


        

    
