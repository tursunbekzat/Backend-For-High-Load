import os
import time
import django
from django.db import connections

# Указываем путь к файлу настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kvstore.settings')
django.setup()

def measure_read_time(db_alias, query="SELECT * FROM store_keyvalue LIMIT 1000;"):
    """
    Измеряет время выполнения запроса на чтение из указанной базы данных.
    """
    start_time = time.time()
    try:
        with connections[db_alias].cursor() as cursor:
            cursor.execute(query)
            cursor.fetchall()
    except Exception as e:
        print(f"Ошибка при чтении из базы данных '{db_alias}': {e}")
        return None
    return time.time() - start_time

def run_benchmark():
    """
    Выполняет тест производительности чтения для основной базы данных и реплики.
    """
    primary_time = measure_read_time('default')
    if primary_time is not None:
        print(f"Время выполнения чтения на основной базе данных: {primary_time:.2f} сек.")
    else:
        print("Ошибка при чтении с основной базы данных.")

    replica_time = measure_read_time('replica')
    if replica_time is not None:
        print(f"Время выполнения чтения на реплике: {replica_time:.2f} сек.")
    else:
        print("Ошибка при чтении с реплики.")

    # Выводим ускорение только если оба времени доступны
    if primary_time and replica_time:
        print(f"Ускорение за счет использования реплики: {primary_time / replica_time:.2f} раз.")

if __name__ == "__main__":
    run_benchmark()
