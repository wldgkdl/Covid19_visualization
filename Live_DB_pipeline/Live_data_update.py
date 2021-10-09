from sodapy import Socrata
import pandas as pd
import os

original_age_sex = pd.read_csv("../EDA/age_sex_data_group_by.csv")
original_heavy_symtom = pd.read_csv("../EDA/heavy_symtom_data_groupby.csv")
original_us_states = pd.read_csv("../EDA/states_data_groupby.csv")

new_month = "2021-09"
def getting_recent_data(new_month):
	client = Socrata("data.cdc.gov", None)
	results = client.get("n8mc-b4w4", limit=5000000, case_month=new_month)#50000000
	original_data = pd.DataFrame.from_records(results)
	necessary_data = pd.DataFrame(original_data, columns =['case_month', 'res_state', 'age_group','sex','icu_yn']) 
	return necessary_data

def preprocessing_age_sex(necessary_data):
	# Slice related columns
	age_sex_data = necessary_data[["case_month", "age_group", "sex"]]
	# Drop NA
	age_sex_data = age_sex_data.dropna()
	# Drop "Missing" and "Unknown" rows in age_group and sex
	age_sex_data = age_sex_data[age_sex_data['age_group'] != "Missing"]
	age_sex_data = age_sex_data[age_sex_data['age_group'] != "Unknown"]
	age_sex_data = age_sex_data[age_sex_data['age_group'] != "NA"]
	age_sex_data = age_sex_data[age_sex_data['sex'] != "Missing"]
	age_sex_data = age_sex_data[age_sex_data['sex'] != "Unknown"]
	age_sex_data = age_sex_data[age_sex_data['sex'] != "Other"]
	age_sex_data = age_sex_data[age_sex_data['sex'] != "NA"]

	age_sex_data["sex_age"] = age_sex_data["sex"].astype(str) +"_"+ age_sex_data["age_group"].astype(str)
	age_sex_data = age_sex_data[["case_month", "sex_age"]]

	age_sex_data_group_by = age_sex_data.groupby(['case_month', 'sex_age']).size().reset_index(name='counts')

	# Convert new dataframe to pivot table
	age_sex_data_group_by = age_sex_data_group_by.pivot(index="case_month", columns="sex_age", values="counts")
	age_sex_data_group_by = age_sex_data_group_by.fillna(0)
	age_sex_data_group_by = age_sex_data_group_by.astype(int)
	age_sex_data_group_by.to_csv('test.csv',index_label=age_sex_data_group_by.columns.name)

	new = pd.read_csv("test.csv")
	frames = [original_age_sex, new]
	result = pd.concat(frames)
	os.remove("test.csv")
	result.to_csv('../EDA/age_sex_data_group_by.csv',index=False)

def preprocessing_heavy_symtom(necessary_data):
	# Slice related columns
	heavy_symtom_data = necessary_data[["case_month", "icu_yn"]]
	# Drop NA
	heavy_symtom_data = heavy_symtom_data.dropna()
	# Drop "Missing" and "Unknown" rows in icu_yn column
	heavy_symtom_data = heavy_symtom_data[heavy_symtom_data['icu_yn'] != "Missing"]
	heavy_symtom_data = heavy_symtom_data[heavy_symtom_data['icu_yn'] != "Unknown"]
	heavy_symtom_data = heavy_symtom_data[heavy_symtom_data['icu_yn'] != "nul"]
	heavy_symtom_data = heavy_symtom_data[heavy_symtom_data['icu_yn'] != "NA"]

	# Group by heavy symtom status
	heavy_symtom_data_groupby = heavy_symtom_data.groupby(['case_month', 'icu_yn']).size().reset_index(name='counts')

	# Convert new dataframe to pivot table
	heavy_symtom_data_groupby = heavy_symtom_data_groupby.pivot(index="case_month", columns="icu_yn", values="counts")

	# Export dataframe to csv file
	heavy_symtom_data_groupby.to_csv('test.csv',index_label=heavy_symtom_data_groupby.columns.name)	

	new = pd.read_csv("test.csv")
	frames = [original_heavy_symtom, new]
	result = pd.concat(frames)
	os.remove("test.csv")
	result.to_csv('../EDA/heavy_symtom_data_groupby.csv',index=False)

def preprocessing_states_data(necessary_data):
	# Slice related columns
	states_data = necessary_data[["case_month", "res_state"]]

	# Drop NA
	states_data = states_data.dropna()
	# Drop "Missing" and "Unknown" rows in icu_yn column
	states_data = states_data[states_data['res_state'] != "Missing"]
	states_data = states_data[states_data['res_state'] != "Unknown"]
	states_data = states_data[states_data['res_state'] != "NA"]

	# Group by states
	states_data_groupby = states_data.groupby(['case_month', 'res_state']).size().reset_index(name='counts')

	# Convert new states dataframe to pivot table
	states_data_groupby = states_data_groupby.pivot(index="case_month", columns="res_state", values="counts")
	states_data_groupby = states_data_groupby.fillna(0)
	# Export dataframe to csv file
	states_data_groupby.to_csv('test.csv',index_label=states_data_groupby.columns.name)

	new = pd.read_csv("test.csv")
	frames = [original_us_states, new]
	result = pd.concat(frames)
	result = result.fillna(0)
	os.remove("test.csv")
	result.to_csv('../EDA/states_data_groupby.csv',index=False)

necessary_data = getting_recent_data(new_month)

preprocessing_age_sex(necessary_data)
preprocessing_heavy_symtom(necessary_data)
preprocessing_states_data(necessary_data)

# aa = pd.read_csv('age_sex_data_group_by.csv')
# bb = pd.read_csv('heavy_symtom_data_groupby.csv')
# cc = pd.read_csv("states_data_groupby.csv")
# print(aa)
# print(bb)
# print(cc)


