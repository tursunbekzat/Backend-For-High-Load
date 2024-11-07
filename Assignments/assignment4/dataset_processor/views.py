from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dataset
from .serializers import DatasetSerializer, DatasetStatusSerializer
from .tasks import process_dataset

from django.core.cache import cache

class DatasetUploadView(generics.CreateAPIView):
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        dataset = serializer.save(user=self.request.user)
        # Trigger the Celery task for async processing
        process_dataset.delay(dataset.id)

class DatasetStatusView(generics.RetrieveAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
def get_dataset_status(dataset_id):
    status = cache.get(f'dataset_status_{dataset_id}')
    if not status:
        status = Dataset.objects.get(id=dataset_id).status
        cache.set(f'dataset_status_{dataset_id}', status, timeout=300)  # Cache for 5 minutes
    return status

def get_user_datasets(user):
    # This will fetch the user data along with each dataset in a single query
    return Dataset.objects.filter(user=user).select_related('user')

def get_datasets_with_processed_data():
    # This will fetch datasets and prefetch all related processed data in fewer queries
    return Dataset.objects.all().prefetch_related('processed_data')


class DatasetStatusByIDView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dataset_id):
        status = get_dataset_status(dataset_id)
        return Response({"dataset_id": dataset_id, "status": status})

class UserDatasetsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        datasets = get_user_datasets(request.user)
        serializer = DatasetStatusSerializer(datasets, many=True)
        return Response(serializer.data)

class ProcessedDatasetsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        datasets = get_datasets_with_processed_data()
        serializer = DatasetStatusSerializer(datasets, many=True)
        return Response(serializer.data)
