import click
import requests
import sqlite3
import json
import logging

# konfiguracja modułu logging do śledzenia komunikatów
logging.basicConfig(level=logging.INFO)

api_url = 'http://127.0.0.1:5000/events'
database_name = 'events.db'

# Utwórz tabelę events, jeśli nie istnieje
with sqlite3.connect(database_name) as connection:
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_data TEXT
        )
    ''')
    connection.commit()


@click.command()
@click.option('--continuous', is_flag=True, help='Enable continuous mode')
@click.option('--save-to-db', is_flag=True, help='Save events to SQLite database')
@click.option('--filter', help='Filter events based on a specific criterion')
def collector(continuous, save_to_db, filter):
    """Remote Event Collector CLI"""
    logging.info(f'Connecting to {api_url}...')

    try:
        if continuous:
            while True:
                response = requests.get(api_url)
                events = response.json()
                for event in events:
                    if not filter or filter in event['name']:  # Dodaj warunek filtru
                        click.echo(event)
                        if save_to_db:
                            save_event_to_db(json.dumps(event))

        elif filter:
            # Pobieranie zdarzeń z bazy danych SQLite na podstawie kryterium filtru
            events = fetch_events_from_db(filter)
            for event in events:
                click.echo(event)

        else:
            response = requests.get(api_url)
            events = response.json()
            for event in events:
                if not filter or filter in event['name']:  # Dodaj warunek filtru
                    click.echo(event)
                    if save_to_db:
                        save_event_to_db(json.dumps(event))

    except requests.RequestException as e:
        logging.error(f'Error connecting to API: {e}')

    except sqlite3.Error as e:
        logging.error(f'SQLite error: {e}')


# Funkcja pobierająca zdarzenia z bazy danych SQLite na podstawie filtru
def fetch_events_from_db(filter):
    with sqlite3.connect(database_name) as connection:
        cursor = connection.cursor()
        query = f"SELECT event_data FROM events WHERE event_data LIKE ? AND event_data LIKE ?"  # Dodaj warunek filtru
        cursor.execute(query, (f"%{filter}%", f"%{filter}%"))
        events = cursor.fetchall()
    return [json.loads(event[0]) for event in events]


def save_event_to_db(event):
    try:
        with sqlite3.connect(database_name) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO events (event_data) VALUES (?)", (event,))
            connection.commit()
    except sqlite3.Error as e:
        logging.error(f'SQLite error: {e}')


if __name__ == '__main__':
    collector()
