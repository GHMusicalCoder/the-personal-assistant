import sys
import yaml

f_download = ""


def main():
    pass


if __name__ == "__main__":
    try:
        with open('settings.yaml', 'r') as f:
            settings = yaml.safe_load(f)
    except FileNotFoundError:
        print("Settings file not found.  Program can not run.")
        print("Please create a settings.yaml file for this program to use.")
        print("See GitHub documentation for further assistance.")
        exit()
