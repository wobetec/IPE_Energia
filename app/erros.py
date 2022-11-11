from app import app
from app.helpers import apology

@app.errorhandler(404)
def page_not_found(e):
    return apology("notFound")