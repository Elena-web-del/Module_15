from seleniumbase import BaseCase

class NavigationTest(BaseCase):

    # задаем базовый урл и переменную-словарь
    def setup_class(self):
        self.base_url = "https://www.babyshop.com"
        self.menu_dict = {"Brands":['//a[@data-class="brand"]', self.base_url+"/brands/s/618"],
                     "Сlothing":['//a[@data-class="babyclothes"]', self.base_url+"/clothing/s/619"],
                     "Footwear":['//a[@data-class="babyshoes"]',self.base_url+"/footwear/s/620"]
            }
    # def test_basket(self):
    #     # Идем на страницу товаров
    #     self.get(self.base_url+'/dolce-gabbana/s/1495')
    #     # выбор товара
    #     self.hover_and_click('//article[1]', '//article[1]//i[@class="quickshop-icon icon icon-cart-small"]')
    #
    #     self.click('//div[@id="id-slct"]')
    #     self.click('//div[@id="id-slct"]/ul/li[2]')
    #     #
    #
    #     self.click('//button[@class="add-to-cart green large"]')
    #     self.sleep(0.1)
    #     self.click('//a[@class="to-checkout white button"]')
    #     self.assert_equal("1", "1")
    # //*[@id="products"]/article[1]/a/div[2]/p[3]/span[2]

    def test_price_for_language_change(self):

        """ Изменение цены при изменении языка"""
        self.get(self.base_url+'/dolce-gabbana/s/1495')

        # Сохраняем цену до изменемия языка
        price_before = self.get_text('//*[@id="products"]/article[1]/a/div[2]/p[3]/span[2]')


        # Идем к выбору языка
        self.click('//*[@id="top-navigation-links"]/ul/li[1]/a')
        # //*[@id="top-navigation-links"]/ul/li[1]/a

        # Выбираем язык: Датский
        self.click('//*[@id="main"]/div[3]/div[1]/ul[1]/li[1]/a/span[2]')
        # //*[@id="main"]/div[3]/div[1]/ul[1]/li[1]/a/span[2]

        # Берем новый URL страницы
        new_url = self.get_domain_url(self.get_current_url())
        #
        # Открываем товары на странице с измененным азыком
        self.get(new_url+'/dolce-gabbana/s/1495')

        # Берем цену тогоже товара но на новом языке
        price_after = self.get_text('//*[@id="products"]/article[1]/a/div[2]/p[3]/span[2]')

        # старая и новая цена не должны совпадать
        self.assert_not_equal(price_before, price_after)
        self.assert_not_equal("3", "1")
