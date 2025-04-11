import scrapy

class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['https://books.toscrape.com/catalogue/page-1.html']

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
    
            title = book.css('h3 a::attr(title)').extract()[0]
            price = book.css('.price_color::text').extract()[0]

            availability_list = book.css('.instock.availability::text').extract()
            availability = availability_list[-1].strip() if availability_list else 'N/A'

        
            rating_class = book.css('p.star-rating::attr(class)').extract()[0]
            rating = rating_class.split()[-1] if rating_class else 'No Rating'

            yield {
                'title': title,
                'price': price,
                'availability': availability,
                'rating': rating
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
