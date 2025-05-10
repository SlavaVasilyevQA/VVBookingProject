import requests
import os
from dotenv import load_dotenv
from jsonschema import validate
from core.settings.environmets import Environment
from core.clients.endpoints import Endpoints
from core.settings.config import Users, Timeouts
from core.settings.contracts import BOOKING_DATA_SCHEME
import allure

load_dotenv()


class APIClient:
    def __init__(self):
        environment_str = os.getenv("ENVIRONMENT")
        try:
            environment = Environment[environment_str]
        except KeyError:
            raise ValueError(f"Unsupported environment value: {environment_str}")

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv("TEST_BASE_URL")
        elif environment == Environment.PROD:
            return os.getenv("PROD_BASE_URL")
        else:
            raise ValueError(f"Unsupported environment: {environment}")

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.session.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.session.headers, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def ping(self):
        with allure.step("Пинг api-клиент"):
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT}"
            response = self.session.get(url)
            response.raise_for_status()

        with allure.step("Проверка статус кода"):
            assert response.status_code == 201, f"Ожидали статус код 201, но получили {response.status_code}"
        return response.status_code

    def auth(self):
        with allure.step("Получение аутентификации"):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT}"
            payload = {
                "username": Users.USERNAME,
                "password": Users.PASSWORD
            }
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, f"Ожидали статус код 200, но получили {response.status_code}"

        token = response.json().get("token")
        with allure.step("Обновление заголовка с авторизацией"):
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get_booking_by_id(self, id):
        with allure.step("Получение брони по ID"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{id}"
            response = self.session.get(url, headers=self.session.headers, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()
            response_json = response.json()

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, f"Ожидали статус код 200, но получили {response.status_code}"

        with allure.step("Валидация JSON-схемы"):
            validate(response_json, BOOKING_DATA_SCHEME)

        return response_json
