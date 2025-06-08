from django.core.management.base import BaseCommand
from task1.factories import CategoryFactory, ProductFactory

class Command(BaseCommand):
    help = 'Generates test data'

    def handle(self, *args, **options):
        # Create 5 categories with 20 products each
        for _ in range(5):
            category = CategoryFactory()
            ProductFactory.create_batch(20, category=category)
        
        self.stdout.write(self.style.SUCCESS('Successfully generated test data'))