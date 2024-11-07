import csv
from celery import shared_task
from .models import Dataset, ProcessedData

@shared_task(bind=True)
def process_dataset(self, dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)
    dataset.status = 'Processing'
    dataset.save()

    try:
        # Read and process the CSV file
        with open(dataset.file.path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # Save each row as encrypted processed data
                ProcessedData.objects.create(dataset=dataset, data=str(row))
                
        dataset.status = 'Completed'
    except Exception as e:
        dataset.status = 'Failed'
        dataset.error_message = str(e)
    finally:
        dataset.save()
