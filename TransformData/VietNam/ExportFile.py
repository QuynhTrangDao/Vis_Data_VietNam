import pandas as pd
import sys
import math
sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')
from base.PATH_UPDATE import *
from VAR_GLOBAL_CONFIG import *
from base.Setup import *
from Flow.ulis import *
pd.options.mode.chained_assignment = None
print("Path get data: ",FU.PATH_MAIN_CURRENT)
# PRICE_1 = pd.read_json(f"{FU.PATH_MAIN_CURRENT}/PRICE.json").rename(columns={"Date":"Time"})
# PRICE_2 = pd.read_json(f"{FU.PATH_MAIN_CURRENT}/PRICE_HSX.json").rename(columns={"Date":"Time"})
# PRICE = pd.concat([PRICE_1,PRICE_2])
# PRICE = PRICE.drop_duplicates()
DIVIDEND = pd.read_excel(f"{FU.PATH_MAIN_CURRENT}/DIVIDEND.xlsx")
# print(DIVIDEND)
FINANCIAL = pd.read_excel(f"{FU.PATH_MAIN_CURRENT}/FINANCAIL_{QUARTER_KEY.replace('/','_')}.xlsx",)
# print(FINANCIAL)
Volume = pd.read_excel(f"{FU.PATH_MAIN_CURRENT}/Volume.xlsx")






# print(Volume)
# raise 1
# DIVIDEND = pd.DataFrame()
# DIVIDEND = pd.read_excel(f"{FU.PATH_MAIN_CURRENT}/DIVIDEND.xlsx")
# Volume = pd.read_excel(f"{FU.PATH_MAIN_CURRENT}/Volume_NotHOSE.xlsx")
# Value_Volume = pd.read_csv(f"{FU.PATH_MAIN_CURRENT}/VALUE_ARG.csv")
# INFOR = List_Symbol[["Mã CK▲","Sàn"]].rename(columns={"Mã CK▲":'Symbol',
#                                                     "Sàn":"Exchange"})
# print(INFOR)
# KEY = 92
# FINANCIAL = pd.read_csv(f"G:\My Drive\DataVIS\VietNam\Data Lake\Distillation\All_Real/3_2022.csv")
# PRICE = pd.read_json(f"G:\My Drive\DataVIS\VietNam\Data Lake\Distillation\All_Real\Base/Close_CafeF_STOCKBIZ.json").rename(columns={"Date":"Time"})
# Value_Volume = pd.read_csv(f"G:\My Drive\DataVIS\VietNam\Data Lake\Distillation\All_Real\Base\ValueTrading.csv")
# FINANCIAL = pd.read_csv(f"G:/My Drive\DataVIS/VietNam/Data WareHouse/Data Year/Data_Year.csv")
# DIVIDEND_1 = pd.read_csv(f"G:\My Drive\DataVIS\VietNam\Data Lake\Stogare\Dividend\Dividend_0.csv")
# DIVIDEND_2 = pd.read_excel(f"G:/My Drive/DataVIS/VietNam/Data Lake/Raw_VIS/2022-11-06/DIVIDEND.xlsx")
# DIVIDEND_3 = pd.read_excel(f"G:/My Drive/DataVIS/VietNam/Data Lake/Raw_VIS/2023-02-04/DIVIDEND.xlsx")
# DIVIDEND_4 = pd.read_excel(f"G:/My Drive/DataVIS/VietNam/Data Lake/Raw_VIS/2023-03-03/DIVIDEND.xlsx")
# DIVIDEND = pd.concat([DIVIDEND,DIVIDEND_1])
# DIVIDEND = pd.concat([DIVIDEND,DIVIDEND_2])
# DIVIDEND = pd.concat([DIVIDEND,DIVIDEND_3])
# DIVIDEND = pd.concat([DIVIDEND,DIVIDEND_4])
# DIVIDEND = DIVIDEND.drop_duplicates()
# DIVIDEND = DIVIDEND.sort_values(by=['Time'])
# print(PRICE)
# print(DIVIDEND)
# FILE_TOTAL = FINANCIAL
# FILE_TOTAL = pd.merge(FINANCIAL,INFOR,on=['Symbol'],how="left")
# FILE_TOTAL["Time_Investment_Number"] = FILE_TOTAL["Time"].apply(lambda row: row)
# FILE_TOTAL["Time"] = [f'{QUARTER_KEY.split("/")[1]}/{QUARTER_KEY.split("/")[0]}' for i in FILE_TOTAL.index]
# FILE_TOTAL["Time_Investment_Number"] = FILE_TOTAL["Time"].apply(lambda x: int(x.split("/")[0]) + (int(x.split("/")[1])-2000)*4)
# FILE_TOTAL.to_csv(f"C:/Users/vangd/OneDrive/Desktop/Data({KEY}).csv",index=False)
# raise 1
#Moi .................
# FILE_TOTAL = FINANCIAL
# def tryUpper(exchange):
#     try:
#         return exchange.upper()
#     except:
#         pass
# FILE_TOTAL["Exchange"] = FILE_TOTAL["Exchange"].apply(lambda row: tryUpper(row))

# FILE_TOTAL["Time"] = FILE_TOTAL.TIME.astype(int)
# FILE_TOTAL["Time_Investment_Number"] = FILE_TOTAL["Time"]

print(FILE_TOTAL)
def count_company(dt):
    count = 0
    for i in COMPANY_ACTIVE:
        if i in dt['Symbol'].values:
            count +=1
    return count

def checkTime(number):
    start,e = CoverTime(number,TYPE_TIME)
    start -= datetime.timedelta(days=3)
    # return start.strftime("%Y-%m-%d")
    df = pd.DataFrame()
    temp = FILE_TOTAL[(FILE_TOTAL["Time_Investment_Number"] == number)]
    on_exchange = count_company(temp)+1
    count_ = 0
    t = 0
    while count_/on_exchange < 0.5 and t <30:
        time_str = start.strftime("%Y-%m-%d")
        df = PRICE[PRICE["Time"] == time_str]
        count_ = count_company(df)
        start += datetime.timedelta(days=1)
        t +=1
    if t == 30:
        return None
    try:
        return df["Time"][df.index[0]].strftime("%Y-%m-%d")
    except:
        return None


def getDay(arr_):
    arr = []
    for number in arr_:
        arr.append(checkTime(number))
    return pd.DataFrame({"Time_Investment_Number":[number for number in arr_],
                            "Date_Buy":arr})


def getClose(symbol,start,end,Close):
    end_end = datetime.datetime(end.year,end.month,end.day+20)
    end,end_end = end.strftime("%Y-%m-%d"),end_end.strftime("%Y-%m-%d")
    df = Close[(Close['Time'] == start) & (Close['Symbol'] == symbol)].reset_index(drop=False)
    try:
        buy = df["Close"][0]
    except KeyError:
        buy = 0
    df = Close[(Close['Time'] >=end)& (Close['Time'] <= end_end) & (Close['Symbol'] == symbol)].sort_values(by=['Time']).reset_index(drop=False)
    try:
        sell = df["Close"][0]
    except KeyError:
        sell = 0
    return buy,sell

def getDividend(symbol):
    try:
        dividend = DIVIDEND[DIVIDEND['Symbol'] == symbol].reset_index()
    except FileNotFoundError:
        dividend = pd.DataFrame()
    return dividend

def getSale(start,time,symbol,Close,dividend):
    v,end = CoverTime(time,year=TYPE_TIME)
    buy,value = getClose(symbol,start,end,Close)
    sum = 0
    cp=1
    if dividend.empty:
        return buy,value*cp+sum
    df = dividend[(dividend['Time'] >=start) & (dividend['Time'] <=end.strftime("%Y-%m-%d"))].reset_index()
    for i in df.index:
        if df["Money"][i] != "NAN":
            tyle = df["Money"][i]
            sum = sum + cp*10*eval(tyle)
        if df["Stock"][i] != "NAN":
            tyle = df["Stock"][i]
            cp = cp*1/eval(tyle)+cp
    return buy,value*cp+sum

# print(pd.unique(FILE_TOTAL["Time_Investment_Number"]))

# Data_Buy = getDay(pd.unique(FILE_TOTAL["Time_Investment_Number"]))
# FILE_TOTAL = pd.merge(FILE_TOTAL,Data_Buy,on=["Time_Investment_Number"],how="left")
# print(FILE_TOTAL)
arr_tb = []
arr_m = []
arr_b = []
sym = ""
CURRENT = 0

for i in FILE_TOTAL.index:
    CURRENT+=1
    if FILE_TOTAL["Time_Investment_Number"][i] ==2022:
        try:
            if sym != FILE_TOTAL['Symbol'][i]:
                sym = FILE_TOTAL['Symbol'][i]
                Close = PRICE[PRICE['Symbol'] == sym].reset_index(drop=True)
                dividend = getDividend(sym)
            m,b = getSale(FILE_TOTAL["Date_Buy"][i],FILE_TOTAL["Time_Investment_Number"][i],FILE_TOTAL['Symbol'][i],Close,dividend)
            print(b,sym)
            # FILE_TOTAL["BUY"][i] = m
            FILE_TOTAL["SELL"][i] = b
        except TypeError:
            print(i)
            m,b = 0,0
        # print(CURRENT)
    # progress_bar(CURRENT,TOTAL,text="Ghep Gia!!!")
    # arr_m.append(m)
    # arr_b.append(b)
# FILE_TOTAL["BUY"] = arr_m
# FILE_TOTAL["SELL"] = arr_b


def getVolume(symbol):
    try:
        df = Volume[Volume['Symbol']==symbol]
        # print(df)
        return df["Volume"][df.index[0]]
    except:
        print(f"{symbol}_loi_volume")
        return
# print(getVolume("KPF"))

# FILE_TOTAL["Volume"] = FILE_TOTAL.apply(lambda row: getVolume(row['Symbol']),axis=1)

def tbc(arr):
    return sum(arr)/len(arr)
def getValueTrading(day,symbol,df_value):
    df_value = df_value.sort_values(by="Time").reset_index(drop=True)
    try:
        index = df_value[df_value["Time"]==day].index[-1]
        if index < 10:
            return 0,0
        else:
            volume = df_value["VolumeTrading"][index-10:index].values
            value = df_value["ValueTrading"][index-10:index].values
            return tbc(volume),tbc(value)
    except IndexError:
        return 0,0
# arr_vo=[]
# arr_va=[]
# sym = ""
# for i in FILE_TOTAL.index:
#     # try:
#     if sym != FILE_TOTAL['Symbol'][i]:
#         sym = FILE_TOTAL['Symbol'][i]
#         Value = Value_Volume[Value_Volume['Symbol'] == sym]
#     vol,val = getValueTrading(FILE_TOTAL["Date_Buy"][i],FILE_TOTAL['Symbol'][i],Value)
#     # except TypeError:
#     #     vol,val = 0,0
#     progress_bar(i,TOTAL,text="Ghep KLGGTB")
#     # print(vol,val,FILE_TOTAL["Time"][i])
#     arr_vo.append(vol)
#     arr_va.append(val)

# FILE_TOTAL["VolumeARG_"] = arr_vo
# FILE_TOTAL["ValueARG_"] = arr_va
FILE_TOTAL['PROFIT'] = FILE_TOTAL['SELL']/FILE_TOTAL['BUY']
print(FILE_TOTAL)
# FILE_TOTAL['MARKET_CAP'] = FILE_TOTAL['BUY']*FILE_TOTAL['Volume']*1000

# FILE_TOTAL["check"] = FILE_TOTAL['Symbol'].apply(lambda row: row in COMPANY_DELETE)
# FILE_TOTAL = FILE_TOTAL[FILE_TOTAL["check"]==False].reset_index(drop=True)
# FILE_TOTAL.drop('check', inplace=True, axis=1)
# FILE_TOTAL.to_csv(f"{PATH_DISTILLATION_VIETNAM_ALLREAL}/{QUARTER_KEY.replace('/','_')}_NotHOSE.csv",index=False)
FILE_TOTAL.to_csv(f"{PATH_DISTILLATION_VIETNAM_ALLREAL}/0-2021.csv",index=False)
# FILE_TOTAL.to_csv(f"C:/Users/vangd/OneDrive/{KEY}.csv",index=False)