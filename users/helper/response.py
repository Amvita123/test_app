from rest_framework.response import Response
import datetime

def success_response(data=None, message="Success", status_code=200):
    return Response(
        {
            "success": True,
            "message": message,
            "data": data,
            "error": None
        }
        , status=status_code
    )

def error_response(data=None, message="Error", status_code=400):
    return Response(
        {
            "success": False,
            "message": message,
            "data": data,
            "error": None
        },
        status=status_code
    )

def create_unique_username(first_name, last_name):
    base_name = f"{first_name.lower()}{last_name.lower()}"
    time = datetime.datetime.now().strftime("%S")
    return f"{base_name}{time}"
