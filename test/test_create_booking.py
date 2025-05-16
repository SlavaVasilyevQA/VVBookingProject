import allure
from jsonschema import validate
from core.settings.contracts import CREATE_BOOKING_DATA_SCHEME
from pydantic import ValidationError
from core.model.booking import BookingResponse
import pytest
import requests


@allure.feature("Проверка создания брони")
@allure.story("Позитивный кейс: Проверка создания брони с фэйковыми данными")
def test_create_booking_with_fake_data(api_client, generate_random_booking_data):
    payload = generate_random_booking_data
    response = api_client.create_booking(payload)
    response_json = response.json()
    with allure.step("Проверка статус кода"):
        assert response.status_code == 200, f"Ожидали статус код 200, но получили {response.status_code}"
    with allure.step("Валидация JSON-схемы"):
        validate(response_json, CREATE_BOOKING_DATA_SCHEME)
    with allure.step("Проверка поля \"firstname\""):
        assert response_json["booking"]["firstname"] == payload["firstname"]
    with allure.step("Проверка поля \"lastname\""):
        assert response_json["booking"]["lastname"] == payload["lastname"]
    with allure.step("Проверка поля \"totalprice\""):
        assert response_json["booking"]["totalprice"] == payload["totalprice"]
    with allure.step("Проверка поля \"depositpaid\""):
        assert response_json["booking"]["depositpaid"] == payload["depositpaid"]
    with allure.step("Проверка поля \"checkin\""):
        assert response_json["booking"]["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"]
    with allure.step("Проверка поля \"checkout\""):
        assert response_json["booking"]["bookingdates"]["checkout"] == payload["bookingdates"]["checkout"]
    with allure.step("Проверка поля \"additionalneeds\""):
        assert response_json["booking"]["additionalneeds"] == payload["additionalneeds"]


@allure.feature("Проверка создания брони")
@allure.story("Позитивный кейс: Проверка создания брони с кастомными данными")
def test_create_booking_with_custom_data(api_client):
    payload = {
        "firstname": "Ivan",
        "lastname": "Ivanovich",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-05-10",
            "checkout": "2025-05-25"
        },
        "additionalneeds": "Dinner"
    }
    response = api_client.create_booking(payload)
    response_json = response.json()
    try:
        BookingResponse(**response_json)
    except ValidationError as e:
        raise ValidationError(f"Валидация провалилась: {e}")
    with allure.step("Проверка поля \"firstname\""):
        assert response_json["booking"]["firstname"] == payload["firstname"]
    with allure.step("Проверка поля \"lastname\""):
        assert response_json["booking"]["lastname"] == payload["lastname"]
    with allure.step("Проверка поля \"totalprice\""):
        assert response_json["booking"]["totalprice"] == payload["totalprice"]
    with allure.step("Проверка поля \"depositpaid\""):
        assert response_json["booking"]["depositpaid"] == payload["depositpaid"]
    with allure.step("Проверка поля \"checkin\""):
        assert response_json["booking"]["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"]
    with allure.step("Проверка поля \"checkout\""):
        assert response_json["booking"]["bookingdates"]["checkout"] == payload["bookingdates"]["checkout"]
    with allure.step("Проверка поля \"additionalneeds\""):
        assert response_json["booking"]["additionalneeds"] == payload["additionalneeds"]


@allure.feature("Проверка создания брони")
@allure.story("Негативный кейс: Проверка создания брони без поля lastname")
def test_create_booking_without_lastname(api_client):
    payload = {
        "firstname": "Ivan",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-05-10",
            "checkout": "2025-05-25"
        },
        "additionalneeds": "Dinner"
    }
    with allure.step("Используем контекстный менеджер для проверки ожидаемой ошибки"):
        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            response = api_client.create_booking(payload)
    with allure.step("Проверка статус кода"):
        assert exc_info.value.response.status_code == 500
    with allure.step("Проверка содержимого ответа"):
        assert exc_info.value.response.text == "Internal Server Error"
