# corrective measures
def update(ws, cells):
    if not cells:
        pass
    else:
        ws.update_cells(cells)

for ws in all_worksheets:

    cells = ws.findall('3 X 8-10 Arnie press')
    for c in cells: c.value = '3x8-10 Arnie Press'
    update(ws, cells)

    cells = ws.findall('3x10-12 Bicep Isolation - ez bar curl')
    for c in cells: c.value = '3x10-12 Bicep Isolation - ez Bar Curl'
    update(ws, cells)

    cells = ws.findall('3x10-12 Tricep Isolation - ez bar skull crusher')
    for c in cells: c.value = '3x10-12 Tricep Isolation - ez bar skull crushers'
    update(ws, cells)

    cells = ws.findall('3x6-8 incline press (bb)')
    for c in cells: c.value = '3x6-8 Incline Press - Barbell'
    update(ws, cells)


#### Acceptable line graph

import matplotlib.dates as dates

plt.close("all")
df_to_plot = exercises_date_weight_frames["2x10-12 Leg Curls"]
df_to_plot.index = pd.to_datetime(df_to_plot.index, dayfirst=True, infer_datetime_format=True)

df_to_plot = df_to_plot.astype({
    "weight": 'int'})


bar = df_to_plot.plot(figsize=(14, 8), style='.-')

bar.xaxis.set_major_formatter(dates.DateFormatter('%Y/%m/%d'))
bar.xaxis.set_major_locator(dates.DayLocator(interval=14))

bar.get_figure().savefig('plots/' + str("2x10-12 Leg Curls"))