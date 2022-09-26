import pandas as pd
import altair as alt
import gspread

class ChartGenerator():
    def __init__(self, ws: gspread.worksheet):
        self.ws = ws

    @staticmethod
    def chart_style() -> dict:
        return {
            'background':'#161619', 'axis': (alt.Axis(labelColor='#666666', titleColor='#ffffff', gridColor='#131316'))
        }

    @staticmethod
    def quant_title(title: str) -> str:
        return title + ':Q'

class ChartGeneratorLeftRight(ChartGenerator):
    def __init__(self, ws: gspread.worksheet):
        self.ws = ws
        super().__init__(ws)

    def make_chart(self, L_index: int, R_index: int) -> alt.Chart:
        title, df = self._load_data(L_index, R_index)

        _transformed = self._transform(df)
        chart = _transformed.mark_line(point = True).encode(
            self._get_X(),
            self._get_Y(title),
            color='key:N'
        ).properties(
            width=1000,
        )

        return chart

    def make_chart_hover(self, L_index: int, R_index: int) -> alt.Chart:
        title, df = self._load_data(L_index, R_index)

        highlight = alt.selection(type='single', on='mouseover',
                            fields=['key'], nearest=True, empty='none')

        _transformed  = self._transform(df)

        chart = _transformed.mark_line().encode(
            self._get_X(),
            self._get_Y(title),
            color='key:N',
            size=alt.condition(~highlight, alt.value(1), alt.value(3))
        ).properties(
            width=1000,
        )

        points = _transformed.mark_point(opacity=1, filled=True).encode(
            x='date:T',
            y='value:Q',
            color='key:N'
        ).add_selection(
            highlight
        )

        return chart + points

    def make_chart_with_hover_tool_tip(self, L_index: int, R_index: int) -> alt.Chart:
        title, df = self._load_data(L_index, R_index)
        title_q = self.quant_title(title)

        nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['date'], empty='none')

        _transformed = self._transform(df)

        line = _transformed.mark_line().encode(
            self._get_X(),
            self._get_Y(title),
            color='key:N',
            tooltip = ['date', 'value:Q']
        ).properties(
            width=1000,
        )

        selectors = _transformed.mark_point().encode(
            x=self._get_X(),
            opacity=alt.value(0),
        ).add_selection(nearest)

        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        text = line.mark_text(align='left', dx=5, dy=-5).encode(
            text=alt.condition(nearest, 'value:Q', alt.value(' '))
        )

        rules = _transformed.mark_rule(color='gray').encode(
            x=self._get_X(),
        ).transform_filter(nearest)

        chart = alt.layer(
            line, selectors, points, rules, text
        ).properties(
            width=1500,
            height=350
        ).configure(**self.chart_style())

        return chart

    def _load_data(self, L_index: int, R_index: int) -> tuple[str, pd.DataFrame]:
        date = self.ws.col_values(1)
        L = self.ws.col_values(L_index)
        R = self.ws.col_values(R_index)

        title = str(L[0]).split(' ')[0]

        df = pd.DataFrame(
            {
                "date": date[1:],
                "L": L[1:],
                "R": R[1:]
            }
        )

        df["L"] = pd.to_numeric(df["L"])
        df["R"] = pd.to_numeric(df["R"])

        df = df[df['L'] != 0]

        df['date'] = pd.to_datetime(df['date'], dayfirst=True)

        return title, df
    
    @staticmethod
    def _get_X() -> alt.X:
        return alt.X('date:T', timeUnit='yearmonthdate', sort='-x', title='date', axis= alt.Axis(grid=True))

    @staticmethod
    def _get_Y(title: str) -> alt.Y:
        return alt.Y('value:Q', scale=alt.Scale(zero=False), title = title + ' Size (cm)', impute=alt.ImputeParams(frame=[-1, 1], method='mean'))

    @staticmethod
    def _transform(df: pd.DataFrame) -> alt.Chart:
            return alt.Chart(df).transform_fold(['L', 'R'])

class ChartGeneratorSingle(ChartGenerator):
    def __init__(self, ws: gspread.worksheet):
        self.ws = ws
        super().__init__(ws)

    def make_chart(self, index: int, withImpute: bool = True) -> alt.Chart:
        title, df = self.load_data(index)
        chart = alt.Chart(df).mark_line(point = True).encode(
            self._get_X(),
            self._get_Y(title, withImpute),
            color=alt.value('#e9702b')
        ).properties(
            width=1500,
            height=250
        ).configure(**self.chart_style())

        return chart

    def make_chart_with_tool_tip(self, index: int, withImpute: bool = True) -> alt.Chart:
        title, df = self.load_data(index)

        chart = alt.Chart(df).mark_line(point = True).encode(
            self._get_X(),
            self._get_Y(title, withImpute),
            tooltip = ['date', title]
        ).properties(
            width=1500,
            height=250
        )

        return chart
    
    def make_chart_with_hover_tool_tip(self,index: int, withImpute: bool = True) -> alt.Chart:
        title, df = self.load_data(index)
        title_q = self.quant_title(title)

        nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['date'], empty='none')

        line = alt.Chart(df).mark_line().encode(
            self._get_X(),
            self._get_Y(title, withImpute),
            tooltip = ['date', title]
        )

        selectors = alt.Chart(df).mark_point().encode(
            x=self._get_X(),
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        text = line.mark_text(align='left', dx=5, dy=-5).encode(
            text=alt.condition(nearest, title_q, alt.value(' '))
        )

        rules = alt.Chart(df).mark_rule(color='gray').encode(
            x=self._get_X(),
        ).transform_filter(nearest)

        chart = alt.layer(
            line, selectors, points, rules, text
        ).properties(
            width=1500,
            height=250
        ).configure(**self.chart_style())

        return chart

    def load_data(self, index: int) -> tuple[str, pd.DataFrame]:
        date = self.ws.col_values(1)
        val = self.ws.col_values(index)
        
        title = str(val[0])

        df = pd.DataFrame(
            {
                "date": date[1:],
                title: val[1:]
            }
        )

        df['date'] = pd.to_datetime(df['date'], dayfirst=True)
        df[title] = pd.to_numeric(df[title])
        df = df[df[title] != 0]

        return title, df

    @staticmethod
    def _get_X() -> alt.X:
        return alt.X('date:T', timeUnit='yearmonthdate', sort='-x', title='date', axis= alt.Axis(grid=False))

    def _get_Y(self, title: str, withImpute: bool) -> alt.Y:
        # weight chart throws JS error with impute, not sure why
        if withImpute:
            return alt.Y(self.quant_title(title), scale=alt.Scale(zero=False), title = title, impute=alt.ImputeParams(frame=[-1, 1], method='mean'))
        else:
            return alt.Y(self.quant_title(title), scale=alt.Scale(zero=False), title = title)

