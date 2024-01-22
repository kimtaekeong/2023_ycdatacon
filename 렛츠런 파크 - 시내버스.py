#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'
import warnings
warnings.filterwarnings(action='ignore') 


# In[2]:


import pandas as pd
import folium


# In[3]:


#렛츠런파크_위도경도
center = [35.952163,128.866750]
lat=35.952163
long=128.866750


# In[4]:


people=pd.read_csv('행정안전부_지역별(행정동) 성별 연령별 주민등록 인구수_20230228.csv',encoding='CP949')


# In[5]:


people.head()


# In[7]:


yc_peo=people[people['시군구명']=='영천시']
yc_peo


# In[8]:


yc_peo.sort_values(by='계',ascending=False)[['읍면동명','계']]


# In[9]:


bus_route=pd.read_csv('20230501184751_중심 관광지.csv',encoding='CP949')
buss=bus_route[bus_route['분류'].str.contains('관광')]


# In[10]:


buss


# In[11]:


buss.rename(columns={'중심 POI X 좌표': 'long','중심 POI Y 좌표': 'lat'}, inplace=True)


# In[12]:


buss=buss.reset_index()
buss=buss.head(25)
buss.head(10)


# In[13]:


center = [35.952163,128.866750]
m = folium.Map(location=center,
               zoom_start=17, 
               width=750, 
               height=500
              )
folium.Marker(center,
                    color='tomato',
                    radius = 100, 
                    icon=folium.Icon('red', icon='star'),
                    tooltip='렛츠런 파크').add_to(m)
for i in range(len(buss)):
    folium.Marker([buss['lat'][i], buss['long'][i]],
                        radius = 100, 
                        icon=folium.Icon('gray',icon='flag'),
                        tooltip=buss['관광지명'][i]).add_to(m)
m


# In[14]:


from geopy.geocoders import ArcGIS

def geocoding(address):
    try:
        geo = ArcGIS(user_agent='South Korea').geocode(address, timeout=10)
        x_y = [geo.latitude, geo.longitude]
        return x_y
    except:
        return [0,0]


# In[15]:


add_bus=['경북 영천시 금완로 98','경상북도 영천시 금호읍 덕성리 132-12','경북 영천시 강변로 44','경북 영천시 금호읍 금호로 72']
tooltip=['영천역','금호역','영천버스터미널','금호시외버스터미널']
latitude = []
longitude =[]

for i in add_bus:
    latitude.append(geocoding(i)[0])
    longitude.append(geocoding(i)[1])


# # 터미널

# In[16]:


m = folium.Map(location=center,
               zoom_start=17, 
               width=750, 
               height=500
              )
folium.Marker(center,
                    color='tomato',
                    radius = 100, 
                    icon=folium.Icon('red', icon='star'),
                    tooltip='렛츠런 파크').add_to(m)
    
for i in range(len(buss)):
    folium.Marker([buss['lat'][i], buss['long'][i]],
                        radius = 100, 
                        icon=folium.Icon('gray',icon='flag'),
                        tooltip=buss['관광지명'][i]).add_to(m)

for i in range(len(add_bus)):
    folium.Marker([latitude[i], longitude[i]],
                        radius = 100, 
                        icon=folium.Icon('green'),
                        tooltip=tooltip[i]).add_to(m)
m


# In[17]:


bus_event=pd.read_csv('yc_busevent.csv')
bus_event.head(10)


# In[18]:


len(bus_event['route_name'].unique())


# In[19]:


bus_event['route_name'] = bus_event['route_name'].str.replace('-', '_')
bus_event


# # 영천 버스 노선

# In[20]:


bus_name=[]
for nosun in bus_event['route_name'].unique():
    df_nosun = bus_event[bus_event['route_name'] == nosun].copy()
    df_nosun =df_nosun.drop_duplicates(subset=['bus stop_name'], keep='first').copy()
    globals()[f'bus_{nosun}'] = df_nosun.reset_index().copy()
    bus_name.append(f'bus_{nosun}')


# In[21]:


len(bus_name)


# In[22]:


globals()[f'bus_{nosun}']


# In[23]:


#unique_bus_stops = 
#bus_sun2 = bus_sun2.drop_duplicates(subset=['bus stop_name'], keep='first')
bus_순환2


# In[24]:


c=["blue",
"green",
"purple",
"orange",
"darkred",
"lightred",
"beige",
"darkblue",
"darkgreen",
"cadetblue",
"darkpurple",
"white",
"pink",
"lightblue",
"red",
"lightgreen",
"gray",
"black"]


# # 버스 노선 데이터 부재로 인해 버스 이벤트 데이터를 활용하여 노선 구하기

# In[59]:


# m = folium.Map(location=center,
#                zoom_start=17, 
#                width=750, 
#                height=500
#               )
# folium.Marker(center,
#                     color='tomato',
#                     radius = 100, 
#                     icon=folium.Icon('red', icon='star'),
#                     tooltip='렛츠런 파크').add_to(m)
# for step,bn in enumerate(bus_name[:18]):
#     bn=globals()[bn]
#     for i in range(len(bn)):
#         folium.CircleMarker(
#             location=[bn['bus stop_gps y'][i], 
#                       bn['bus stop_gps x'][i]],
#             tooltip=f"{bn['bus stop_name'][i]} {bn['route_name'][i]}",
#             radius=5,
#             color=c[step]
#         ).add_to(m);


# In[26]:


m


# In[60]:


# m = folium.Map(location=center,
#                zoom_start=17, 
#                width=750, 
#                height=500
#               )
# folium.Marker(center,
#                     color='tomato',
#                     radius = 100, 
#                     icon=folium.Icon('red', icon='star'),
#                     tooltip='렛츠런 파크').add_to(m)
# for step,bn in enumerate(bus_name[18:36]):
#     bn=globals()[bn]
#     for i in range(len(bn)):
#         folium.CircleMarker(
#             location=[bn['bus stop_gps y'][i], 
#                       bn['bus stop_gps x'][i]],
#             tooltip=f"{bn['bus stop_name'][i]} {bn['route_name'][i]}",
#             radius=5,
#             color=c[step]
#         ).add_to(m)


# In[28]:


m


# In[61]:


# m = folium.Map(location=center,
#                zoom_start=17, 
#                width=750, 
#                height=500
#               )
# folium.Marker(center,
#                     color='tomato',
#                     radius = 100, 
#                     icon=folium.Icon('red', icon='star'),
#                     tooltip='렛츠런 파크').add_to(m)
# for step,bn in enumerate(bus_name[36:54]):
#     bn=globals()[bn]
#     for i in range(len(bn)):
#         folium.CircleMarker(
#             location=[bn['bus stop_gps y'][i], 
#                       bn['bus stop_gps x'][i]],
#             tooltip=f"{bn['bus stop_name'][i]} {bn['route_name'][i]}",
#             radius=5,
#             color=c[step]
#         ).add_to(m)
# m


# In[30]:


m


# In[62]:


# m = folium.Map(location=center,
#                zoom_start=17, 
#                width=750, 
#                height=500
#               )
# folium.Marker(center,
#                     color='tomato',
#                     radius = 100, 
#                     icon=folium.Icon('red', icon='star'),
#                     tooltip='렛츠런 파크').add_to(m)
# for step,bn in enumerate(bus_name[54:72]):
#     bn=globals()[bn]
#     for i in range(len(bn)):
#         folium.CircleMarker(
#             location=[bn['bus stop_gps y'][i], 
#                       bn['bus stop_gps x'][i]],
#             tooltip=f"{bn['bus stop_name'][i]} {bn['route_name'][i]}",
#             radius=5,
#             color=c[step]
#         ).add_to(m)


# In[32]:


m


# In[63]:


# m = folium.Map(location=center,
#                zoom_start=17, 
#                width=750, 
#                height=500
#               )
# folium.Marker(center,
#                     color='tomato',
#                     radius = 100, 
#                     icon=folium.Icon('red', icon='star'),
#                     tooltip='렛츠런 파크').add_to(m)
# for step,bn in enumerate(bus_name[72:90]):
#     bn=globals()[bn]
#     for i in range(len(bn)):
#         folium.CircleMarker(
#             location=[bn['bus stop_gps y'][i], 
#                       bn['bus stop_gps x'][i]],
#             tooltip=f"{bn['bus stop_name'][i]} {bn['route_name'][i]}",
#             radius=5,
#             color=c[step]
#         ).add_to(m)


# In[34]:


m


# In[64]:


# m = folium.Map(location=center,
#                zoom_start=17, 
#                width=750, 
#                height=500
#               )
# folium.Marker(center,
#                     color='tomato',
#                     radius = 100, 
#                     icon=folium.Icon('red', icon='star'),
#                     tooltip='렛츠런 파크').add_to(m)
# for step,bn in enumerate(bus_name[90:104]):
#     bn=globals()[bn]
#     for i in range(len(bn)):
#         folium.CircleMarker(
#             location=[bn['bus stop_gps y'][i], 
#                       bn['bus stop_gps x'][i]],
#             tooltip=f"{bn['bus stop_name'][i]} {bn['route_name'][i]}",
#             radius=5,
#             color=c[step]
#         ).add_to(m)


# In[36]:


m


# 원하는 노선을 지나는 버스는 총 6대

# In[37]:


line_nosun=[bus_555_7,bus_111_1,bus_55,bus_555,bus_111]
line_nosun= pd.concat(line_nosun)
line_nosun


# In[38]:


len(line_nosun['bus stop_name'])


# In[39]:


import pandas as pd

pd.options.display.max_rows = 241

line_count = line_nosun['bus stop_name'].value_counts().to_frame().reset_index()
line_count.columns = ['bus stop_name', 'count']
count_5=line_count[line_count['count']==5]


# In[40]:


line_count


# In[41]:


count_5_list=count_5['bus stop_name'].tolist()


# In[42]:


count_5_list


# In[43]:


count_4=line_count[line_count['count']==4]
count_4_list=count_4['bus stop_name'].tolist()
count_4_list


# In[44]:


count_5_list


# In[45]:


x_y4=pd.DataFrame()
for name in count_4_list:
    x_y4=pd.concat([x_y4,line_nosun[line_nosun['bus stop_name']==name]])
#x_y4
line_x_y4=x_y4[::4].reset_index()
line_x_y4


# In[46]:


x_y4


# In[47]:


x_y5=pd.DataFrame()
for name in count_5_list:
    x_y5=pd.concat([x_y5,line_nosun[line_nosun['bus stop_name']==name]])
#x_y4
line_x_y5=x_y5[::5].reset_index()
line_x_y5


# In[48]:


x_y5=pd.DataFrame()
for name in count_5_list:
    x_y5=pd.concat([x_y5,line_nosun[line_nosun['bus stop_name']==name]])
    


# In[49]:


line_x_y5=x_y5[::5].reset_index()
line_x_y5


# In[50]:


m = folium.Map(location=center,
               zoom_start=17, 
               width=750, 
               height=500
              )
folium.Marker(center,
                    color='tomato',
                    radius = 100, 
                    icon=folium.Icon('red', icon='star'),
                    tooltip='렛츠런 파크').add_to(m)
    
for i in range(len(buss)):
    folium.Marker([buss['lat'][i], buss['long'][i]],
                        radius = 100, 
                        icon=folium.Icon('gray',icon='flag'),
                        tooltip=buss['관광지명'][i]).add_to(m)

for i in range(len(add_bus)):
    folium.Marker([latitude[i], longitude[i]],
                        radius = 100, 
                        icon=folium.Icon('green'),
                        tooltip=tooltip[i]).add_to(m)


# In[51]:


for i in range(len(line_x_y4)):
    folium.CircleMarker([line_x_y4['bus stop_gps y'][i],line_x_y4['bus stop_gps x'][i]],
                        radius = 5, 
                        color='purple',
                        fill_color='purple',
                         fill_opacity=1,
                        tooltip=line_x_y4['bus stop_name'][i]).add_to(m)
for i in range(len(line_x_y5)):
    folium.CircleMarker([line_x_y5['bus stop_gps y'][i],line_x_y5['bus stop_gps x'][i]],
                        radius = 5, 
                        color='darkorange',
                        fill_color='darkorange',
                         fill_opacity=1,
                        tooltip=line_x_y5['bus stop_name'][i]).add_to(m)
m


# # 반대방향과 이미 지나온 정류장 제거

# In[52]:


#line_x_y4
one_line_x_y4=line_x_y4[line_x_y4['bus stop_name'].isin(['오수동.쌍계마을입구(금호방면)','오수동e마트','영천경찰서','원제리','윤성아파트앞','808종점','금호초등학교','금호읍사무소'
                                           ,'금호시장앞','금호터미널건너'])]


# # 4개짜리 한방향만

# In[53]:


m = folium.Map(location=center,
               zoom_start=17, 
               width=750, 
               height=500
              )
folium.Marker(center,
                    color='tomato',
                    radius = 100, 
                    icon=folium.Icon('red', icon='star'),
                    tooltip='렛츠런 파크').add_to(m)
    
for i in range(len(buss)):
    folium.Marker([buss['lat'][i], buss['long'][i]],
                        radius = 100, 
                        icon=folium.Icon('gray',icon='flag'),
                        tooltip=buss['관광지명'][i]).add_to(m)

for i in range(len(add_bus)):
    folium.Marker([latitude[i], longitude[i]],
                        radius = 100, 
                        icon=folium.Icon('green'),
                        tooltip=tooltip[i]).add_to(m)


# In[54]:


one_line_x_y4=one_line_x_y4.drop('level_0',axis=1).reset_index()


# In[55]:


for i in range(len(one_line_x_y4)):
    folium.CircleMarker([one_line_x_y4['bus stop_gps y'][i],one_line_x_y4['bus stop_gps x'][i]],
                        radius = 5, 
                        color='purple',
                        fill_color='purple',
                        fill_opacity=1,
                        tooltip=one_line_x_y4['bus stop_name'][i]).add_to(m)
m


# # 5개 한방향

# In[56]:


one_line_x_y5=line_x_y5[line_x_y5['bus stop_name'].isin(['금호시장앞','금호터미널건너'])]
one_line_x_y5


# In[57]:


one_line_x_y5['bus stop_gps y']


# In[58]:


for i in range(1,len(one_line_x_y5)+1):
    folium.CircleMarker([one_line_x_y5['bus stop_gps y'][i],one_line_x_y5['bus stop_gps x'][i]],
                        radius = 5, 
                        color='orange',
                        fill_color='orange',
                        fill_opacity=1,
                        tooltip=one_line_x_y5['bus stop_name'][i]).add_to(m)
m


# In[ ]:




