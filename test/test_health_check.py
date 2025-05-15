import allure
import pytest
import requests


@allure.feature("Проверка Пинг")
@allure.story("Проверка соединения")
def test_ping(api_client):
    status_code = api_client.ping()
    assert status_code == 201, f"Ожидали статус код 201, но получили {status_code}"


@allure.feature("Проверка Пинг")
@allure.story("Проверка недоступности сервера")
def test_ping_server_unavailable(api_client, mocker):
    mocker.patch.object(api_client.session, "get", side_effect=Exception("Сервер недоступен"))
    with pytest.raises(Exception, match="Сервер недоступен"):
        api_client.ping()


@allure.feature("Проверка Пинг")
@allure.story("Проверка неправильного HTTP метода")
def test_ping_wrong_method(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, "get", return_value=mock_response)
    with pytest.raises(AssertionError, match=f"Ожидали статус код 201, но получили 405"):
        api_client.ping()


@allure.feature("Проверка Пинг")
@allure.story("Проверка ошибки сервера")
def test_ping_internal_server_error(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, "get", return_value=mock_response)
    with pytest.raises(AssertionError, match=f"Ожидали статус код 201, но получили 500"):
        api_client.ping()


@allure.feature("Проверка Пинг")
@allure.story("Проверка неправильной страницы URL")
def test_ping_not_found(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, "get", return_value=mock_response)
    with pytest.raises(AssertionError, match=f"Ожидали статус код 201, но получили 404"):
        api_client.ping()


@allure.feature("Проверка Пинг")
@allure.story("Проверка успешного неправильного статус кода")
def test_ping_success_different_code(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mocker.patch.object(api_client.session, "get", return_value=mock_response)
    with pytest.raises(AssertionError, match=f"Ожидали статус код 201, но получили 200"):
        api_client.ping()


@allure.feature("Проверка Пинг")
@allure.story("Проверка таймаута")
def test_ping_timeout(api_client, mocker):
    mocker.patch.object(api_client.session, "get", side_effect=requests.Timeout)
    with pytest.raises(requests.Timeout):
        api_client.ping()
