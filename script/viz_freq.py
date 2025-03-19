import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import re


with open("char_res_all.txt",'r',encoding='utf8') as rf:
    text = rf.read().split("\n")
    data = [d.split("\t") for d in text]

with open("../data/corpus/25272.txt", "r", encoding="utf8") as rf:
    jpm_text = rf.read()

chapter_locs = re.finditer(r'第[一二三四五六七八九十百]+回', jpm_text)
chapter_locs = [r.start() for r in chapter_locs]
chapter_locs.append(len(jpm_text))
vals = [0 for i in range(len(jpm_text))]

for d in data:
    loc = int(d[0])
    locations = d[1].split(",")
    vals[loc] = len(locations)

has_data = [0 if c == 0 else 1 for c in vals]
print(sum(has_data)/len(jpm_text))

current_chapter = 1
chapter_data = []
temp_chap = []
for i,val in enumerate(vals):
    if current_chapter <= 100:
        if i < chapter_locs[current_chapter]:
            temp_chap.append(val)
        else:
            chapter_data.append(temp_chap)
            current_chapter += 1
            temp_chap = [val]

chapter_data.append(temp_chap)
    # else:
    #     chapter_data.append(temp_chap)

by_chapter_dived = []
chap_div = []
for c in chapter_data:
    square = math.ceil(math.sqrt(len(c)))


    divided_data = []
    temp_row = []


    for i, d in enumerate(c):
        if i % square == 0 and i > 0:
            divided_data.append(temp_row)
            temp_row = []


        if d > 100:
            d = 100
        if d != 0:
            d = math.log(d) + 1

        temp_row.append(d)

    while len(temp_row) < square:
        temp_row.append(0)

    divided_data.append(temp_row)
    by_chapter_dived.append(divided_data)

fig = make_subplots(rows=10, cols=10, subplot_titles=[f"Chapter {i+1}" for i in range(100)], horizontal_spacing=0.005, vertical_spacing=0.02)

for i,d in enumerate(by_chapter_dived):
    fig.add_trace(go.Heatmap(z=d, coloraxis = "coloraxis"),row=i//10+1, col=i%10+1)
fig.update_layout(title_text='Heatmaps of Shared Text in <i>Jinpingmei</i> by Chapter Across Full Corpus', coloraxis = {'colorscale':'blackbody'})
fig.update_xaxes(showticklabels=False)
fig.update_yaxes(showticklabels=False)
fig.update_annotations(font_size=12)
# fig = px.imshow(by_chapter_dived[0], color_continuous_scale="blackbody")
fig.show()
