from labs1 import *
from settings import *
from datetime import datetime
def getSheet(N,prapraktikum=False):
    if prapraktikum:
        return (2 * (N - 1)) + 1
    else:
        return (2 * (N - 1)) + 2
def runthisprogram():
    #dframe_sheetNilai = get_data_google_sheets(SHEET_CODE_PENILAIAN, PRAKTIKUM_KE)
    dframe_pra = get_data_google_sheets(SHEET_CODE_PRAKTIKUM, getSheet(PRAKTIKUM_KE,True))
    dframe_praktikum = get_data_google_sheets(SHEET_CODE_PRAKTIKUM, getSheet(PRAKTIKUM_KE,False))
    DeadlineTime = datetime.strptime(DEADLINE_TP, '%m/%d/%Y %H:%M:%S')
    DeadlineTimePrak = datetime.strptime(DEADLINE_PRAK, '%m/%d/%Y %H:%M:%S')

    FOLDER_PRAKTIKUM = "PRAKTIKUM_0"+str(PRAKTIKUM_KE)+"_"+SESI+KELAS
    FOLDER_PRA = "TP_0"+str(PRAKTIKUM_KE)+"_"+SESI+KELAS

    listnim = []
    for x in range(int(RANGE_NIM_BAWAH), int(RANGE_NIM_ATAS)+1): listnim.append(str(x))
    data_praprak = dframe_pra.to_records(index=False)
    data_praktikum = dframe_praktikum.to_records(index=False)
    pra_files = dict()
    praktikum_files = dict()
    for x in listnim:
        waktu = ""
        for y in data_praprak:
            if y[3] == x and waktu == "":
                pra_files[x] = y[8]
                waktu = y[0]
                # print("catch A")
            elif y[3] == x:
                w1 = y[0]
                # print("catch B")
                time1 = datetime.strptime(w1, '%m/%d/%Y %H:%M:%S')
                time0 = datetime.strptime(waktu, '%m/%d/%Y %H:%M:%S')
                if time1 > time0 and time1 < DeadlineTime:
                    pra_files[x] = y[8]
                    waktu = w1
            elif waktu == "":
                pra_files[x] = "NaN"

        waktu = ""
        for y in data_praktikum:
            if y[3] == x and waktu == "":
                praktikum_files[x] = y[8]
                waktu = y[0]
            elif y[3] == x:
                w1 = y[0]
                # print("catch B")
                time1 = datetime.strptime(w1, '%m/%d/%Y %H:%M:%S')
                time0 = datetime.strptime(waktu, '%m/%d/%Y %H:%M:%S')
                diff = time1 - time0
                if time1 > time0 and time1 < DeadlineTimePrak and diff.total_seconds() < SPANTIME:
                    praktikum_files[x] = y[8]
                    waktu = w1
            elif waktu == "":
                praktikum_files[x] = "NaN"

    if(DOWNLOAD_TP):
        makeNewFolder(FOLDER_PRA)
        for x in listnim:
            if (pra_files[x] != "Nan"):
                flname = "H0" + str(PRAKTIKUM_KE) + "_" + str(x) + ".zip"
                downloadFile(pra_files[x], flname, FOLDER_PRA)
                unzipfile(flname,FOLDER_PRA)

    if(DOWNLOAD_PRAK):
        makeNewFolder(FOLDER_PRAKTIKUM)
        for x in listnim:
            if(praktikum_files[x]!="NaN"):
                flname = "P0" + str(PRAKTIKUM_KE) + "_" + str(x) + ".zip"
                downloadFile(praktikum_files[x],flname,FOLDER_PRAKTIKUM)
                unzipfile(flname,FOLDER_PRAKTIKUM)
