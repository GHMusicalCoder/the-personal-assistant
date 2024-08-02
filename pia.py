import os
import yaml
import fnmatch
import shutil
from datetime import datetime
from dateutil.relativedelta import relativedelta


def linux_magazine():
    for folder in settings["rename_folders"]:
        for file in os.listdir(settings['home_folder']+folder):
            if fnmatch.fnmatch(file.lower(), "lm_*.pdf"):
                rename_linux_magazine(settings['home_folder']+folder, file)


def rename_linux_magazine(folder, file):
    issue = int(file.split(".")[0].split("_")[1])
    months = issue - 282
    the_date = datetime(2024, 5, 1) + relativedelta(months=months)
    year = the_date.year
    month = the_date.strftime("%m")
    rename = f"{year}-{month}_Linux_Pro_Magazine_{issue}.pdf"
    shutil.move(f"{folder}/{file}", f"{settings['linux_magazine_location']}/{year}/{rename}")


def main():
    print("Processing Linux Magazine downloads")
    linux_magazine()


if __name__ == "__main__":
    # testing
    # rename_linux_magazine("", "LM_283.pdf")

    try:
        with open('settings.yaml', 'r') as f:
            settings = yaml.safe_load(f)
    except FileNotFoundError:
        print("Settings file not found.  Program can not run.")
        print("Please create a settings.yaml file for this program to use.")
        print("See GitHub documentation for further assistance.")
        exit()

    main()