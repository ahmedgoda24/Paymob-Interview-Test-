import factory
from task1.models import Category, Product
from django.utils import timezone

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    
    name = factory.Sequence(lambda n: f"Category {n}")
    description = factory.Faker('sentence')

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    
    name = factory.Sequence(lambda n: f"Product {n}")
    category = factory.SubFactory(CategoryFactory)
    price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    created_at = factory.LazyFunction(timezone.now)
