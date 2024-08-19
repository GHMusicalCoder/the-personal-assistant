import os
import yaml
import fnmatch
import shutil
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
from urllib.request import urlopen

dcc_entries = []
dcc_dyingearth = []
dcc_horror = []
dcc_lankhmar = []
dcc_empire = []
dcc_exceptions = []
dcc_convention = []
month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
               'November', 'December']


def convert_month_name(month):
    return month_names.index(month) + 1


def validate_folder(new_folder):
    os.makedirs(new_folder, exist_ok=True)


def file_renaming():
    for folder in settings["rename_folders"]:
        for file in os.listdir(settings['home_folder']+folder):
            home = settings['home_folder']+folder
            if fnmatch.fnmatch(file.lower(), "lm_*.pdf"):
                print("Processing Linux Magazine downloads")
                rename_linux_magazine(home, file)

            if fnmatch.fnmatch(file.lower(), "dungeoncrawlclassics_*.pdf"):
                print("Processing DCC Magazine downloads")
                # rename_dcc_items(home, file)

            if fnmatch.fnmatch(file.lower(), "dungeoncrawlclassicshorror_*.pdf"):
                print("Processing DCC Horror Magazine downloads")
                # rename_dcchorror_items(home, file)

            if fnmatch.fnmatch(file.lower(), "*_photos.pdf") or fnmatch.fnmatch(file.lower(), "*_printerfriendly.pdf"):
                print("Processing Jaroudi Family Monthly Recipes...")
                rename_jaroudi_recipes(home, file)


def rename_jaroudi_recipes(folder, file):
    jaroudi = file.split('_')
    recipe_date = jaroudi[0][:-7]
    month = recipe_date[:-4]
    year = recipe_date[-4:]
    base_folder = settings['jaroudi_location']
    new_folder = f"{year}/{year}-{str(convert_month_name(month)).zfill(2)} {month[:3]}"
    new_location = f"{base_folder}/{new_folder}/{file}"
    validate_folder(f"{base_folder}/{new_folder}")
    shutil.move(f"{folder}/{file}", new_location)


def rename_dcchorror_items(folder, file):
    if len(dcc_horror) == 0:
        build_dcc_magazines()
    pass


def build_dcc_magazines():
    global dcc_entries, dcc_horror, dcc_dyingearth, dcc_lankhmar, dcc_exceptions

    exc_counter = 1
    url = "https://goodman-games.com/store/dcc-modules-in-order-pdf/"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    test = soup.find_all("figcaption")
    items = [item.text for item in test]
    for item in items:
        if item.find(":") > 0:
            if item[:6] == "DCC 87":
                dcc_entries.append((87, item[7:]))
            elif item[:7] == "Dungeon":
                print(f"Exception item - {item}")
                t = item.split(":")
                dcc_exceptions.append((f"EXC{exc_counter}", strip_title(t[1])))
                exc_counter += 1
            else:
                print(item)
                t = item.split(":")
                i = t[0].split("#")
                if t[0][:6] == "DCC DE":
                    dcc_dyingearth.append((i[1], strip_title(t[1])))
                elif t[0][:12] == "DCC Lankhmar":
                    dcc_lankhmar.append((i[1], strip_title(t[1])))
                elif t[0][:10] == "DCC Empire":
                    dcc_empire.append((i[1], strip_title(t[1])))
                elif t[0][:10] == "DCC Horror":
                    dcc_horror.append((i[1], strip_title(t[1])))
                else:
                    dcc_entries.append((i[1], strip_title(t[1])))


def strip_title(title):
    return title.strip().replace("'", "").replace("\u2019", "").replace('\u2018', "").replace(" - PDF", "")


def rename_dcc_items(folder, file):
    # dcc issues before 53 are d20/3.5 compatible
    # 53-65 is 4E
    # 66+ is DCC OSR
    if len(dcc_entries) == 0:
        build_dcc_magazines()

    dcc = file[:-4].split("_")
    if len(dcc) < 3:
        print(f"{file} is not formatted properly for this section")
        exit()

    try:
        issue = int(dcc[1][5:])
    except ValueError:
        try:
            issue = float(dcc[1][5:])
        except ValueError:
            print(f"{file} is not giving us a proper issue for this section")
            exit()

    index = [i for i,v in enumerate(dcc_entries) if v[0] == str(issue)]
    rename = f"DCC_{str(issue).zfill(3)} - {dcc_entries[index[0]][1]}.pdf"

    # where does this issue go
    if issue > 65:
        new_location = settings['dccosr_location']
    elif issue > 53:
        new_location = settings['dcc4e_location']
    else:
        new_location = settings['dccd20_location']

    shutil.move(f"{folder}/{file}", f"{new_location}/{rename}")


def rename_linux_magazine(folder, file):
    issue = int(file.split(".")[0].split("_")[1])
    months = issue - 282
    the_date = datetime(2024, 5, 1) + relativedelta(months=months)
    year = the_date.year
    month = the_date.strftime("%m")
    rename = f"{year}-{month}_Linux_Pro_Magazine_{issue}.pdf"
    shutil.move(f"{folder}/{file}", f"{settings['linux_magazine_location']}/{year}/{rename}")


def main():
    file_renaming()


if __name__ == "__main__":
    # testing
    # rename_linux_magazine("", "LM_283.pdf")
    # rename_dcc_items("", "dungeoncrawlclassics_issue63_thewarbringersson.pdf")

    try:
        with open('settings.yaml', 'r') as f:
            settings = yaml.safe_load(f)
    except FileNotFoundError:
        print("Settings file not found.  Program can not run.")
        print("Please create a settings.yaml file for this program to use.")
        print("See GitHub documentation for further assistance.")
        exit()

    main()