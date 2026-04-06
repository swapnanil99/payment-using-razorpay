from __future__ import annotations

import random

from django.core.management.base import BaseCommand

from app.models import product


class Command(BaseCommand):
    help = "Create demo plant products with plant images."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=24, help="How many products to create")

    def handle(self, *args, **options):
        count = int(options["count"])
        created = 0

        adjectives = ["Indoor", "Fresh", "Green", "Mini", "Premium", "Air-Purifying", "Low-Light", "Pet-Friendly"]
        nouns = [
            "Snake Plant",
            "Money Plant",
            "Peace Lily",
            "Aloe Vera",
            "Spider Plant",
            "Jade Plant",
            "ZZ Plant",
            "Areca Palm",
            "Bamboo Palm",
            "Rubber Plant",
            "Fiddle Leaf Fig",
            "Pothos",
        ]

        # Direct Unsplash image URLs (more reliable than source.unsplash.com redirects)
        plant_images = [
            "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1485955900006-10f4d324d411?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1512428813834-c702c7702b78?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1509423350716-97f2360af21e?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1520412099551-62b6bafeb5bb?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1524594154908-edd66554b2a5?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1444392061186-0e23080c612f?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1463320726281-696a485928c7?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1498842812179-c81beecf902c?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1506259091721-347e791bab0f?auto=format&fit=crop&w=1200&q=80",
        ]

        for i in range(count):
            name = f"{random.choice(adjectives)} {random.choice(nouns)}"
            price = random.choice([199, 249, 299, 349, 399, 499, 599, 699, 899, 999, 1199])
            stock = random.randint(5, 50)
            image_url = random.choice(plant_images)

            product.objects.create(
                name=name,
                description="Healthy, easy-care plant to brighten your space. Delivered fresh and ready to grow.",
                price=price,
                stock=stock,
                image_url=image_url,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} product(s)."))

