import argparse

import os
import sys
import shutil


my_parser = argparse.ArgumentParser(description="comands to help in my development")


my_parser.add_argument("option", metavar="option", type=str, help="to do")


args = my_parser.parse_args()

option = args.option

if option == "migrate":
    print("Deleting...")
    try:
        os.remove("./database.db")
    except:
        pass
    try:
        shutil.rmtree("./flask_session")
    except:
        pass

    print("Building...")
    os.system("cat ./app/models/models.sql | sqlite3 database.db")
    print("Populating...")
    os.system("cat ./app/models/models_create.sql | sqlite3 database.db")
    print("Done!")

    sys.exit()
elif option == "debug":
    os.system("flask --app app --debug run")


