import allure
from jsonschema import validate
from core.settings.contracts import CREATE_BOOKING_DATA_SCHEME


@allure.feature("Проверка создания брони")
@allure.story("Проверка валидного создания брони")
def test_create_booking_valid(api_client, generate_random_booking_data):
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
