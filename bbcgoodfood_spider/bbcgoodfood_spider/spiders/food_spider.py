import scrapy
import json

class GoodFoodSpider(scrapy.Spider):
    """
    The aim of this spider is to,
    Aim:
        - Extract all recipes from bbcgoodfood
        - Save all the information to a csv or senible format.
    How:
        - sitemap bad we have a link to all recipes using the bbcgoodfood search function.
        - https://www.bbcgoodfood.com/search/recipes/page/1?sort=-date
        - The crawler will begin by extracting all the information of the first page and then
          simply go to the next page and repeat.
        - To save time when updating new recipes we could only add new recipes and ignore
          already added ones. This doesnt apply if existing recipes have been updated.
    Why:
        - So we can get all the recipe information for our website and are able to
          periodically update the information by running the spider.

    How do we want our data to look?
    title: ...
    url: ...
    image_url: ...
    cook_time: ...
    difficulty: ...
    vegiterian: ...
    vegan: ...


     
    """

    name = "food_spider"

    page = 1
    start_urls = ["https://www.bbcgoodfood.com/search/recipes/page/1?sort=-date"]
            
    def parse(self, response):
      
        recipe_links = response.css("h4.heading-4.standard-card-new__display-title a::attr('href')")
        yield from response.follow_all(recipe_links, self.parse_meal)
            
      
        self.page += 1
        pagination_link = "https://www.bbcgoodfood.com/search/recipes/page/%i/?sort=-date" % self.page
        yield scrapy.Request(pagination_link, self.parse)

    def parse_meal(self, response):
        title = response.css("div.masthead__body h1::text").get()
        recipe = response.css("div.recipe-template__instructions li.pb-xxs.pt-xxs.list-item.list-item--separator ::text").getall()
        tags = response.css("ul.term-icon-list.mb-xs.hidden-print.list.list--horizontal ::text").getall()
        rating = response.css("div.rating__values span.sr-only::text").get()
        num_of_rating = response.css("div.rating__values span.rating__count-text.body-copy-small ::text").get()
        try:
          prep_time = response.css("div.icon-with-text__children time::text")[0].get()
        except IndexError:
          prep_time = None

        try:
          cook_time = response.css("div.icon-with-text__children time::text")[1].get()
        except IndexError:
          cook_time = None

        serves = response.css("div.icon-with-text.masthead__servings.body-copy-small.body-copy-bold.icon-with-text--aligned div.icon-with-text__children ::text").get()
        yield { "title": title,
                "url": response.url,
                "recipe": recipe,
                "rating": rating,
                "num_of_rating": num_of_rating,
                "tags": tags,
                "prep_time": prep_time,
                "cook_time": cook_time,
                "serves": serves
        }
