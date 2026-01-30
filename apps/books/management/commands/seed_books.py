import random
import os
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from apps.books.models import Category, Author, Publisher, Book

class Command(BaseCommand):
    help = 'Seeds the database with fake categories, authors, publishers, and books'

    def handle(self, *args, **kwargs):
        fake = Faker(['az_AZ', 'en_US'])
        
        self.stdout.write('Seeding data...')

        # 1. Categories
        categories_data = [
            ('Bədii ədəbiyyat', 'fiction'),
            ('Dedektiv', 'detective'),
            ('Romantik', 'romance'),
            ('Elmi məşhur', 'science'),
            ('Biznes', 'business'),
            ('Uşaq ədəbiyyatı', 'children'),
            ('Klassiklər', 'classics'),
            ('Tarixi', 'history'),
        ]
        
        categories = []
        for name, slug in categories_data:
            cat, created = Category.objects.get_or_create(
                name=name,
                defaults={'slug': slug, 'description': fake.text(max_nb_chars=200)}
            )
            categories.append(cat)
        
        # Add some subcategories
        if categories:
            sub_cat, _ = Category.objects.get_or_create(
                name='Müasir Biznes',
                defaults={
                    'slug': 'modern-business', 
                    'parent': categories[4], # Biznes
                    'description': fake.text(max_nb_chars=100)
                }
            )
            categories.append(sub_cat)

        # 2. Publishers
        publishers = []
        for _ in range(5):
            name = fake.company()
            pub, _ = Publisher.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'website': fake.url(),
                }
            )
            publishers.append(pub)

        # 3. Authors
        authors = []
        for _ in range(10):
            name = fake.name()
            auth, _ = Author.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'bio': fake.text(max_nb_chars=500),
                    'nationality': fake.country(),
                }
            )
            authors.append(auth)

        # 4. Books
        formats = [Book.Format.HARDCOVER, Book.Format.PAPERBACK, Book.Format.EBOOK]
        languages = ['az', 'en', 'tr']
        
        # Get list of seed images
        seed_dir = os.path.join(settings.MEDIA_ROOT, 'seed')
        seed_images = [f for f in os.listdir(seed_dir) if f.endswith(('.png', '.jpg', '.jpeg'))] if os.path.exists(seed_dir) else []

        for i in range(25):
            title = fake.sentence(nb_words=random.randint(2, 5)).rstrip('.')
            price = random.uniform(5.0, 50.0)
            discount_price = price * 0.8 if random.random() > 0.7 else None
            
            book = Book.objects.create(
                title=title,
                slug=slugify(f"{title}-{random.randint(1000, 9999)}"),
                isbn=fake.isbn13().replace('-', ''),
                description=fake.paragraph(nb_sentences=5),
                publisher=random.choice(publishers),
                publication_date=fake.date_between(start_date='-10y', end_date='today'),
                language=random.choice(languages),
                pages=random.randint(100, 800),
                format=random.choice(formats),
                price=round(price, 2),
                discount_price=round(discount_price, 2) if discount_price else None,
                stock=random.randint(0, 50),
                is_active=True,
                is_featured=random.random() > 0.8,
                is_bestseller=random.random() > 0.9,
            )
            
            # Add random authors and categories
            book.authors.add(random.choice(authors))
            if random.random() > 0.7:
                book.authors.add(random.choice(authors))
                
            book.categories.add(random.choice(categories))
            if random.random() > 0.8:
                book.categories.add(random.choice(categories))

            # Assign a random seed image
            if seed_images:
                img_name = random.choice(seed_images)
                img_path = os.path.join(seed_dir, img_name)
                with open(img_path, 'rb') as f:
                    book.cover_image.save(img_name, File(f), save=True)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {Book.objects.count()} books!'))
