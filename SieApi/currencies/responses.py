from .errors import  *

common_response = {200: {
            'type': 'object',
            'properties': {
                'refresh': {
                    'bmx': 'object',
                },
            },
            'example': {
                "bmx": {
                    "series": [
                        {
                            "idSerie": "SF43718",
                            "titulo": "Tipo de cambio Pesos por dólar E.U.A. Tipo de cambio para solventar obligaciones denominadas en moneda extranjera Fecha de determinación (FIX)",
                            "datos": [
                                {
                                    "fecha": "02/01/2020",
                                    "dato": "18.8817"
                                }
                            ]
                        }
                    ]
                }
            },
        },
            400: {
                'type': 'object',
                'properties': {
                    'password': {
                        'type': 'string',
                    },
                    'email': {
                        'type': 'email',
                    },
                },
                'example': [
                    invalid_currency,
                    invalid_currency,
                    banxico_invalid_request
                ]
            },
        }