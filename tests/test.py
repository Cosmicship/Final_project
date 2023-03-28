#python3 -m pytest -v --driver Chrome --driver-path C:\Users\Enot\PycharmProjects\finalproject_module28\chromedriver.exe test.py
import pytest
import selenium
import urllib3
from pagesRT.auth_page import AuthPage
from pagesRT.locators import AuthLocators
from pagesRT.registr_page import RegistrPage
from config.settings import *

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


s = Service(r"C:\Users\Enot\PycharmProjects\finalproject_module28\chromedriver.exe")
driver = webdriver.Chrome(service=s)
chromeOptions = webdriver.ChromeOptions()
chromeOptions.binary_location = r"C:\Users\Enot\PycharmProjects\finalproject_module28\chromedriver.exe"
driver.maximize_window()


def test_authform_elements(selenium):
    #EXP-001 Проверка, что в форме авторизации присутствуют необходимые элементы

    page = AuthPage(selenium)

    assert page.email.text in page.card_of_auth.text
    assert page.pass_eml.text in page.card_of_auth.text
    assert page.btn_enter.text in page.card_of_auth.text
    assert page.forgot_password_link.text in page.card_of_auth.text
    assert page.register_link.text in page.card_of_auth.text


def test_authform_tubs(selenium):
    #EXP-002 Проверка, что в форме авторизации присутствуют все табы способов авторизации

    try:
        page = AuthPage(selenium)
        menu = [page.tub_phone.text, page.tub_email.text, page.tub_login.text, page.tub_ls.text]
        for i in range(len(menu)):
            assert "Номер" in menu
            assert 'Почта' in menu
            assert 'Логин' in menu
            assert 'Лицевой счёт' in menu
    except AssertionError:
        print('Ошибка в имени вкладки способа авторизации')


def test_default_auth_type(selenium):
    #EXP-003 Проверка, что по умолчанию выбрана авторизация по номеру телефона.
    page = AuthPage(selenium)

    assert page.active_tub_phone.text == Settings.menu_type_auth[0]


def test_auth_placeholder_name_swap(selenium):
    #EXP-004 Проверка, что при смене способа авторизации таб меняется автоматически
    page = AuthPage(selenium)
    page.tub_phone.click()

    assert page.placeholder_name.text in Settings.placeholder_name
    page.tub_email.click()
    assert page.placeholder_name.text in Settings.placeholder_name
    page.tub_login.click()
    assert page.placeholder_name.text in Settings.placeholder_name
    page.tub_ls.click()
    assert page.placeholder_name.text in Settings.placeholder_name


def test_auth_email_valid_data(selenium):
    #EXP-008 Базовый позитивный тест авторизации с валидным email и паролем
    page = AuthPage(selenium)
    page.email.send_keys(Settings.valid_email)
    page.email.clear()
    page.pass_eml.send_keys(Settings.valid_password)
    page.pass_eml.clear()
    page.btn_enter.click()

    try:
        assert page.get_relative_link() == '/account_b2c/page'
    except AssertionError:
        assert 'Неверно введен текст с картинки' in page.find_other_element(*AuthLocators.error_message).text

@pytest.mark.parametrize("incor_email", [Settings.invalid_email, Settings.empty_email],
                         ids=['invalid_email', 'empty'])
@pytest.mark.parametrize("incor_passw", [Settings.invalid_password, Settings.empty_password],
                         ids=['invalid_password', 'empty'])

def test_auth_email_invalid_data(selenium, incor_email, incor_passw):
    #EXP-009 Проверка авторизации по email c некорректным паролем
    #EXP-011 Проверка авторизации по email c некорректным email

    page = AuthPage(selenium)
    page.email.send_keys(incor_email)
    page.email.clear()
    page.pass_eml.send_keys(incor_passw)
    page.pass_eml.clear()
    page.btn_enter.click()

    assert page.get_relative_link() != '/account_b2c/page'


def test_forgot_password_link(selenium):
    #EXP-020 Проверка перехода на страницу восстановления пароля
    page = AuthPage(selenium)
    page.driver.execute_script("arguments[0].click();", page.forgot_password_link)

    assert page.find_other_element(*AuthLocators.password_recovery).text == 'Восстановление пароля'

def test_registration_link(selenium):
    #EXP-021 Проверка перехода на страницу регистрации
    page = AuthPage(selenium)
    page.register_link.click()

    assert page.find_other_element(*AuthLocators.registration).text == 'Регистрация'


def test_regform_elements(selenium):
    #EXP-027 Проверка, что на странице регистрации в форме ввода данных присутствуют необходимые элементы
    try:
        page_reg = RegistrPage(selenium)
        card_of_reg = [page_reg.first_name, page_reg.last_name, page_reg.address_registration,
                       page_reg.email_registration, page_reg.password_registration,
                       page_reg.password_registration_confirm, page_reg.registration_btn]
        for i in range(len(card_of_reg)):
            assert page_reg.first_name in card_of_reg
            assert page_reg.last_name in card_of_reg
            assert page_reg.email_registration in card_of_reg
            assert page_reg.address_registration in card_of_reg
            assert page_reg.password_registration in card_of_reg
            assert page_reg.password_registration_confirm in card_of_reg
            assert page_reg.registration_btn in card_of_reg
    except AssertionError:
        print("Элемент отсутствует в форме регистрации")


def test_regform_elements_names(selenium):
    #EXP-028 Проверка, что форма регистрации содержит все необходимые элементы с правильными названиями
    try:
        page_reg = RegistrPage(selenium)
        assert 'Имя' in page_reg.card_of_registration.text
        assert 'Фамилия' in page_reg.card_of_registration.text
        assert 'Регион' in page_reg.card_of_registration.text
        assert 'E-mail или мобильный телефон' in page_reg.card_of_registration.text
        assert 'Пароль' in page_reg.card_of_registration.text
        assert 'Подтверждение пароля' in page_reg.card_of_registration.text
        assert 'Зарегистрироваться' in page_reg.card_of_registration.text
    except AssertionError:
        print('Название элемента в форме регистрации некорректно')


def test_registration_valid_data(selenium):
    #EXP-029, EXP-031 Проверка регистрации с валидными данными "Имя" и "Фамилия", "Пароль"

    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(Settings.first_name)
    page_reg.first_name.clear()
    page_reg.last_name.send_keys(Settings.last_name)
    page_reg.last_name.clear()
    page_reg.email_registration.send_keys(Settings.valid_email_reg)
    page_reg.email_registration.clear()
    page_reg.password_registration.send_keys(Settings.valid_password)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.valid_password)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert page_reg.find_other_element(*AuthLocators.email_confirm).text == 'Подтверждение email'

def test_registration_not_unique_email(selenium):
    #EXP-036 Проверка, что нельзя зарегистрироваться с уже зарегистрированным email
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(Settings.first_name)
    page_reg.first_name.clear()
    page_reg.last_name.send_keys(Settings.last_name)
    page_reg.last_name.clear()
    page_reg.email_registration.send_keys(Settings.valid_email)
    page_reg.email_registration.clear()
    page_reg.password_registration.send_keys(Settings.valid_password)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.valid_password)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert "Учётная запись уже существует" in page_reg.find_other_element(*AuthLocators.error_account_exists).text


@pytest.mark.parametrize("valid_first_name",
                         [
                             (Settings.russian_generate_string) * 5
                             , (Settings.russian_generate_string) * 8
                             , (Settings.russian_generate_string) * 13
                             , (Settings.russian_generate_string) * 24
                             , (Settings.russian_generate_string) * 32
                         ],
                         ids=
                         [
                             'russ_symbols=5', 'russ_symbols=8', 'russ_symbols=13',
                             'russ_symbols=24', 'russ_symbols=32'
                         ])


def test_reg_first_name_by_valid_data(selenium, valid_first_name):
    #EXP-029 Проверка ввода валидного значения в поле ввода "Имя" формы регистрации.
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(valid_first_name)
    page_reg.first_name.clear()
    page_reg.registration_btn.click()

    assert 'Необходимо заполнить поле кириллицей. От 2 до 32 символов.' not in page_reg.container_first_name.text



def test_first_name_invalid_data(selenium, invalid_first_name):
    #EXP-030. Негативный тест. Проверка недопустимости некорректных значений в поле "Имя" формы "Регистрация":
    # пустые значения, кириллица в недопустимом количестве, латиница, иероглифы, спецсимволы, числа.
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(invalid_first_name)
    page_reg.first_name.clear()
    page_reg.registration_btn.click()

    assert 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.' in \
           page_reg.find_other_element(*AuthLocators.error_first_name).text

@pytest.mark.parametrize("invalid_first_name",
                         [
                             (Settings.russian_generate_string) * 1
                             , (Settings.russian_generate_string) * 100
                             , (Settings.russian_generate_string) * 257
                             , (Settings.empty), (Settings.numbers)
                             , (Settings.latin_generate_string)
                             , (Settings.chinese_chars), (Settings.special_chars)
                         ],
                         ids=
                         [
                             'russ_symbols=1', 'russ_symbols=100', 'russ_symbols=257',
                             'empty', 'numbers', 'latin_symbols', 'chinese_symbols', 'special_symbols'
                         ])
def test_reg_password_valid_data(selenium, valid_password):
    #EXP-033 Проверка валидности значения пароля в форме регистрации

    page_reg = RegistrPage(selenium)
    page_reg.password_registration.send_keys(valid_password)
    page_reg.password_registration.clear()
    page_reg.registration_btn.click()

    assert 'Длина пароля должна быть не менее 8 символов' and \
           'Длина пароля должна быть не более 20 символов' and \
           'Пароль должен содержать хотя бы одну заглавную букву' and \
           'Пароль должен содержать хотя бы одну прописную букву' and \
           'Пароль должен содержать хотя бы 1 спецсимвол или хотя бы одну цифру' not in page_reg.password_registration.text


def test_reg_confirm_password_valid_data(selenium):
    #EXP-034 Проверка, что в форме регистрации значения в поле "Пароль" и "Подтвердить пароль" совпадают

    page_reg = RegistrPage(selenium)
    page_reg.password_registration.send_keys(Settings.passw1)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.passw1)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert 'Пароли не совпадают' not in page_reg.container_password_confirm.text


def test_registration_confirm_password_invalid_data(selenium):
    #EXP-035 Негативный тест. Проверка обнаружения, что значения в форме "Пароль" и "Подтвердить пароль" не совпадают

    page_reg = RegistrPage(selenium)
    page_reg.password_registration.send_keys(Settings.passw1)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.passw2)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_btn.click()

    assert 'Пароли не совпадают' in page_reg.find_other_element(*AuthLocators.error_password_confirm).text

