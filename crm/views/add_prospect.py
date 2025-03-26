from django.conf import settings
from django.http import HttpResponse
from django.contrib.gis.geoip2 import GeoIP2
from crm.models.lead import Lead
import os
from django.views.decorators.csrf import csrf_exempt


def check_bearer_token(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header:
        return False
        
    parts = auth_header.split()
    
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return False
        
    token = parts[1]
    env_token = os.environ.get('API_BEARER_TOKEN')
    
    if not env_token or token != env_token:
        return False
        
    return True


def get_country_and_city(ip, data):
    if not ip:
        return "No IP address provided"

    try:
        g = GeoIP2()
        city = g.city(ip)
        city_name = city.get('city')  # can be None
        country_name = city.get('country_name')  # can be None
        if city_name:
            from crm.models import City
            try:
                city_obj = City.objects.get(name=city_name)
                data['city'] = city_obj
            except City.DoesNotExist:
                city_obj = City.objects.create(name=city_name)
                data['city'] = city_obj

        if country_name:
            from crm.models import Country
            try:
                country_obj = Country.objects.get(name=country_name)
                data['country'] = country_obj
            except Country.DoesNotExist:
                if ip:
                    country_info = g.country(ip)
                    alt_country_name = country_info.get('country_name')
                    if alt_country_name:
                        try:
                            country_obj = Country.objects.get(name=alt_country_name)
                            data['country'] = country_obj
                        except Country.DoesNotExist:
                            country_obj = Country.objects.create(name=country_name)
                            data['country'] = country_obj
    except Exception as e:
        print(f"Error in geo lookup: {e}")
    
    return data


@csrf_exempt
def add_prospect(request):
    if request.method != "POST":
        return HttpResponse(status=405)  # 405 Method Not Allowed

    if not check_bearer_token(request):
        return HttpResponse(status=401)  # 401 Unauthorized

    email = request.POST.get("email")
    if not email:
        return HttpResponse(status=400)  # 400 Bad Request

    client_ip_address = request.POST.get('client_ip_address')
    data = {"email": email}

    if settings.GEOIP and client_ip_address:
        data = get_country_and_city(client_ip_address, data)
    if 'city' not in data or not data['city']:
        data.pop('city', None)

    lead, created = Lead.objects.get_or_create(
        email=email,
        defaults=data
    )
    return HttpResponse(status=201 if created else 200)  # 201 Created or 200 OK