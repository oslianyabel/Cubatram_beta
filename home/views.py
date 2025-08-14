import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render

from .models import Booking, Category, ContactInfo, Destination, HeroSection, Tour, NavBar
from .notifications import send_admin_notification


def tour_detail(request, destination_slug, category_slug, tour_slug):
    tour = get_object_or_404(Tour, slug=tour_slug, is_active=True)
    categories = Category.objects.filter(is_active=True)
    destinations = Destination.objects.filter(is_active=True)
    destination_selected = get_object_or_404(
        Destination, slug=destination_slug, is_active=True
    )
    category_selected = get_object_or_404(Category, slug=category_slug, is_active=True)
    hero_section = HeroSection.objects.filter(is_active=True).first()
    navbar = NavBar.objects.filter(is_active=True).first()

    recaptcha_error = None
    if request.method == "POST":
        date = request.POST.get("date")
        adults = int(request.POST.get("adults", 1))
        kids = int(request.POST.get("kids", 0))
        children = int(request.POST.get("children", 0))
        pickup = request.POST.get("pickup")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        country = request.POST.get("country")
        comments = request.POST.get("comments", "")

        # Validar reCAPTCHA
        recaptcha_response = request.POST.get("g-recaptcha-response")
        recaptcha_secret = settings.RECAPTCHA_PRIVATE_KEY
        recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"
        recaptcha_data = {
            "secret": recaptcha_secret,
            "response": recaptcha_response,
            "remoteip": request.META.get("REMOTE_ADDR"),
        }
        recaptcha_result = requests.post(recaptcha_url, data=recaptcha_data).json()
        if not recaptcha_result.get("success"):
            recaptcha_error = "Please verify that you are not a robot"
        else:
            # Calcular el precio total
            total_price = float(adults * tour.adult_price)
            if tour.kids_price and kids > 0:
                total_price += float(kids * tour.kids_price)
            if tour.children_price and children > 0:
                total_price += float(children * tour.children_price)

            # Aplicar descuentos por grupo si están disponibles
            if adults >= 4 and tour.adult_price_4:
                total_price = (
                    float(adults * tour.adult_price_4)
                    + float(kids * (tour.kids_price or 0))
                    + float(children * (tour.children_price or 0))
                )
            elif adults >= 3 and tour.adult_price_3:
                total_price = (
                    float(adults * tour.adult_price_3)
                    + float(kids * (tour.kids_price or 0))
                    + float(children * (tour.children_price or 0))
                )
            elif adults >= 2 and tour.adult_price_2:
                total_price = (
                    float(adults * tour.adult_price_2)
                    + float(kids * (tour.kids_price or 0))
                    + float(children * (tour.children_price or 0))
                )

            # Crear la reserva
            booking = Booking.objects.create(
                tour=tour,
                date=date,
                adults=adults,
                kids=kids,
                children=children,
                location=pickup,
                full_name=name,
                email=email,
                phone=phone,
                country=country,
                special_requests=comments,
                total_price=total_price,
            )

            # Guardar los datos del formulario en la sesión
            request.session["form_data"] = {
                "date": date,
                "adults": adults,
                "kids": kids,
                "children": children,
                "pickup": pickup,
                "name": name,
                "email": email,
                "phone": phone,
                "country": country,
                "comments": comments,
                "total_price": total_price,
            }

            try:
                send_admin_notification(booking)
            except Exception as e:
                print(f"Error enviando notificaciones: {e}")

            messages.success(
                request, "Your booking request has been submitted successfully."
            )
            return redirect('home')

    # Obtener datos del formulario de la sesión si existen
    form_data = request.session.pop("form_data", None)

    context = {
        "tour": tour,
        "categories": categories,
        "destinations": destinations,
        "destination_selected": destination_selected,
        "category_selected": category_selected,
        "hero_section": hero_section,
        "navbar": navbar,
        "form_data": form_data,
        "recaptcha_site_key": settings.RECAPTCHA_PUBLIC_KEY,
        "recaptcha_error": recaptcha_error,
    }
    return render(request, "home/tour_detail.html", context)


def home(request):
    hero_section = HeroSection.objects.filter(is_active=True).first()
    navbar = NavBar.objects.filter(is_active=True).first()

    categories = Category.objects.filter(is_active=True)
    destinations = Destination.objects.filter(is_active=True)
    featured_destinations = Destination.objects.filter(
        is_active=True, is_featured=True
    )[:3]

    featured_tours = Tour.objects.filter(is_featured=True, is_active=True)[:3]

    contact_info = ContactInfo.objects.first()

    context = {
        "hero_section": hero_section,
        "navbar": navbar,
        "categories": categories,
        "destinations": destinations,
        "featured_destinations": featured_destinations,
        "featured_tours": featured_tours,
        "contact_info": contact_info,
    }
    return render(request, "home/home.html", context)


def destination_selected(request, slug):
    destination_selected = get_object_or_404(Destination, slug=slug, is_active=True)

    hero_section = HeroSection.objects.filter(is_active=True).first()
    navbar = NavBar.objects.filter(is_active=True).first()

    categories = destination_selected.categories.all()  # type: ignore
    destinations = Destination.objects.filter(is_active=True)

    featured_tours = Tour.objects.filter(is_featured=True, is_active=True)[:3]

    contact_info = ContactInfo.objects.first()

    context = {
        "destination_selected": destination_selected,
        "hero_section": hero_section,
        "navbar": navbar,
        "categories": categories,
        "destinations": destinations,
        "featured_tours": featured_tours,
        "contact_info": contact_info,
    }
    return render(request, "home/select_category.html", context)


def tour_list(request, destination_slug, category_slug):
    destination_selected = get_object_or_404(
        Destination, slug=destination_slug, is_active=True
    )
    category_selected = get_object_or_404(Category, slug=category_slug, is_active=True)

    tours = Tour.objects.filter(
        categories=category_selected, destinations=destination_selected, is_active=True
    )

    categories = Category.objects.filter(is_active=True)
    destinations = Destination.objects.filter(is_active=True)
    hero_section = HeroSection.objects.filter(is_active=True).first()
    navbar = NavBar.objects.filter(is_active=True).first()
    contact_info = ContactInfo.objects.first()

    context = {
        "destination_selected": destination_selected,
        "category_selected": category_selected,
        "tours": tours,
        "categories": categories,
        "destinations": destinations,
        "hero_section": hero_section,
        "navbar": navbar,
        "contact_info": contact_info,
    }
    return render(request, "home/tour_list.html", context)
