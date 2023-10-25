# ProductPriceChecker


Цель: Сайт для сравнения цен на товары между магазинами 
      и отслеживания динамики цен во времени.
	  
Миссия: Предоставить пользователям простой и удобный интерфейс
        для анализа динамики цен на рынке.



## Запуск проекта

За создание конфига отвечает файл env_variables.py, с поиощью него можно создать ```.env_json``` и конвертировать его в ```.env```

      python3 -m venv .venv
      source .venv/bin/activate

      pip install -r requirements.txt
      pip install Werkzeug==2.3.7 # Important

      export $(cat .env)
      python3 app.py
