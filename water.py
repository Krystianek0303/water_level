**Skrypt pobiera dane przez api i umieszcza je w bazie danych**                                                                                  
import requests
import datetime
import mysql.connector
import time

def main():
    # URL API
    url = "http://danepubliczne.imgw.pl/api/data/hydro/"  # Zmień na właściwy URL API

    # Pobierz dane z API
    response = requests.get(url)
    data = response.json()

    # Wybrane województwo
    selected_wojewodztwo = "podkarpackie"

    # Połączenie z bazą danych MySQL
    conn = mysql.connector.connect(
        host='adres',
        user='user',
        password='paswword',
        database='baza'
    )
    c = conn.cursor()

    # Utwórz tabelę, jeśli nie istnieje
    c.execute('''CREATE TABLE IF NOT EXISTS pomiary (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    id_stacji VARCHAR(20),
                    stacja VARCHAR(100),
                    rzeka VARCHAR(100),
                    wojewodztwo VARCHAR(50),
                    stan_wody FLOAT,
                    stan_wody_data_pomiaru DATETIME,
                    temperatura_wody FLOAT,
                    temperatura_wody_data_pomiaru DATETIME
                 )''')

    # Filtruj dane
    filtered_data = [entry for entry in data if entry['województwo'] == selected_wojewodztwo]

# Dodaj dane do bazy
    for entry in filtered_data:
        c.execute('''INSERT INTO pomiary (id_stacji, stacja, rzeka, wojewodztwo, stan_wody, stan_wody_data_pomiaru, temperatura_wody, temperatura_wody_data_pomiaru)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                  (entry['id_stacji'], entry['stacja'], entry['rzeka'], entry['województwo'], entry['stan_wody'], entry['stan_wody_data_pomiaru'],
                   entry['temperatura_wody'], entry['temperatura_wody_data_pomiaru']))

    # Zatwierdź zmiany
    conn.commit()

    # Zamknij połączenie
    conn.close()

    # Aktualna data i godzina
    current_date = datetime.datetime.now()
    print('Data i godzina pobrania danych:', current_date)


if __name__ == "__main__":
    while True:
        main()
        # Poczekaj 1 godzinę przed wykonaniem kolejnej iteracji
        time.sleep(10800)  # 3600 sekund to 1 godzina



