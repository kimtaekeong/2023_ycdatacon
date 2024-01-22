#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'
import warnings
warnings.filterwarnings(action='ignore') 
import folium
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# AppleGothic 폰트 경로 가져오기
font_path = fm.findfont(fm.FontProperties(family='AppleGothic'))

# 한글 폰트 등록
plt.rcParams['font.family'] = 'AppleGothic'


# In[12]:


yc_1=pd.read_csv('20230512164942_방문자 거주지 분포.csv',encoding='CP949')
yc_2=pd.read_csv('20230512164952_방문자 유출지 분포.csv',encoding='CP949')
yc_1.head(5)
yc_2.head(5)


# In[13]:


yc_1=yc_1.groupby('광역지자체명')['기초지자체별 거주 방문자 수'].sum().sort_values(ascending=False)
yc_2=yc_2.groupby('광역지자체명')['기초지자체별 유출 방문자 수'].sum().sort_values(ascending=False)


# In[14]:


import matplotlib.pyplot as plt

# 데이터 설정
labels1 = yc_1.index
labels1 = list(labels1[:7]) + [''] * (len(labels1) - 7)  # 광역지자체명
sizes1 = yc_1.values  # 기초지자체별 거주 방문자 수
colors1 = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']  # 색상 설정

labels2 = yc_2.index
labels2 = list(labels2[:4]) + [''] * (len(labels2) - 4)  # 광역지자체명
sizes2 = yc_2.values  # 기초지자체별 거주 방문자 수
colors2 = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']  # 색상 설정

def my_autopct(pct):
    return f"{pct:.1f}%" if pct > 2 else ""
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

centre_circle1 = plt.Circle((0, 0), 0.5, fc='white')
ax1.add_artist(centre_circle1)
ax1.pie(sizes1,labels=labels1,colors=colors1,autopct=my_autopct, startangle=90,textprops={'fontsize': 12})


ax2.pie(sizes2,labels=labels2,colors=colors2,autopct=my_autopct, startangle=90,textprops={'fontsize': 12})
centre_circle2 = plt.Circle((0, 0), 0.5, fc='white')
ax2.add_artist(centre_circle2)


# 타이틀 설정
ax1.set_title("방문자 거주지 분포", fontsize=20)
ax2.set_title("방문자 유출지 분포", fontsize=20)


# 그래프 출력
plt.axis('equal')
plt.show()


# In[19]:


people=pd.read_csv('행정안전부_지역별(행정동) 성별 연령별 주민등록 인구수_20230228.csv',encoding='CP949')


# In[20]:


people.head()


# # 대구 광역시

# In[21]:


dg=people[people['시도명']=='대구광역시']
dg['시군구명'].unique()
dg.head()


# In[22]:


age=dg.iloc[:,8:]
not_age=dg.iloc[:,:8]
df2=not_age.copy()
for i in range(12):
    a=age.iloc[:,10*i:10*(i+1)].sum(axis=1)
    df2[f'{i*10}대 남자']=a
for i in range(11,23):
    a=age.iloc[:,10*i+1:10*(i+1)+1].sum(axis=1)
    df2[f'{i*10-110}대 여자']=a
df2


# # 도로명 주소를 위도 경도로 변환해주는 코드

# In[23]:


get_ipython().system('pip install geopy')


# In[24]:


from geopy.geocoders import ArcGIS

def geocoding(address):
    try:
        geo = ArcGIS(user_agent='South Korea').geocode(address, timeout=10)
        x_y = [geo.latitude, geo.longitude]
        return x_y
    except:
        return [0,0]

address = "경상북도 구미시 구미중앙로 12"
x_y = geocoding(address)
print(x_y)


# In[11]:


geocoding('경북 구미시 구미중앙로 76')


# In[56]:


# from geopy.geocoders import Nominatim

# geolocator = Nominatim(user_agent='South Korea')

# def geocoding(address):
#     try:
#         location = geolocator.geocode(address, timeout=10, exactly_one=True)
#         return (location.latitude, location.longitude)
#     except:
#         return (0, 0)

# address = '경기도 화성시 봉담읍 와우리 230'
# lat, lng = geocoding(address)
# print(lat, lng)


# # 대구 지하철 승하차

# In[25]:


dg_sub=pd.read_csv('대구교통공사_역별일별시간별승하차인원현황_20230228.csv',encoding='CP949')
dg_sub.head(5)
dg_sub['역명']=dg_sub['역명'].replace('반월당1','반월당')
dg_sub['역명']=dg_sub['역명'].replace('반월당2','반월당')
dg_sub['역명']=dg_sub['역명'].replace('명덕1','명덕')
dg_sub['역명']=dg_sub['역명'].replace('명덕3','명덕')
dg_sub['역명']=dg_sub['역명'].replace('청라언덕2','청라언덕')
dg_sub['역명']=dg_sub['역명'].replace('청라언덕3','청라언덕')


# In[26]:


ride=dg_sub[dg_sub['승하차']=='승차'].sort_values(ascending=False,by='일계')
take_off=dg_sub[dg_sub['승하차']=='하차'].sort_values(ascending=False,by='일계')
ride=ride.groupby('역명')[['05시-06시', '06시-07시', '07시-08시',
       '08시-09시', '09시-10시', '10시-11시', '11시-12시', '12시-13시', '13시-14시',
       '14시-15시', '15시-16시', '16시-17시', '17시-18시', '18시-19시', '19시-20시',
       '20시-21시', '21시-22시', '22시-23시', '23시-24시','일계']].sum().sort_values(ascending=False,by='일계').reset_index()
take_off=take_off.groupby('역명')[['05시-06시', '06시-07시', '07시-08시',
       '08시-09시', '09시-10시', '10시-11시', '11시-12시', '12시-13시', '13시-14시',
       '14시-15시', '15시-16시', '16시-17시', '17시-18시', '18시-19시', '19시-20시',
       '20시-21시', '21시-22시', '22시-23시', '23시-24시','일계']].sum().sort_values(ascending=False,by='일계').reset_index()

ride
take_off


# 대구 지하철 승하차 시각화

# In[27]:


import seaborn as sns
import matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 1, figsize=(20,10))
sns.barplot(x='역명', y='일계', data=ride.head(10), palette='pastel', ax=axs[0])
axs[0].set_title('역별 일일 승차 인구수',fontsize=20)
axs[0].set_xlabel('역명',fontsize=15)
axs[0].set_ylabel('승차 인원',fontsize=15)
axs[0].tick_params(axis='both', which='major', labelsize=15)

sns.barplot(x='역명',y='일계',data=take_off.head(10),palette='pastel',ax=axs[1])
axs[1].set_title('역별 일일 하차 인구수',fontsize=20)
axs[1].set_xlabel('역명',fontsize=15)
axs[1].set_ylabel('하차 인원',fontsize=15)
axs[1].tick_params(axis='both', which='major', labelsize=15)
plt.subplots_adjust(hspace=0.5)
plt.show()


# In[28]:


add_dg=['대구광역시 중구 달구벌대로 2100','대구 동구 동대구로 550','대구 중구 중앙대로 424','대구 달서구 월배로 223','대구 남구 월배로 501']


# In[29]:


lat_dg = []
long_dg =[]

for i in add_dg:
    lat_dg.append(geocoding(i)[0])
    long_dg.append(geocoding(i)[1])


# In[30]:


lat_dg
long_dg


# 대구 지하철 유동 인구 많은 상위 5개 역 지도 표시

# In[31]:


# !pip install geopandas


# In[32]:


center=[geocoding('대구광역시 중구 달구벌대로 2100')[0],geocoding('대구광역시 중구 달구벌대로 2100')[1]]
m = folium.Map(location=center,zoom_start=17, 
               width=750, 
               height=500)
tooltip=['반월당역','동대구역','중앙로역','상인역','서부정류장역']
for i in range(len(lat_dg)):
    folium.Marker([lat_dg[i], long_dg[i]],
                        color='tomato',
                        radius = 100, 
                        icon=folium.Icon('tomato'),
                        tooltip=tooltip[i]).add_to(m)

m


# 셔틀 출발: <반월당역> - <동대구역>

# # 경상북도 

# In[33]:


gb=people[people['시도명']=='경상북도']
gb['시군구명'].unique()
gb.head()


# In[34]:


age=gb.iloc[:,8:]
not_age=gb.iloc[:,:8]
df2=not_age.copy()


# In[35]:


for i in range(12):
    a=age.iloc[:,10*i:10*(i+1)].sum(axis=1)
    df2[f'{i*10}대 남자']=a
for i in range(11,23):
    a=age.iloc[:,10*i+1:10*(i+1)+1].sum(axis=1)
    df2[f'{i*10-110}대 여자']=a
df2


# # 경상북도 인구 수 많은 상위 두개 지역

# 전체 인구 수 기준

# In[36]:


tot=df2[['시군구명','계']].groupby('시군구명')['계'].sum().sort_values(ascending=False).to_frame().reset_index()
#tot
plt.subplots(figsize=(20, 6))
sns.barplot(x='시군구명',y='계',data=tot)
tot.head(2)


# 40~50대 인구 수 기준

# In[37]:


tot2=df2[['시군구명','40대 남자','50대 남자','40대 여자','50대 여자']].groupby('시군구명')[['40대 남자','50대 남자','40대 여자','50대 여자']].sum()
tot2=tot2.sum(axis=1).sort_values(ascending=False).to_frame().reset_index()
tot2= tot2.rename(columns={0: '계'})
tot2.head(2)
plt.subplots(figsize=(20, 6))
sns.barplot(x='시군구명',y='계',data=tot2)


# # 주요 시군구의 인구 수가 많은 읍면동 세군데 추출

# 전체 인구 수 기준

# <구미>

# In[38]:


df2[df2['시군구명']=='구미시'].sort_values(by='계', ascending=False).head(3)['읍면동명']


# <포항시 북구>

# In[39]:


df2[df2['시군구명']=='포항시 북구'].sort_values(by='계', ascending=False).head(3)['읍면동명']


# 40-50대 인구 수 기준

# <구미>

# In[40]:


a=df2[df2['시군구명']=='구미시'][['읍면동명','40대 남자','50대 남자','40대 여자','50대 여자']].groupby('읍면동명')[['40대 남자','50대 남자','40대 여자','50대 여자']].sum()
a.sum(axis=1).sort_values(ascending=False).head(3)


# <포항시 북구>

# In[41]:


b=df2[df2['시군구명']=='포항시 북구'][['읍면동명','40대 남자','50대 남자','40대 여자','50대 여자']].groupby('읍면동명')[['40대 남자','50대 남자','40대 여자','50대 여자']].sum()
pohang_top3=b.sum(axis=1).sort_values(ascending=False).head(3)


# # 상위 두개 지역에 상위 3개의 읍면동 찍기

# <구미>

# In[42]:


# 인동동 양포동 선주원남동
address1=['경상북도 구미시 인동15길 42','경상북도 구미시 산호대로35길 6','경상북도 구미시 봉곡로 42']


# In[43]:


latitude1 = []
longitude1 =[]

for i in address1:
    latitude1.append(geocoding(i)[0])
    longitude1.append(geocoding(i)[1])


# 파란점-상위 3개의 읍면동
# 빨간점-구미시 최다승차 버스 지점 5군데 (구미역1-금오산사거리-구미역2 같은 위치)

# In[44]:


center = [36.1327723, 128.3200213]

m = folium.Map(location=center,
               zoom_start=17, 
               width=750, 
               height=500
              )
tooltip=['인동동','양포동','선주원남동']
for i in range(len(latitude1)):
    folium.Marker([latitude1[i], longitude1[i]],
                        color='tomato',
                        radius = 100, 
                        icon=folium.Icon('blue'),
                        tooltip=tooltip[i]).add_to(m)
folium.Marker(geocoding('경북 구미시 구미중앙로 76'),
              popup="구미역",
              icon=folium.Icon('red', icon='star'),
              tooltip="구미역").add_to(m)
folium.Marker(geocoding('경상북도 구미시 인동중앙로 28'),
              popup="인동초등학교",
              icon=folium.Icon('red', icon='star'),
              tooltip="인동초등학교").add_to(m)
folium.Marker(geocoding('경상북도 구미시 상사동로 51'),
              popup="상모농협앞",
              icon=folium.Icon('red', icon='star'),
              tooltip="상모농협앞").add_to(m)
folium.Marker(geocoding('경상북도 구미시 구미중앙로 124'),
              popup="금오산사거리",
              icon=folium.Icon('red', icon='star'),
              tooltip="금오산사거리").add_to(m)
m


# 셔틀버스 출발: <구미역> - <인동초등학교>

# <포항시 북구>

# In[45]:


#장량동 흡해읍 우창동
address2=['경북 포항시 북구 법원로63번길 10','경상북도 포항시 북구 흥해읍 동해대로 1511','경상북도 포항시 북구 우창동로 24']


# In[46]:


latitude2 = []
longitude2 =[]

for i in address2:
    latitude2.append(geocoding(i)[0])
    longitude2.append(geocoding(i)[1])


# In[47]:


add_po=['경상북도 포항시 북구 장량로 50','경상북도 포항시 북구 흥해읍 한동로 52']
lat_po = []
long_po =[]

for i in add_po:
    lat_po.append(geocoding(i)[0])
    long_po.append(geocoding(i)[1])


# In[48]:


pohang_top3
sns.barplot(x=pohang_top3.index,y=pohang_top3.values,palette='pastel')
for idx, value in enumerate(pohang_top3.values):
    plt.text(idx, value, value, ha='center')


# 파란점-상위 3개의 읍면동
# 빨간점-포항시 북구 '흥해읍 환승센터' & '장량동 행정복지센터'(인구 多)

# In[49]:


#포항시 북구
import folium
center = [36.0768402, 129.3872069]

m = folium.Map(location=center, zoom_start=10)
m = folium.Map(location=[36.0768402, 129.3872069],
               zoom_start=17, 
               width=750, 
               height=500
              )
tooltip=['장량동','흥해읍','우창동']
for i in range(len(latitude2)):
    folium.Marker([latitude2[i], longitude2[i]],
                        color='tomato',
                        radius = 100, 
                        icon=folium.Icon('blue'),
                        tooltip=tooltip[i]).add_to(m)
tooltip=['장량동 행정복지센터','흥해읍 환승센터']
for i in range(len(tooltip)):
    folium.Marker([lat_po[i], long_po[i]],
                        color='tomato',
                        radius = 100, 
                        icon=folium.Icon('tomato'),
                        tooltip=tooltip[i]).add_to(m)
m


# 셔틀버스 출발: <흥해읍 환승센터> - <장량동 행정복지센터>
