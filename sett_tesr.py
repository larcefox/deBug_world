import configparser  # импортируем библиотеку
 
config = configparser.ConfigParser()  # создаём объекта парсера
config.read('settings.ini')  # читаем конфиг

for i in config["Bioms"]:
    print(config["Bioms"][i])