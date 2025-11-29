import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render

API_KEY = "4b26f4df5343070e0a06f2052adbc76c"


class WeatherAPI(APIView):
    def get(self, request):
        city = request.GET.get("city")

        if not city:
            return Response({"error": "City is required"}, status=400)

        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            res = requests.get(url, timeout=5)
            data = res.json()

            if data.get("cod") != 200:
                return Response({"error": "City not found"}, status=404)

            return Response({
                "city": city.title(),
                "temp": data["main"]["temp"],
                "condition": data["weather"][0]["main"]
            })

        except requests.exceptions.Timeout:
            return Response({"error": "Request timed out"}, status=408)

        except Exception as e:
            return Response({"error": "Something went wrong"}, status=500)


class OutfitAPI(APIView):
    def get(self, request):
        city = request.GET.get("city")

        if not city:
            return Response({"error": "City is required"}, status=400)

        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            res = requests.get(url, timeout=5)
            data = res.json()

            if data.get("cod") != 200:
                return Response({"error": "City not found"}, status=404)

            temp = data["main"]["temp"]
            condition = data["weather"][0]["main"].lower()

            if temp < 15:
                outfit = "🧥 Wear a warm jacket"
            elif "rain" in condition:
                outfit = "☔ Carry an umbrella"
            elif temp > 30:
                outfit = "🩳 Light cotton clothes recommended"
            else:
                outfit = "👕 Comfortable casual outfit"

            return Response({
                "city": city.title(),
                "temp": temp,
                "condition": condition,
                "outfit": outfit
            })

        except requests.exceptions.Timeout:
            return Response({"error": "Request timed out"}, status=408)

        except Exception as e:
            return Response({"error": "Something went wrong"}, status=500)


# -----------------------------
# Frontend pages calling REST API
# -----------------------------
def weather_page(request):
    data = None
    city = request.GET.get("city")
    if city:
        try:
            # Use requests.get to call your REST API
            api_response = requests.get(f"http://127.0.0.1:8000/api/weather/?city={city}")
            data = api_response.json()
        except:
            data = {"error": "Server error"}
    return render(request, "weather_page.html", {"data": data})


def outfit_check_page(request):
    data = None
    city = request.GET.get("city")
    if city:
        try:
            # Call the OutfitAPI
            api_response = requests.get(f"http://127.0.0.1:8000/api/outfit/?city={city}")
            data = api_response.json()
        except:
            data = {"error": "Server error"}
    return render(request, "outfit_check.html", {"data": data})
