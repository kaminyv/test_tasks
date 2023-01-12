import json
from enum import Enum
from http import HTTPStatus
from requests import post, auth
from django.http import JsonResponse, HttpResponse
from asgiref.sync import sync_to_async
from .forms import EmployeeRequest


class EmployeeItem(Enum):
    ID = 'id'
    Name = 'name'
    Surname = 'last_name'
    Phone = 'phone'
    Photo = 'image_url'


@sync_to_async(thread_sensitive=False)
def employees(request):
    if request.method != 'GET':
        return JsonResponse(
            {'message': 'Incorrect method request'},
            status=HTTPStatus.BAD_REQUEST
        )

    if request.content_type != 'application/json':
        return JsonResponse(
            {'message': 'Invalid raw parametrs in body'},
            status=HTTPStatus.BAD_REQUEST
        )

    form = EmployeeRequest(json.loads(request.body))

    if not form.is_valid():
        return HttpResponse(
            content=form.errors.as_json(),
            content_type='application/json',
            status=HTTPStatus.BAD_REQUEST
        )

    data = {
        "Request_id": "e1477272-88d1-4acc-8e03-7008cdedc81e",
        "ClubId": form.data.get('clubid'),
        "Method": "GetSpecialistList",
        "Parameters": {
            "ServiceId": ""
        }
    }

    url = form.data.get('url')
    user_name = form.data.get('user')
    password = form.data.get('password')
    auth_base = auth.HTTPBasicAuth(user_name, password)

    response = post(url=url, auth=auth_base, json=data)

    if response.status_code != 200:
        if request.content_type != 'application/json':
            return JsonResponse(
                {'message': 'Internal server error.'},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    convert_response = [
        {
            item.value:
                employee.get(item.name) if employee.get(item.name) else ''
            for item in EmployeeItem
        }
        for employee in response.json()['Parameters']
    ]

    return JsonResponse(convert_response, safe=False, status=HTTPStatus.OK)
