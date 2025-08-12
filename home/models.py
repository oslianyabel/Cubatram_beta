from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class Destination(models.Model):
    """Modelo para los destinos turísticos (ej: Havana, Varadero Beach)"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    para1 = models.TextField(blank=True)
    para2 = models.TextField(blank=True)
    para3 = models.TextField(blank=True)
    image = models.ImageField(upload_to="destinations/")
    map_image = models.ImageField(upload_to="destinations/", null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=20)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    """Modelo para categorías de excursiones (ej: Adventure Tours, Popular Destinations)"""

    title = models.CharField(max_length=100, blank=True)
    destination = models.ManyToManyField(Destination, related_name="categories")
    slug = models.SlugField(max_length=100, unique=True)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


class Tour(models.Model):
    """Modelo principal para las excursiones"""

    supplier = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    destinations = models.ManyToManyField(Destination, related_name="tours")
    categories = models.ManyToManyField(Category, related_name="tours")
    title = models.CharField(max_length=200)
    pricing_type = models.CharField(max_length=200, default="Per Person")
    adult_price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )
    adult_price_2 = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True, help_text="2 adults price"
    )
    adult_price_3 = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True, help_text="3 adults price"
    )
    adult_price_4 = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True, help_text="4 adults price"
    )
    kids_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="6-12 years",
    )
    children_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="0-5 years",
    )
    min_participants = models.PositiveIntegerField(default=1)
    max_participants = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    available_days = models.CharField(max_length=200, default="Mon-Sunday")
    start_time = models.CharField(max_length=200)
    finish_time = models.CharField(max_length=200)
    duration = models.CharField(
        max_length=200, help_text="Duración del tour (ej: 4 horas, 1 día)"
    )
    min_notice = models.CharField(max_length=200, default="24 hrs")
    frequency = models.CharField(max_length=200, default="1 Times per day")
    payment = models.CharField(max_length=200, default="Kiosk")
    slug = models.SlugField(max_length=200, unique=True)
    main_image = models.ImageField(upload_to="tours/")
    image2 = models.ImageField(upload_to="tours/", null=True, blank=True)
    image3 = models.ImageField(upload_to="tours/", null=True, blank=True)
    image4 = models.ImageField(upload_to="tours/", null=True, blank=True)
    image5 = models.ImageField(upload_to="tours/", null=True, blank=True)
    link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="External link for reservations or more information",
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class HeroSection(models.Model):
    """Modelo para la sección hero de la página principal"""

    name = models.CharField(max_length=50)
    background_image = models.ImageField(upload_to="hero/")
    background_image2 = models.ImageField(upload_to="hero/", null=True, blank=True)
    background_image3 = models.ImageField(upload_to="hero/", null=True, blank=True)
    background_image4 = models.ImageField(upload_to="hero/", null=True, blank=True)
    background_image5 = models.ImageField(upload_to="hero/", null=True, blank=True)
    title1 = models.CharField(max_length=200)
    title2 = models.CharField(max_length=200)
    title3 = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"

    def __str__(self):
        return f"Hero Section #{self.display_order} {self.name}"


class InfoSection(models.Model):
    """Modelo para la sección de información de la página principal"""

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    content = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Info Section"
        verbose_name_plural = "Info Sections"

    def __str__(self):
        return self.title


class InfoPoint(models.Model):
    """Puntos de información dentro de la info section"""

    info_section = models.ForeignKey(
        InfoSection, on_delete=models.CASCADE, related_name="points"
    )
    icon = models.FileField(upload_to="info_point/", blank=True, null=True)
    content = models.TextField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"Info Point #{self.display_order}"


class Booking(models.Model):
    """Modelo para las reservas de tours"""

    tour = models.ForeignKey(Tour, on_delete=models.PROTECT, related_name="bookings")
    date = models.DateField()
    adults = models.PositiveIntegerField(default=1)
    kids = models.PositiveIntegerField(default=0)
    children = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    special_requests = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Reserva #{self.id} - {self.tour.title}"  # type: ignore

    def calculate_total_price(self):
        total = self.adults * self.tour.adult_price

        if self.tour.kids_price and self.kids > 0:
            total += self.kids * self.tour.kids_price

        if self.tour.children_price and self.children > 0:
            total += self.children * self.tour.children_price

        return total

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)


class ContactInfo(models.Model):
    """Información de contacto para el footer"""

    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return "Contact Information"


class SocialMediaLink(models.Model):
    """Redes sociales para el footer"""

    name = models.CharField(max_length=50)
    url = models.URLField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.name
