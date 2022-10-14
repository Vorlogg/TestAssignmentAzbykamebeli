import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import psycopg2


def parse(max):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }
    data = []
    for j in tqdm(range(1, max)):
        url = 'https://azbykamebeli.ru/catalog/0000057/?page=' + str(j)
        r = requests.get(url, timeout=20, headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser').find_all("div",
                                                                 class_="col-lg-3 col-md-4 col-sm-6 mb-3 fadeInUp")
            for tag in soup:
                name = tag.find("div", class_="item__title h4").text
                temp_art_av = tag.find("div", class_="d-flex justify-content-between").text
                temp_art_av = temp_art_av.split()
                artikul = temp_art_av[1]
                price = tag.find("a", class_="js-favorite")["data-price"]
                if tag.find("a", class_="store-price fake-link"):
                    price_without_discount = tag.find("a", class_="store-price fake-link").text
                    price_without_discount = str(price_without_discount).split()
                    price_without_discount = int(price_without_discount[0] + price_without_discount[1])
                else:
                    price_without_discount = price
                if len(temp_art_av) == 3:
                    availability = 1
                else:
                    availability = 2
                id = tag.find("a", class_="js-favorite")["data-id"]
                product = {"id": int(id), "name": name, "artikul": artikul, "price": int(price),
                           "price_without_discount": int(price_without_discount), "availability": availability}
                data.append(product)

    return data


if __name__ == '__main__':
    connection = psycopg2.connect(dbname='products', user='postgres',
                                  password='admin0', host='localhost')
    cursor = connection.cursor()
    data = parse(14)

    for i in data:
        insert_query = """ INSERT INTO public.sofas (
     name, artikul, price,price_without_discount, availability,sofa_id) VALUES (
     '{}'::character varying, '{}'::character varying, 
    '{}'::numeric, '{}'::numeric, '{}'::integer,'{}'::integer)""".format(i["name"], i["artikul"], i["price"],
                                                                         i["price_without_discount"], i["availability"],
                                                                         i["id"])

        cursor.execute(insert_query)
    connection.commit()

# Запросы на графики
# 1
# SELECT  price_without_discount, availability.availability
# FROM public.sofas  JOIN public.availability
# ON availability.availability_id = sofas.availability
# WHERE public.sofas.availability=2
# 2
# SELECT  artikul, AVG(price_without_discount) as price_avg FROM public.sofas
# GROUP BY artikul ORDER BY price_avg ASC LIMIT 10
# 3
# SELECT  COUNT(DISTINCT(sofa_id)), availability.availability
# FROM public.sofas  JOIN public.availability
# ON availability.availability_id = sofas.availability
# GROUP BY availability.availability
