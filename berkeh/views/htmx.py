import requests
from django.conf import settings
from django.shortcuts import render
from requests.exceptions import RequestException


def handle_api_error(request, e):
    """Centralized error handling for API requests"""
    context = {}

    if isinstance(e, requests.exceptions.Timeout):
        context["message"] = "سرور پاسخگو نیست. لطفا دوباره تلاش کنید"
        status = 504
    elif isinstance(e, requests.exceptions.ConnectionError):
        context["message"] = "خطا در اتصال به سرور"
        status = 503
    else:
        context["message"] = "خطای سیستمی رخ داده است"
        status = 500

    if settings.DEBUG:
        context["debug"] = str(e)
        print(f"API Error: {str(e)}")

    return render(request, "error.html", context, status=status)


def berkeh_list(request):
    try:
        search_query = request.GET.get("search", "")
        response = requests.get(
            f"{settings.API_BASE_URL}/berkehs",
            params={"search": search_query},
            timeout=settings.HTTP_REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        berkehs = response.json()

        if settings.DEBUG:
            for b in berkehs:
                for p in b["photos"]:
                    p["image"] = p["image"].replace("https", "http")

        template = (
            "berkeh/partials/berkeh_list.html"
            if request.htmx
            else "berkeh/berkeh_list.html"
        )
        return render(request, template, {"berkehs": berkehs})

    except RequestException as e:
        return handle_api_error(request, e)


def berkeh_detail(request, berkeh_id):
    try:
        berkeh_resp, comments_resp = requests.get(
            f"{settings.API_BASE_URL}/berkehs/{berkeh_id}",
            timeout=settings.HTTP_REQUEST_TIMEOUT,
        ), requests.get(
            f"{settings.API_BASE_URL}/comments/by-berkeh",
            params={"berkeh_id": berkeh_id},
            timeout=settings.HTTP_REQUEST_TIMEOUT,
        )

        berkeh_resp.raise_for_status()
        comments_resp.raise_for_status()

        berkeh = berkeh_resp.json()
        comments = comments_resp.json()

        if settings.DEBUG:
            for p in berkeh["photos"]:
                p["image"] = p["image"].replace("https", "http")

        return render(
            request,
            "berkeh/berkeh_detail.html",
            {"berkeh": berkeh, "comments": comments},
        )

    except RequestException as e:
        return handle_api_error(request, e)
