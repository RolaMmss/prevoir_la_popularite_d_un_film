import scrapy
from ..items import ScrapImdbItem


class ImdbSpiderSpider(scrapy.Spider):

    name = "spider_movies_250"
    allowed_domains = ["allocine.fr"]
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'

    def start_requests(self):
        yield scrapy.Request(url='https://www.allocine.fr/films/decennie-2020/annee-2022/', headers={
            'User-Agent': self.user_agent
        })


    def parse(self, response):
        # Sélectionnez tous les liens de films et suivez-les pour récupérer les informations de chaque film
        links = response.css('h2.meta-title a.meta-title-link::attr(href)').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_movie)



    def parse_movie(self, response):
        items = ScrapImdbItem()
        titre = response.xpath('(//div[@class="titlebar titlebar-page"]//div[@class="titlebar-title titlebar-title-lg"]//text())').get() 
        date = response.css('span.date.blue-link::text').get()
        réalisateur = response.css('span.light + span.blue-link::text').get()
        acteurs = response.css('div.meta-body-item.meta-body-actor span:not(.light)::text').getall()
        durée =  response.xpath('//div[@class="meta-body-item meta-body-info"]/span[@class="spacer"]/following-sibling::text()[1]').get()
        genre = response.css('div.meta-body-item.meta-body-info span::text').getall()
        titre_original = response.xpath('//span[@class="light" and contains(text(), "Titre original")]/following-sibling::text()').get()
        nationnalités = response.xpath('//span[@class="what light" and contains(text(), "Nationalités")]/following-sibling::span[@class="that"]//following-sibling::span/text()').getall()
        type_film = response.xpath('//span[@class="what light" and contains(text(), "Type de film")]/following-sibling::span[@class="that"]/text()').get()
        langue_d_origine = response.xpath('//span[@class="what light" and contains(text(), "Langues")]/following-sibling::span[@class="that"]/text()').get()
        budget = response.xpath('//span[@class="what light" and contains(text(), "Budget")]/following-sibling::span[@class="that"]/text()').get()
        recompenses = response.xpath('//span[@class="what light" and contains(text(), "Récompenses")]/following-sibling::span/text()').get()
        annee_production = response.xpath('//span[@class="what light" and contains(text(), "Année de production")]/following-sibling::span[@class="that"]/text()').get()
        note_presse = response.xpath('(//div[@class="rating-item-content"]//div[@class="stareval stareval-medium stareval-theme-default"]//span[@class="stareval-note"])[1]//text()').get()
        note_spectateurs = response.xpath('(//div[@class="rating-item-content"]//div[@class="stareval stareval-medium stareval-theme-default"]//span[@class="stareval-note"])[2]//text()').get()
        nombre_article = response.xpath('(//section[@class="section ovw"]//a[@class="end-section-link "])[2]//text()').get()
        description = response.xpath('//div[@class="content-txt "]//text()').get()

        def convertir_time(durée):
            if 'h' in durée and 'm' in durée:
                heure, minute = durée.split("h ")
                heure = int(heure)
                minute = int(minute.replace("m", ""))
            elif 'h' in durée:
                heure = int(durée.replace("h", ""))
                minute = 0
            elif 'm' in durée:
                heure = 0
                minute = int(durée.replace("m", ""))
            else:
                raise ValueError()
            duree_minutes = heure * 60 + minute
            return duree_minutes
    
     
        items['titre'] = titre
        items['date'] = date.strip() if date else None

        if titre_original is not None:
            items['titre_original'] = titre_original.replace('\n', '').strip()
        else:
            items['titre_original'] = None 

        items['durée'] = durée.strip()

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

        if nationnalités:
            items['nationnalités'] = [nat.strip() for nat in nationnalités]
        else:
            items['nationnalités'] = None

        items['note_presse'] = note_presse 
        items['note_spectateurs'] = note_spectateurs
        items['nombre_article'] = nombre_article

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


        

    
