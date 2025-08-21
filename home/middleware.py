import datetime
from django.shortcuts import redirect
from django.conf import settings

class LicenseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # fecha de inicio (puedes guardarla en la DB o settings)
        self.start_date = datetime.date(2025, 8, 15)
        self.days_limit = 30  # licencia de 30 días

    def __call__(self, request):
        today = datetime.date.today()
        days_used = (today - self.start_date).days
        days_left = self.days_limit - days_used

        # Guardar días restantes en request para las plantillas
        request.days_left = days_left

        if days_left < 0 and not request.path.startswith("/pago/"):
            return redirect("pago")  # redirigir a la vista de pago

        response = self.get_response(request)
        return response
