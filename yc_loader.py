import os
import pandas as pd
from ust import save_xml, read_rates, available_years

xml_directory = "./yc_xml"
if not os.path.exists(xml_directory):
    os.makedirs(xml_directory)

# save UST yield rates to local folder for selected years
for year in available_years():
    save_xml(year, folder=xml_directory)

# run later - force update last year (overwrites existing file)
save_xml(2022, folder=xml_directory, overwrite=True)

# read UST yield rates as pandas dataframe
df = read_rates(start_year=2014, end_year=2022, folder=xml_directory)
print(df)

# save as single CSV file
df.to_csv("yc.csv")

