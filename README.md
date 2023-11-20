# ProductPriceChecker


Цель: Сайт для сравнения цен на товары между магазинами 
      и отслеживания динамики цен во времени.
	  
Миссия: Предоставить пользователям простой и удобный интерфейс
        для анализа динамики цен на рынке.



## Запуск проекта

#### Зависимости:

Все зависимые сервисы создаются с помощью docker-compose. Ниже приведены docker-compose.yml файлы.

**Нельзя использовать TAB в docker-compose.yml файлах**

**1) Основная база данных**

      # [PostgreSQL]
      version: '3.1'

      services:
        db:
          image: postgres
          restart: always
          environment:
                POSTGRES_PASSWORD: <PASS>
          ports:
                - 5432:5432
          volumes:
                - ./data:/var/lib/postgresql/data

        adminer: # Если необходим phpAdmin
          image: adminer
          restart: always
          ports:
                - 8081:8080

**2) Объектное хранилище**

      # [MinIO]
      version: '3.1'

      services:
        minio:
          image: minio/minio
          restart: always
          ports:
                - "9000:9000"
                - "9001:9001"
          volumes:
                - ./data:/data
                - ./keys:/keys
          environment:
                MINIO_ROOT_USER: minIO
                # MINIO_ROOT_PASSWORD: <PASS>
                MINIO_ROOT_USER_FILE: /keys/access_key
                MINIO_ROOT_PASSWORD_FILE: /keys/secret_key
          command: server --console-address ":9001" /data
  
**3) Кэширующая база данных**

      # [Redis]
      version: '3.1'
      services:
        redis:
          image: redis:alpine
          restart: always
          ports:
                - '6379:6379'
          command: redis-server --save 20 1 --loglevel warning --requirepass <PASS>
          volumes:
                - ./data:/data


За создание конфига отвечает файл env_variables.py, с поиощью него можно создать ```.env_json``` и конвертировать его в ```.env```

      python3 -m venv .venv
      source .venv/bin/activate

      pip install -r requirements.txt
      pip install Werkzeug==2.3.7 # Important

      export $(cat .env)
      python3 app.py

## API сервера предоставляющего данные о курсах валют и цен товаров

#### Получение цен товаров

* [POST] ```/shops/get```

Body:

      {
            shops: [
                  {
                        "id": 8
                        "name": "Citilink",
                        "url": "https://cit.com/product?id=3"},
                  {
                        "name": "Video-shoper",
                        "url": "https://vid.ru/product?id=5"
                  }
            ]
      }

Response:

      {
            "shops": [
                  {
                        "date": "2023-11-20",
                        "id": "8",
                        "name": "Чайник",
                        "price": "2499",
                        "shop": "Citilink"
                  },
                  {
                        "date": "2023-11-20",
                        "id": "-1",
                        "name": "Чайник",
                        "price": "5000",
                        "shop": "Video-shoper"
                  }
            ]
      }


#### Получение курсов валют

* [GET] ```/currency?codes=EUR,USD,KZT,GEL```

Response:

      [
            {
                  "code": "EUR",
                  "name": "Евро",
                  "number": "978",
                  "price": "96.7692"
            },
            {
                  "code": "USD",
                  "name": "Доллар США",
                  "number": "840",
                  "price": "89.1237"
            },
            {
                  "code": "KZT",
                  "name": "Казахстанских тенге",
                  "number": "398",
                  "price": "19.3097"
            },
            {
                  "code": "GEL",
                  "name": "Грузинский лари",
                  "number": "981",
                  "price": "32.9953"
            }
      ]


## База данных

```Base.metadata.create_all(bind=ENGINE)``` - для создания БД

```add_test_data()``` - добавление данных для тестирования сайта

```selection_of_db()``` - проверка, что тестовые данные записаны в БД

## Шаблонизатор Jinja

В файле ```jinja.py``` добавлены функции для заполнения информации в блоке ```system-info``` в файле ```templates/blocks/info.html```

## Представления

#### api.py

Методы из данного класса вызываются в JS функциях на стороне клиента для добавления/изменения/удаления данных

- [GET]  ```/products``` - получение всех продуктов
- [GET]  ```/product``` - получение информации о продукте
- [POST] ```/product``` - создание/изменение продукта
- [GET]  ```/delete_product``` - удаление продукта
- [POST] ```/add_comment``` - добавленние комментария
- [POST] ```/delete_comment``` - удаление комментария

#### files.py

Получение файлов из объектного хранилища (MinIO)

**Статичечкие файлы сайта**

- [GET] ```/img/<name>``` - получение изображения
- [GET] ```/fonts/<name>"``` - получение шрифта

**Файлы, которые загружают пользователи**

- [GET] ```/img/<path>/<name>``` - получение изображения продукта

#### proxy.py

Proxy между JS скриптам на frontend'е и сторонним api для получния цен товара и курсов валют

- [POST] ```/shops``` - получает цену товаров
- [GET]  ```/currencies``` - получает информацию о курсах валют

#### users.py

Отвечает за регистрацию, авторизацию, деаутентификацию пользователей

#### view.py

Отдает html страницы

- ```/``` - главная страница, на ней расположен список товаров
- ```/about``` -  страница о нас, содержит информацию о компании
- ```/product``` - страница товара, на ней содержатся графики изменения цен, описание и комментарии
- ```/add_product``` - страница для добавления товара, на ней содержатся поля для ввода и загрузки информации
- ```/edit_product``` - страница для редактирования товара
- ```/admin``` - страница, на которой функциональность предстоит реализовать. Функции, которые будут доступны: Редактирование пользователей, Изменение магазинов, Изменение валют


# Roadmap

Разделить проект на несколько частей:
- API получения цен товаров
- API получения курса валют
- Backend взаимодействует с БД
- Frontend - Angular

Данное разделение позволит пользователю загрузить web страницу 1 раз и стоваться на ней до окончания работы, это сделает сайт более отзывчивым.

Разделение API улучшит тестируемость кода и разделит ответственности.

