import pandas as pd
df=pd.read_excel("data/cleaned/clean_data.xlsx")
RT=1
df["RC"]=df["Gas Price"]*df["Gas Used"]
df["RE"]=1/(RT*df["RC"])
df.to_excel("output/tables/result.xlsx",index=False)
