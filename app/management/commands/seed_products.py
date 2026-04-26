from __future__ import annotations
import random
from itertools import cycle
from django.core.management.base import BaseCommand
from app.models import product


class Command(BaseCommand):
    help = "Create demo plant products with fresh plant images."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=24, help="How many products to create")
        parser.add_argument(
            "--refresh-images",
            action="store_true",
            help="Update all existing products with the current image set instead of creating new rows",
        )

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

        # Fresh plant image URLs from Unsplash.
        plant_images = [
            "https://images.unsplash.com/photo-1506045412240-22980140a405?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1616189597001-9046fce2594d?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1483794344563-d27a8d18014e?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1509423350716-97f2360af21e?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1458530970867-aaa3700e966d?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1473448912268-2022ce9509d8?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1512428813834-c702c7702b78?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1524594154908-edd66554b2a5?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1506259091721-347e791bab0f?auto=format&fit=crop&w=1200&q=80",
        ]

        image_cycle = cycle(plant_images)

        if options["refresh_images"]:
            updated = 0
            for item in product.objects.all().order_by("id"):
                item.image_url = next(image_cycle)
                item.save(update_fields=["image_url"])
                updated += 1

            self.stdout.write(self.style.SUCCESS(f"Updated {updated} existing product image(s)."))
            return

        for i in range(count):
            name = f"{random.choice(adjectives)} {random.choice(nouns)}"
            price = random.choice([199, 249, 299, 349, 399, 499, 599, 699, 899, 999, 1199])
            stock = random.randint(5, 50)
            image_url = next(image_cycle)

            product.objects.create(
                name=name,
                description="Healthy, easy-care plant to brighten your space. Delivered fresh and ready to grow.",
                price=price,
                stock=stock,
                image_url=image_url,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} product(s)."))

