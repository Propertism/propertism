import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from communications.models import CommunicationRetry
from communications.dispatcher import CommunicationDispatcher
from communications.services import DeliveryService

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Processes pending retries from the CommunicationRetry queue."

    def handle(self, *args, **options):
        now = timezone.now()
        pending_retries = CommunicationRetry.objects.select_related('delivery').filter(
            status='pending',
            scheduled_time__lte=now
        )

        total_retries = pending_retries.count()
        if total_retries == 0:
            self.stdout.write(self.style.SUCCESS("No pending communication retries in the queue."))
            return

        self.stdout.write(f"Found {total_retries} pending retries to process...")

        for retry in pending_retries:
            delivery = retry.delivery
            self.stdout.write(f"Processing retry for delivery: {delivery.tracking_reference} (Attempt {retry.attempt_number})")
            
            # Mark retry as processed (avoid double-processing)
            retry.status = 'success'
            retry.save()

            try:
                # Dispatch again synchronously (or async depending on preference, sync is better for CLI runner)
                CommunicationDispatcher.dispatch(delivery.id)
                self.stdout.write(self.style.SUCCESS(f"Finished processing retry for: {delivery.tracking_reference}"))
            except Exception as e:
                retry.status = 'failed'
                retry.save()
                self.stdout.write(self.style.ERROR(f"Failed to process retry for: {delivery.tracking_reference}. Error: {e}"))
                
        self.stdout.write(self.style.SUCCESS("Finished processing communication retry queue."))
