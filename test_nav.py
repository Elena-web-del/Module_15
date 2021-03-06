from seleniumbase import BaseCase

# Тесты изменены так, что тестировать текущую, на момент 10 июля 2020, версию сайта.

class NavigationTest(BaseCase):

    # задаем базовый урл и переменную-словарь
    def setup_class(self):
        self.base_url = "https://www.babyshop.com"
        self.menu_dict = {"Brands":['//a[@data-class="brand"]', self.base_url+"/brands/s/618"],
                     "Сlothing":['//a[@data-class="babyclothes"]', self.base_url+"/clothing/s/619"],
                     "Footwear":['//a[@data-class="babyshoes"]',self.base_url+"/footwear/s/620"]
            }

    def setup_language_region_select(self, language = "English", region = "Россия"):
        """ Функция выберает язык и регион, переходит на главную страницу и
        возвращает URL главной страницы."""
        # Необходимость данной функции в том, что бы тесты работали не смотря на то, в каком регионе находиться тестировщик.
        self.get(self.base_url)
        # Выбераем язык и регион в меню
        self.click('//*[@id="top-navigation-links"]/ul/li[1]/a')
        self.click(f'//a[@title="{language}"]')
        self.sleep(0.1)
        self.click(f'//a[@title="{region}"]')
        # Полуйаем базовый URL
        new_url = self.get_domain_url(self.get_current_url())
        # Переходим на главную страницу
        self.get(new_url)
        # Возвращаем новый URL для дальнейших действий
        return new_url


    # проверяем пункты меню
    def test_01_menu(self):
        self.get(self.setup_language_region_select())
        for item in self.menu_dict:
            print(f"Меню {item}")
            self.click(self.menu_dict[item][0])
            # получаем текущий урл в переменную curr_url
            curr_url = self.get_current_url()
            # проверка соответствия полученного и ожидаемого урл
            self.assert_equal(curr_url, self.menu_dict[item][1])

    def test_02_sub_menu(self):
        self.get(self.setup_language_region_select())
        #self.get(self.base_url)
        sub = '//a[@href="/boots-and-winter-shoes/s/673"]'
        #'//div[@class="babyshoes mid-navigation-container"]/div[@class="content c-16"]/div[@class="c-8"]/ul[2]/li[1]/a'
        # '//*[@id="mid-navigation"]/div[@class="babyshoes mid-navigation-container"]//div[@class="c-8"]/ul[2]/li[1]/a'
        #
        #'//*[@id="mid-navigation"]/div[9]/div/div[1]/ul[2]/li[1]/a'
        self.hover_and_click('//a[@data-class="babyshoes"]', sub)

    def test_03_find_items(self):
        self.get(self.setup_language_region_select())
        # send_keys - это печать текста в поле (отправка клавиш)
        self.send_keys('//*[@id="search-form"]/input', "Sirona S i-Size Car Seat")
        # клик на кнопке поиска
        self.click('//*[@id="search-form"]/button')
        # получаем  все элементы по заданному х-пазу и считаем длинну списка
        count = len(self.find_elements("//article"))
        self.sleep(5)
        # сверяем длину и ожидаемый результат
        self.assert_equal(count,5)
        # пример, как можно задать паузу
        self.sleep(2)

    def test_04_basket(self):
        # Идем на страницу товаров
        self.get(self.setup_language_region_select()+'/dolce-gabbana/s/1495')
        # сохраняем название первого товара страницы
        item_name = self.get_text('//article[3]/a/div[2]/p[2]')
        # эмулируем наведение мышкой и клик на кнопке "Add to cart"
        self.hover_and_click('//article[3]','//article[3]/a/div[1]/div/div[1]/p')
        # выбираем размер в выпадающем меню
        self.click('//*[@id="id-slct"]/div')
        self.click('//*[@id="id-slct"]/ul/li[2]')
        # эмулируем наведение мышкой и клик на кнопке "Add to cart"
        self.click('//*[@id="products"]/article[3]/div[1]/form/div/button/span[1]')
        # чуть ждем отработки скрипта
        self.sleep(0.1)
        # переходим к оплате
        self.click('//*[@id="products"]/article[3]/div[1]/form/div/a')
        # сохраняем название товара в корзине
        basket_name = self.get_text('//a[@class="product-name c-6"]/p[2]')
        # название выбранного товара и товара в корзине должно совпасть
        self.assert_equal(item_name,basket_name)
        # удаляем товар
        self.click('//a[@class="remove"]')
        #self.sleep(0.1)
        # Получаем сообщение, что корзина пуста
        empty_text = self.get_text('//div[@class="simple-page"]/h1')
        # проверяем его
        self.assert_equal(empty_text, "Your cart is empty")

    def test_05_change_region(self):
        self.get(self.setup_language_region_select()+'/dolce-gabbana/s/1495')
        # получаем английский текст
        eng_text = self.get_text('//*[@id="navigation"]/a[1]/span')
        # В связи с тем, что спецификация не ясна, то есть не ясно, должно ли название товара переводиться с английского на русский язык. Предлагаю проверять изменяется ли язык и одной из кнопок меню.
        # получаем цены товара
        price_before = self.get_text('//*[@id="products"]/article[1]/a/div[2]/p[3]/span[2]')
        # переход в раздел языковых параметров и их смена
        new_url = self.setup_language_region_select(language = "Russian", region = "USA")
        self.get(new_url + '/dolce-gabbana/s/1495')
        # получаем русский текст
        ru_text = self.get_text('//*[@id="navigation"]/a[1]/span')
        price_after = self.get_text('//*[@id="products"]/article[1]/a/div[2]/p[3]/span[2]')
        # английский текст не должен совпадать с русским
        self.assert_not_equal(eng_text, ru_text)
        # старая и новая цена не должны совпадать
        self.assert_not_equal(price_before, price_after)
