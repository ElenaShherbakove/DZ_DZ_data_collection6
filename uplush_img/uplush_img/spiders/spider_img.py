"""Создайте новый проект Scrapy. Дайте ему подходящее имя и убедитесь, что ваше окружение правильно настроено для работы с проектом.
Создайте нового паука, способного перемещаться по сайту www.unsplash.com. 
Ваш паук должен уметь перемещаться по категориям фотографий и получать доступ к страницам отдельных фотографий.
Определите элемент (Item) в Scrapy, который будет представлять изображение. 
Ваш элемент должен включать такие детали, как URL изображения, название изображения и категорию, к которой оно принадлежит.
Используйте Scrapy ImagesPipeline для загрузки изображений. Обязательно установите параметр IMAGES_STORE в файле settings.py.
Убедитесь, что ваш паук правильно выдает элементы изображений, которые может обработать ImagesPipeline.
Сохраните дополнительные сведения об изображениях (название, категория) в CSV-файле. 
Каждая строка должна соответствовать одному изображению и содержать URL изображения, локальный путь к файлу (после загрузки), 
название и категорию."""



import scrapy


class UnsplashSpider(scrapy.Spider):
    name = "spider_img"
    # allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def parse(self, response):
        for image_page in response.xpath('//*[@itemprop="contentUrl"]/@href').extract():
            yield scrapy.Request(response.urljoin(image_page), self.parse_image_page)

    def parse_image_page(self, response):
        full_image_url = response.xpath('//*[@class="wdUrX"]/img[2]/@src').extract_first()
        if full_image_url:
            yield scrapy.Request(full_image_url, self.save_image)
            # print(full_image_url)

    def save_image(self, response):
        filename = response.url.split('/')[-1][0:20] + ".jpg"
        with open(f'images/{filename}', 'wb') as f:
            f.write(response.body)