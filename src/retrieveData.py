import pandas as pd 
import wget
import os

table = pd.read_csv("../sparqlQuery.csv")
print(table)
for i, link in enumerate(table['work']):
    folder = f"treaty{i}"
    os.mkdir(folder)
    wget.download(link, out=folder)