import os
import bs4
import requests
from abc import ABC, abstractmethod


class ImageScrapper(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def scrape_images(self, search_item):
        pass


class ImagesFromGoogle(ImageScrapper):
    def __init__(self, base_url='https://www.google.com/search?q={search_item}&source=lnms&tbm=isch&sa=X&ved='
                                '2ahUKEwj55o_fnpf-AhV6yzgGHcsGBlQQ_AUoAnoECAEQBA&biw=1366&bih=649&dpr=1'):
        super().__init__()
        self.base_url = base_url

    def scrape_images(self, search_item):
        images_page = self.base_url.replace('{search_item}', search_item)
        response = requests.get(images_page)
        soup = bs4.BeautifulSoup(response.text, 'lxml')

        image_tags = soup.select('img')[1:]

        image_urls = []
        for image_tag in image_tags:
            image_url = image_tag['src']
            image_urls.append(image_url)

        return image_urls

    def save_images(self, search_item, save_dir='images/'):
        image_urls = self.scrape_images(search_item)

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        i = 1
        for image_url in image_urls:
            image_data = requests.get(image_url).content
            image_path = save_dir + f'{search_item}_{str(i)}' + '.jpg'
            with open(image_path, 'wb') as f:
                f.write(image_data)
            i += 1
