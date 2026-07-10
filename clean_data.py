import pandas as pd
def clean_dataset(inp,out):
 df=pd.read_excel(inp)
 df=df.drop_duplicates()
 df=df.dropna(subset=["Timestamp","Gas Price","Gas Used"])
 for c in ["Gas Price","Gas Used"]:
  df[c]=pd.to_numeric(df[c],errors="coerce")
 df=df.dropna(subset=["Gas Price","Gas Used"])
 df=df[(df["Gas Price"]>0)&(df["Gas Used"]>0)]
 df.to_excel(out,index=False)
if __name__=="__main__":
 clean_dataset("data/raw/raw_data.xlsx","data/cleaned/clean_data.xlsx")
