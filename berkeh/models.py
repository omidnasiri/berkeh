import uuid
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from .storage import MinioBerkehPhotosStorage


class Location(models.Model):
    country = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True, blank=True)
    village = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        parts = [self.country, self.province, self.county]
        if self.city:
            parts.append(self.city)
        if self.village:
            parts.append(self.village)
        if self.district:
            parts.append(self.district)
        return ", ".join(parts)

    def clean(self):
        if not any([self.city, self.village, self.district]):
            raise ValidationError(
                "At least one of city, village, or district must be provided."
            )
        if (
            Location.objects.filter(
                country=self.country,
                province=self.province,
                county=self.county,
                city=self.city,
                village=self.village,
                district=self.district,
            )
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                "A location with this combination of country, province, county, city, village, and district already exists."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Berkeh(models.Model):
    name = models.CharField(
        max_length=255, blank=True, null=True
    )  # Not every berkeh has a name
    description = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=20, unique=True)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="berkehs"
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    @staticmethod
    def generate_code(location: Location) -> str:
        """Generate an incrementing code based on the city inside Location"""
        location_slug = location.slug.upper()
        last_entry = Berkeh.objects.filter(location=location).order_by("-code").first()

        if last_entry and last_entry.code.startswith(location_slug):
            last_number = int(last_entry.code.split("-")[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"{location_slug}-{new_number:03d}"


def photo_name_generator(instance, filename):
    new_filename = (
        f"berkeh_{instance.berkeh.code}_{uuid.uuid4()}.{filename.split(".")[-1]}"
    )
    return new_filename


class BerkehPhoto(models.Model):
    berkeh = models.ForeignKey(Berkeh, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(
        upload_to=photo_name_generator, storage=MinioBerkehPhotosStorage()
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    berkeh = models.ForeignKey(
        Berkeh, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
