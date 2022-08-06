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