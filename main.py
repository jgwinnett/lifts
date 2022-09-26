from altair import Chart
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import chart_generator as cg
from sheets import Sheets

app = FastAPI()
sheets = Sheets("creds/lifts-service.json")
ws = sheets.getWorkSheet()
lr = cg.ChartGeneratorLeftRight(ws)
single = cg.ChartGeneratorSingle(ws)

class SheetParamsSingle(BaseModel):
    index: int
    style: str

class SheetParamsLR(BaseModel):
    index_L: int
    index_R: int
    style: str 

@app.post("/charts/single")
def get_chart(sheetParam: SheetParamsSingle):
    chart: Chart

    match sheetParam.style:
        case 'chart':
            chart = single.make_chart(sheetParam.index)
        case 'hover':
            chart = single.make_chart_with_hover_tool_tip(sheetParam.index)
        case 'tooltip':
            chart = single.make_chart_with_tool_tip(sheetParam.index)
        case _:
            raise HTTPException(status_code=400, detail="Bad style type requested")

    if (chart):
        return chart.to_json()
    else:
        raise HTTPException(status_code=500, detail="Somethings gone wrong")

@app.post("/charts/LR")
def get_chart(sheetParam: SheetParamsLR):
    chart: Chart

    match sheetParam.style:
        case 'chart':
            chart = lr.make_chart(sheetParam.index_L, sheetParam.index_R)
        case 'hover':
            chart = lr.make_chart_with_hover_tool_tip(sheetParam.index_L, sheetParam.index_R)
        case 'tooltip':
            chart = lr.make_chart_with_tool_tip(sheetParam.index_L, sheetParam.index_R)
        case _:
            raise HTTPException(status_code=400, detail="Bad style type requested")

    if (chart):
        return chart.to_json()
    else:
        raise HTTPException(status_code=500, detail="Somethings gone wrong")