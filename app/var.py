ACCESS_LEVEL = {
    1: "Master", 
    2: "Full + subordinados", 
    3: "Full", 
    4: "Inserir dados"
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
