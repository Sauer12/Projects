import random, string
from django.db import models

BASE62 = string.ascii_letters + string.digits

def generate_slug(length=6):
    # generuj unikátny slug (opakuj, kým nenájde voľný)
    while True:
        candidate = ''.join(random.choice(BASE62) for _ in range(length))
        if not Link.objects.filter(slug=candidate).exists():
            return candidate

class Link(models.Model):
    original_url = models.URLField(max_length=2048)
    slug = models.SlugField(max_length=32, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hits = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [models.Index(fields=["slug"])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug} -> {self.original_url}"
