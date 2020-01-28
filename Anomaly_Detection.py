import pandas as pd
import math
from datetime import datetime
df=pd.read_excel("df_indian_longitude1.xlsx")

base_location = df[df["Txn Count"] == max(df["Txn Count"])]
base_long = base_location["lon"].values.tolist()[0]
base_lat = base_location["lat"].values.tolist()[0]


from math import radians, cos, sin, asin, sqrt 
def distance(lat1, lat2, lon1, lon2): 
      
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2)       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))  
    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371   
    # calculate the result 
    return(c * r) 


            
def preprocessing(data):
    blanklis=[]
    for i in range(len(data)):
          blanklis.append(distance(data["lat"][i], base_lat, data["lon"][i], base_long))
    data['Distance1']=blanklis
    return data

def z_score(data):
    xs = data["Distance"].values.tolist()     # values (must be floats!)
    var  = sum(pow(x,2) for x in xs) / len(xs)  # variance
    data['z-score'] = [(x)/math.sqrt(var) for x in xs]
    return data
        
df=preprocessing(df)
df=z_score(df)      
q1 = df['z-score'].quantile(0.0)
q3 = df['z-score'].quantile(0.12)
iqr = q3 - q1 

def TnxThreshold(data):
    TnxTh=data.sort_values("Tnx Count", ascending = False)
    TnxTh=TnxTh.iloc[8:]
    TnxTh=TnxTh.loc[TnxTh['Tnx Count'] > 0]
    TnxTh=TnxTh['Tnx Count'].mean()
    print(TnxTh)
    return TnxTh

def AmountThreshold(data):
    AmtTh=data.loc[data['Amount']>1000]
    AmtTh=AmtTh['Amount'].mean()
    print(AmtTh)
    return AmtTh


for i in range(len(anomalies)):
    if anomalies["Txn Count"][i] > 5:
        


TnxTh=TnxThreshold(df)
AmtTh=AmountThreshold(df)

df['Date']=-1
for i in range(len(df["Last Txn Date"])):
    if df['Last Txn Date'][i]!=0:
        df['Date'][i] = pd.to_datetime(df['Last Txn Date'][i]).date
    else:
        df['Date'][i] = 0
        


def predict(data):
    Prediction=[]
    for i in range(len(data)):
     if data['Widthdraw_amount'][i]>AmtTh:
         Prediction.append("Anomaly: Case-1 Amount Exceeded")
         print("Anomaly: Case-1 Amount Exceeded")
     elif data['Widthdraw_amount'][i] < AmtTh:
         for j in range(len(df['City'])):
             if data['City'][i] == df["City"][j]:
                 if df['Tnx Count'][j] < TnxTh and df['Tnx Count'][j] >0 and df['z-score'][j] >  iqr and (df['Date'][j] - datetime.now().date()).days > 365 :
                    Prediction.append("Anomaly:less tnx,outer,no last 2 years tnx")
                 elif df['Tnx Count'][j] < TnxTh and df['Tnx Count'][j] >0 and df['z-score'][j] >  iqr and (df['Date'][j] - datetime.now().date()).days < 365:
                    Prediction.append("Anomaly:less tnx,outer")
                 elif df['Tnx Count'][j] < TnxTh and df['Tnx Count'][j] >0 and df['z-score'][j] <  iqr and (df['Date'][j] - datetime.now().date()).days > 365:
                    Prediction.append("Alert:less tnx,inner,no last 2 years tnx")
                 elif df['Tnx Count'][j] > TnxTh  and df['z-score'][j] <  iqr and (df['Date'][j] - datetime.now().date()).days > 365:
                    Prediction.append("Alert:inner,no last 2 years tnx")
                 elif df['Tnx Count'][j] > TnxTh  and df['z-score'][j] <  iqr and (df['Date'][j] - datetime.now().date()).days < 365:
                    Prediction.append("Genuine")
                 elif df['Tnx Count'][j] > TnxTh  and df['z-score'][j] > iqr and (df['Date'][j] - datetime.now().date()).days < 365:
                    Prediction.append("Genuine")
                 elif df['Tnx Count'][j] > TnxTh  and df['z-score'][j] >  iqr and (df['Date'][j] - datetime.now().date()).days > 365:
                    Prediction.append("Anomaly;Outer area, no tnx in 2 years")
                 elif df['Tnx Count'][j] > TnxTh  and df['z-score'][j] >  iqr and (df['Date'][j] - datetime.now().date()).days < 60:
                    Prediction.append("Genuine")
            
                 elif df['Tnx Count'][j] ==0 and df['z-score'][j] >  iqr 
                    Prediction.append("Anomaly;Outer area, no tnx")
                 elif df['Tnx Count'][j] ==0 and df['z-score'][j] <  iqr
                    Prediction.append("Alert;Inner area but no tnx")
                 else:
                    Prediction.append("Genuine")
                            
    return Prediction
         


                    
test=pd.read_excel('test.xlsx')
                

x=predict(test)        
    
