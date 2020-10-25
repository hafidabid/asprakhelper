import datetime
import os
import gdown
from zipfile import ZipFile
import pdb
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

def getgdownurl(oldurl):
    token = oldurl[33::]
    return "https://drive.google.com/uc?id="+token

def makeNewFolder(foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)
        return True
    else: return False

def downloadFile(gUrl,filename,foldername=""):
    try:
        if(foldername==""):
            gdown.download(getgdownurl(gUrl), filename)
        else:
            makeNewFolder(foldername)
            gdown.download(getgdownurl(gUrl), foldername+"/"+filename)
    except Exception as e:
        print(e)

def unzipfile(filename,isLate=False,foldername=""):
    try:
        f = filename[:len(filename) - 4:]
        if isLate:
            f= f+" TERLAMBAT"
        if(foldername==""):
            with ZipFile(filename, 'r') as toUnzip:
                toUnzip.extractall(f)
        else:
            makeNewFolder(foldername)
            with ZipFile(foldername + "/" + filename, 'r') as toUnzip:
                toUnzip.extractall(foldername + "/" +f)
    except Exception as e:
        print(e)

def getfileInFolder(dir=""):
    if os.path.exists(dir) and dir!="":
        return  os.listdir(dir)
    elif dir=="" : return os.listdir()
    else : return []


def pureNIM(oldnim):
    newnim = ""
    for x in oldnim:
        if x>="0" and x<="9" : newnim=newnim+x
    return newnim

def get_data_google_sheets(sample_spreadsheet_id, tab_index):
    # Link to authenticate
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    # Read the .json file and authenticate with the links
    credentials = Credentials.from_service_account_file(
        'asistenpengkom-1dfb14ae8f40.json',
        scopes=scopes
    )

    # Request authorization and open the selected spreadsheet
    gc = gspread.authorize(credentials).open_by_key(sample_spreadsheet_id)
    #print(gc)
    # Prompts for all spreadsheet values
    values = gc.get_worksheet(tab_index).get_all_values()
    #print(values)
    # Turns the return into a dataframe
    df = pd.DataFrame(values)
    df.columns = df.iloc[0]
    df.drop(df.index[0], inplace=True)

    return df
