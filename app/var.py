ACCESS_LEVEL = {
    0: "The OneAboveAll",
    1: "Admin", 
    2: "Subordinado",
}

DEFAULT_APOLOGY = {
    "missing": {
        "message" : "Missing something",
        "code": 400
    },
    "unauthorized":{
        "message" : "You don't have permission to this",
        "code": 401
    },
    "forbidden":{
        "message" : "You don't have access to this",
        "code": 403
    },
    "notFound":{
        "message" : "Page not found",
        "code": 404
    },

}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

UPLOAD_FOLDER = "app/static/images/brasoes/"


# Variáveis de energia
GRUPOS_TARIFARIOS = {
    'A':{
        "MODALIDADE_CONTRATADA":{
            "Azul":{
                "DEMANDA_CONTRATADA":{ # Demanda Contratada 
                    1:"Úmida Ponta",
                    2:"Úmida Fora Ponta",
                    3:"Seca Ponta",
                    4:"Seca Fora Ponta",
                }
            },
            "Verde":{
                "DEMANDA_CONTRATADA":{
                    1:"Úmida",
                    2:"Seca"
                }
            },
        },
        "SUBGRUPO":{
            1:"A1",
            2:"A2",
            3:"A3",
            4:"A3a",
            5:"A4",
            6:"AS",
        }
    },
    'B':{
        "SUBGRUPO":{
            1:"B1",
            2:"B2",
            3:"B3",
            4:"B4",
        },
    }
}




