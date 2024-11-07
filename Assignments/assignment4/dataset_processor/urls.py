from django.urls import path
from .views import DatasetUploadView, DatasetStatusView, DatasetStatusByIDView, UserDatasetsView, ProcessedDatasetsView

urlpatterns = [
    path('dataset/upload/', DatasetUploadView.as_view(), name='dataset-upload'),
    path('dataset/status/<int:pk>/', DatasetStatusView.as_view(), name='dataset-status'),
    path('dataset/status/id/<int:dataset_id>/', DatasetStatusByIDView.as_view(), name='dataset-status-by-id'),
    path('dataset/user/', UserDatasetsView.as_view(), name='user-datasets'),
    path('dataset/processed/', ProcessedDatasetsView.as_view(), name='processed-datasets'),
]
