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
       # durée = response.xpath('//div[@class="meta-body-item meta-body-direction"] [1]').get()
       
        réalisateur = response.css('span.light + span.blue-link::text').get()
        acteurs = response.css('div.meta-body-item.meta-body-actor span:not(.light)::text').getall()

        durée =  response.xpath('//div[@class="meta-body-item meta-body-info"]/span[@class="spacer"]/following-sibling::text()[1]').get()
        genre = response.xpath('//div[@class="meta-body-item meta-body-info"]//a[@class="xXx"]').get()
       # genre = response.xpath('//div[@class="meta-body-item meta-body-info"]/span[@class="spacer"]/following-sibling::text()[5]').getall()
        titre_original = 1
        nationnalités = response.xpath('(//div[@class="item"]//span[@class="that"])[1]//text()').getall()
        type_film = response.xpath('(//div[@class="item"]//span[@class="that"])[6]//text()').get()
        langue_d_origine = response.xpath('(//div[@class="item"]//span[@class="that"])[8]//text()').get()
        box_office_fr = response.css('div.item span.that.blue-link::text').get()
        desciption = response.xpath('//div[@class="content-txt "]//text()').get()
       






       # item['release_date'] = release_date.strip() if release_date else None
        # durée = response.xpath('(//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]/li)[3]//text()').get().strip('()')
        
        #date = response.xpath('(//div[@class="meta-body"]//div[@class="meta-body-item meta-body-info"]//a[@class="xXx date blue-link"])').get()
        
      #  date = response.xpath('(//div[@class="card entity-card entity-card-list cf entity-card-overview"]//div[@class="meta  "][1]//div[@class="meta-body"]//div[@class="meta-body-item meta-body-info"][1]//a[@class="xXx date blue-link"][1]  )').get()
        # score = response.xpath('//a[@class="ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-baseAlt ipc-btn--theme-baseAlt ipc-btn--on-textPrimary ipc-text-button sc-acdbf0f3-2 tBSnU"]//span[@class="ipc-btn__text"]//div[@class="sc-acdbf0f3-3 kpRihV"]//div[@class="sc-bde20123-2 gYgHoj"]//text()').get().strip('()')
        # nbr_votants = response.xpath('(//a[@class="ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-baseAlt ipc-btn--theme-baseAlt ipc-btn--on-textPrimary ipc-text-button sc-acdbf0f3-2 tBSnU"]//span[@class="ipc-btn__text"]//div[@class="sc-acdbf0f3-3 kpRihV"]//div[@class="sc-bde20123-3 bjjENQ"])//text()').get().strip('()')
        # genre = response.xpath('(//div[@class="ipc-chip-list--baseAlt ipc-chip-list"]//div[@class="ipc-chip-list__scroller"])//text()').extract()
        
       # acteurs = response.css('(class="meta-body-item meta-body-direction")').extract()
        # pays = response.xpath('(//ul[@class="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base"]//li[@class="ipc-metadata-list__item"]//div[@class="ipc-metadata-list-item__content-container"]//ul[@class="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base"]//li[@class="ipc-inline-list__item"]//a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"])[1]//text()').extract()
        # langue_d_origine = response.xpath('(//ul[@class="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base"]//li[@class="ipc-metadata-list__item"]//div[@class="ipc-metadata-list-item__content-container"]//ul[@class="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base"]//li[@class="ipc-inline-list__item"]//a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"])[4]//text()').extract()
        # budget = response.xpath('(//li[@class="ipc-metadata-list__item sc-6d4f3f8c-2 byhjlB"]//div[@class="ipc-metadata-list-item__content-container"]//li[@class="ipc-inline-list__item"]//span[@class="ipc-metadata-list-item__list-content-item"])[1]//text()').get()
        # Sociétés_de_production = response.xpath('(//li[@class="ipc-metadata-list__item ipc-metadata-list-item--link"]//div[@class="ipc-metadata-list-item__content-container"]//ul[@class="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base"]//li[@class="ipc-inline-list__item"]//a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"])[3]//text()').extract()       
        
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
        items['titre_original'] = titre_original
        items['durée'] = durée.strip()
        # items['score'] = score
        items['type_film'] = type_film
        # items['nbr_votants'] = nbr_votants
        items['réalisateur'] = réalisateur
        items['desciption'] = desciption.replace('\n', '').strip()
        items['genre'] = genre
        items['acteurs'] = acteurs
        items['box_office_fr'] = box_office_fr
       
        items['langue_d_origine'] = langue_d_origine.strip()

        cleaned_nationnalites = [nat.strip() for nat in nationnalités if nat.strip()]
        items['nationnalités'] = cleaned_nationnalites

        yield items


        

    
