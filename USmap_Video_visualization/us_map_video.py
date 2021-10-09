import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import PIL
import io
#print(gpd.__version__)
#print(pd.__version__)
image_frames = []

states_data = pd.read_csv("states_data_groupby.csv")
states_data = states_data.rename({"res_state":"STUSPS"}, axis='columns')
#states_data = states_data.set_index('Month')

states_data = states_data.fillna(0)
#states_data = states_data.astype(int)

data = states_data.T

new_header = data.iloc[0] #grab the first row for the header
data = data[1:] #take the data less the header row
data.columns = new_header #set the header row as the df header


# cumulate covid cases 
new_header_list = ['STUSPS']
for i in new_header:
	new_header_list.append(i)

cumulated_us = []
for i in data.iterrows():
	state_name = i[0]

	states = i[1]
	this_states = [state_name]
	start_value = 0
	for months in states:
		start_value = start_value + months
		this_states.append(start_value)
	cumulated_us.append(this_states)



etc_states = ["AS","GU", "PR", "VI","MP","AK", "HI"]
# Merge with Map
data1 = pd.DataFrame(cumulated_us, columns = new_header_list, dtype = float) 
#print(data1.info())
#print(len(data1))

for index, row in data1.iterrows():
    if row['STUSPS'] in etc_states:
        data1.drop(index, inplace=True)

#print(len(data1))

world = gpd.read_file('cb_2018_us_state_500k/cb_2018_us_state_500k.shp')
#print(world.info())
#print(world)

merge = world.set_index('STUSPS').join(data1.set_index('STUSPS'),  how = 'right')
#print(len(merge))

date_info = list(merge.columns)[9:]

for dates in date_info:

	ax = merge.plot(column = dates,
		            cmap = 'OrRd',
		            figsize = (10, 10),
		            scheme = 'user_defined',
		            classification_kwds = {'bins':[100, 500, 1000, 5000, 10000, 100000, 500000, 1000000, 5000000]},
		            legend = True,
		            edgecolor = 'black',
		            linewidth = 0.4)
	ax.set_title("Total Confirmed Covid cases: "+ str(dates), 
	            	fontdict = {'fontsize':20},
	            	pad = 12.5)
	ax.set_axis_off()
	ax.get_legend().set_bbox_to_anchor((0.18, 0.4))
	
	img = ax.get_figure()
	#print(type(img))

	f = io.BytesIO()
	img.savefig(f, format = 'png', bbox_inches = 'tight')
	f.seek(0)
	image_frames.append(PIL.Image.open(f))

image_frames[0].save("Dynamic COVID 19 Map.gif", format = "GIF",
	append_images = image_frames[1:],
	save_all = True,
	duration = 100,
	loop = 1)

f.close()