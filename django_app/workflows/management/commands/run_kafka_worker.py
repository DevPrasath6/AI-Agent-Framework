from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Run the local Kafka worker to process agent and workflow requests (dev only)"
    )

    def handle(self, *args, **options):
        from src.orchestrator.kafka_worker import run_kafka_worker

        self.stdout.write("Starting kafka worker (dev)...")
        run_kafka_worker()
