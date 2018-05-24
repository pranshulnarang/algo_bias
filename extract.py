import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def get_db_yr(x):
	return int(x.split('/')[-1])

def get_sc_yr(x):
	return int(x.split('/')[-1].split(' ')[0]) + 100


def process_sc(req):
	req_new = req.loc[:,['Screening_Date']]
	req_new = req_new.applymap(get_sc_yr)
	return req_new

def process_dob(req):
	req_new = req.loc[:, ['DateOfBirth']]
	req_new = req_new.applymap(get_db_yr)
	return req_new

def get_age(req):
	req["Age"]=req.loc[:,['Screening_Date']].sub(req['DateOfBirth'], axis=0)["Screening_Date"]
	# print req["Age"]
	return req
	# pass

df = pd.read_csv("data/raw.csv")
# print(df["RawScore"].max())
df = df[df.DisplayText != 'Risk of Failure to Appear']
df = df[df.DisplayText != 'Risk of Recidivism']
cols = df.columns.values

req_cols =[cols[i] for i in (3,7,8,13,14,15,16)]

for col in req_cols:
	unique_rows = df[col].unique()
	i = 1
	for each_row in unique_rows:
		df[col] = df[col] .replace([each_row], i)
		i+=1
		
df["DateOfBirth"] = process_dob(df)["DateOfBirth"]
df["Screening_Date"] = process_sc(df)["Screening_Date"]
df = get_age(df)

df["RawScore"] += np.abs(df["RawScore"].min() )+ 1.0

train, test = train_test_split(df, test_size=(1.0/6.0))

df.to_csv("data/out.csv")
train.to_csv("data/out-train.csv")
test.to_csv("data/out-test.csv") 

print(train.shape)
print(test.shape)
print(df.shape)