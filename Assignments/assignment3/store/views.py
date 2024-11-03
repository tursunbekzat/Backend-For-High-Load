import random, logging
from rest_framework import generics, status
from rest_framework.response import Response
from .models import KeyValue
from .serializers import KeyValueSerializer
from django.http import JsonResponse
from .models import KeyValue
from django.db import connections

# INSTANCES = [
#     "http://localhost:8000",
#     "http://localhost:8001",
#     "http://localhost:8002"
# ]

# Simulate multiple nodes for quorum logic
NODES = 3  # Number of nodes

def quorum_reached(successes, total_nodes=NODES):
    """Check if quorum is achieved."""
    return successes >= (total_nodes // 2) + 1

# For real Django Instances
# def write_to_nodes(key, value):
#     successes = 0
#     for instance in INSTANCES:
#         try:
#             response = requests.post(
#                 f"{instance}/api/kv/",
#                 json={"key": key, "value": value}
#             )
#             if response.status_code == 201:
#                 successes += 1
#         except requests.exceptions.RequestException as e:
#             print(f"Failed to write to {instance}: {e}")
#     return successes


def write_to_nodes(key, value):
    """Simulate writing to multiple nodes."""
    successes = 0
    for node in range(NODES):
        if random.choice([True, False]):  # Simulate success/failure
            kv, created = KeyValue.objects.update_or_create(
                key=key,
                defaults={'value': value}
            )
            successes += 1
            # logger.info(f"Node {node} - Write success")
        else:
            # logger.warning(f"Node {node} - Write failed")
            pass

    return successes

def read_from_nodes(key):
    """Simulate reading from multiple nodes."""
    values = []
    for node in range(NODES):
        try:
            kv = KeyValue.objects.get(key=key)
            values.append(kv.value)
            # logger.info(f"Node {node} - Read success: {kv.value}")
        except KeyValue.DoesNotExist:
            pass
            # logger.warning(f"Node {node} - Key not found")
    return values

class KeyValueCreate(generics.CreateAPIView):
    queryset = KeyValue.objects.all()
    serializer_class = KeyValueSerializer

    def post(self, request, *args, **kwargs):
        key = request.data.get('key')
        value = request.data.get('value')

        successes = write_to_nodes(key, value)

        if quorum_reached(successes):
            return Response({"message": "Key-value pair written successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Quorum not achieved"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class KeyValueRetrieve(generics.RetrieveAPIView):
    queryset = KeyValue.objects.all()
    serializer_class = KeyValueSerializer

    def get(self, request, *args, **kwargs):
        key = kwargs.get('key')
        values = read_from_nodes(key)

        if not values:
            return Response({"error": "Key not found"}, status=status.HTTP_404_NOT_FOUND)

        # Majority vote for the most common value
        most_common_value = max(set(values), key=values.count)
        if values.count(most_common_value) < quorum_reached(len(values)):
            return Response({"error": "Inconsistent data across nodes"}, status=status.HTTP_409_CONFLICT)

        return Response({"key": key, "value": most_common_value}, status=status.HTTP_200_OK)

class KeyValueList(generics.ListAPIView):
    queryset = KeyValue.objects.all()
    serializer_class = KeyValueSerializer


def write_to_primary(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        value = request.POST.get('value')
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("INSERT INTO store_keyvalue (key, value) VALUES (%s, %s);", (key, value))
                return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)

def read_from_replica(request):
    try:
        with connections['replica'].cursor() as cursor:
            cursor.execute("SELECT key, value FROM store_keyvalue;")
            rows = cursor.fetchall()
            return JsonResponse(rows, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Получаем экземпляр логера
logger = logging.getLogger('django')

def example_view(request):
    # Добавляем сообщение в лог
    logger.debug("Начало выполнения example_view")
    
    # Пример логирования при обращении к базе данных
    try:
        data = KeyValue.objects.all()
        logger.info("Успешно получены данные из базы")
    except Exception as e:
        logger.error(f"Ошибка при получении данных из базы: {e}")

    # Завершаем выполнение
    logger.debug("Завершение выполнения example_view")
    # Далее идет остальная логика вашего представления