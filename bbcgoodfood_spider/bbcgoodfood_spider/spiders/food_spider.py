import scrapy

class GoodFoodSpider(scrapy.Spider):
    """
    The aim of this spider is to,
    Aim:
        - Extract all recipes from bbcgoodfood
        - Save all the information to a csv or senible format.
    How:
        - Crawl from the sitemap https://www.bbcgoodfood.com/wp-sitemap.xml
        - Identify all the recipe links
        - crawl through every recipe link and on each page locate all recipes
          and extract that information
        - Find the next page links and run over all pages of recipe lists.
        - save all the information. The information may potentially be too large for
          dicts so saving in batches might be necessary.
    Why:
        - So we can get all the recipe information for our website and are able to
          periodically update the information by running the spider.
    """

    name = "food_spider"

    start_urls = ["https://www.bbcgoodfood.com/wp-sitemap.xml"]
            
    def parse(self, response):
        y = {
            'url': [],
            'title': []
        }
        for meal in response.css('h4.heading-4.standard-card-new__display-title'):
            y['url'].append(meal.css("a::attr('href')").get())
            y['title'].append(meal.css('a::text').get())

        ingredient = response.url.replace("https://www.bbcgoodfood.com/search/recipes?q=", '')

        for i in range(len(y['url'])):
            yield scrapy.Request("https://www.bbcgoodfood.com" + y['url'][i], self.parse_meal,
                                 cb_kwargs=dict(title=y['title'][i], ingredient=ingredient))
            

    def parse_meal(self, response, title, ingredient):
        recipe = response.css("div.recipe-template__instructions li.pb-xxs.pt-xxs.list-item.list-item--separator ::text").getall()
        yield { "title": title,
                "ingredient": ingredient,
                "url": response.url,
                "recipe": recipe
        }
