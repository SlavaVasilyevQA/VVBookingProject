BOOKING_DATA_SCHEME = {
    "type": "object",
    "properties": {
        "firstname": {
            "type": "string"
        },
        "lastname": {
            "type": "string"
        },
        "totalprice": {
            "type": "integer"
        },
        "depositpaid": {
            "type": "boolean"
        },
        "bookingdates": {
            "type": "object",
            "properties": {
                "checkin": {
                    "type": "string"
                },
                "checkout": {
                    "type": "string"
                }
            },
            "required": ["checkin", "checkout"],
            "additionalProperties": False
        },
        "additionalneeds": {
            "type": "string"
        }
    },
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
    "additionalProperties": False
}

CREATE_BOOKING_DATA_SCHEME = {
    "type": "object",
    "properties": {
        "bookingid": {
            "type": "integer",
            "description": "Уникальный идентификатор бронирования"
        },
        "booking": {
            "type": "object",
            "properties": {
                "firstname": {
                    "type": "string",
                    "description": "Имя гостя"
                },
                "lastname": {
                    "type": "string",
                    "description": "Фамилия гостя"
                },
                "totalprice": {
                    "type": "integer",
                    "description": "Общая стоимость бронирования"
                },
                "depositpaid": {
                    "type": "boolean",
                    "description": "Оплачен ли депозит"
                },
                "bookingdates": {
                    "type": "object",
                    "properties": {
                        "checkin": {
                            "type": "string",
                            "description": "Дата заезда"
                        },
                        "checkout": {
                            "type": "string",
                            "description": "Дата выезда"
                        }
                    },
                    "required": ["checkin", "checkout"],
                    "description": "Даты бронирования"
                },
                "additionalneeds": {
                    "type": "string",
                    "description": "Дополнительные пожелания"
                }
            },
            "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates", "additionalneeds"],
            "description": "Информация о бронировании"
        }
    },
    "required": ["bookingid", "booking"],
    "additionalProperties": False,
    "description": "Схема данных бронирования"
}
