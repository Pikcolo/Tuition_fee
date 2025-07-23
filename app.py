import pandas as pd
import plotly.express as px
import dash
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State, ALL
import math

# โหลดข้อมูล
df = pd.read_excel("data/cleaned_tuition_data.xlsx")

# กรองเฉพาะสาขาวิศวกรรมคอมพิวเตอร์, ปัญญาประดิษฐ์, หุ่นยนต์
df = df[df['Faculty'].str.contains("วิศวกรรมคอมพิวเตอร์|วิศวกรรมปัญญาประดิษฐ์|วิศวกรรมหุ่นยนต์", na=False)]

# แปลงเป็นตัวเลขและกรองข้อมูลที่มีค่าเทอม > 0
df['Confirm Tution Fee'] = pd.to_numeric(df['Confirm Tution Fee'], errors='coerce')
df = df[df['Confirm Tution Fee'] > 0]

app = Dash(__name__)
app.title = "MyTCAS Tuition Dashboard"

per_page = 5

app.layout = html.Div([
    html.H1(
        "📊 MyTCAS Dashboard: ค่าใช้จ่ายในการศึกษาวิศวกรรมคอมพิวเตอร์และปัญญาประดิษฐ์",
        style={ 
            "textAlign": "center",
            "fontFamily": "Kanit, sans-serif",
            "color": "#003366",
            "marginTop": "20px",
            "marginBottom": "30px",
            "fontWeight": "700",
            "fontSize": "2.5rem",
        }
    ),

    dcc.Tabs(id='tabs', value='tab-graph', children=[
        # Tab 1: Graph
        dcc.Tab(label='กราฟเปรียบเทียบค่าใช้จ่ายในการศึกษา', value='tab-graph', children=[
            html.Div([
                html.Div([
                    html.Label("เลือกประเภทค่าใช้จ่าย:", style={"fontWeight": "600", "fontSize": "16px", "marginBottom": "5px"}),
                    dcc.Dropdown(
                        id='tuition-category-dropdown',
                        options=[
                            {"label": "ค่าเทอม (ต่อภาค)", "value": "ค่าเทอม"},
                            {"label": "ค่าเรียนตลอดหลักสูตร", "value": "ค่าเรียนตลอดหลักสูตร"}
                        ],
                        value="ค่าเทอม",
                        clearable=False,
                        style={"width": "280px", "borderRadius": "8px", "marginTop": "5px"}
                    ),
                ], style={"flex": "1", "minWidth": "280px", "marginRight": "20px"}),

                html.Div([
                    html.Label("เลือกมหาวิทยาลัยเพื่อเปรียบเทียบ (เลือกได้หลายแห่ง):", style={"fontWeight": "600", "fontSize": "16px", "marginBottom": "5px"}),
                    dcc.Dropdown(
                        id='university-dropdown',
                        multi=True,
                        placeholder="เลือกมหาวิทยาลัย",
                        style={"width": "500px", "borderRadius": "8px", "marginTop": "5px"}
                    ),
                ], style={"flex": "2", "minWidth": "300px"}),
            ], style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "flex-start",
                "marginBottom": "30px",
                "flexWrap": "wrap",
                "gap": "15px",
                "padding": "0 20px"
            }),

            dcc.Graph(id="tuition-graph", config={"displayModeBar": False}, style={"height": "700px"}),

            html.Div(id='pagination-container', style={
                "textAlign": "center",
                "marginTop": "25px",
                "marginBottom": "40px",
                "display": "flex",
                "justifyContent": "center",
                "gap": "10px",
                "flexWrap": "wrap",
            }),

            html.Div(id="stats-container", style={
                "textAlign": "center",
                "fontSize": "16px",
                "color": "#444",
                "fontWeight": "600",
                "marginBottom": "40px"
            }),
        ]),

        # Tab 2: Pie Chart
        dcc.Tab(label='จำนวนหลักสูตรที่เปิดสอน', value='tab-pie', children=[
            html.Div([
                dcc.Graph(
                    id='program-count-pie',
                    figure=px.pie(
                        df.groupby('University')['Program'].nunique()
                        .sort_values(ascending=False)
                        .head(10)
                        .reset_index(name='Program Count'),
                        names='University',
                        values='Program Count',
                        title='Top 10 มหาวิทยาลัยที่เปิดหลักสูตรด้านวิศวกรรมคอมพิวเตอร์และปัญญาประดิษฐ์มากที่สุด',
                    ).update_traces(
                        textinfo='label+value',
                        hovertemplate='%{label}<br>จำนวนหลักสูตรทั้งหมด: %{value} หลักสูตร',
                        marker=dict(line=dict(color='#fff', width=1))
                    ).update_layout(
                        showlegend=True,
                        margin={"t": 60, "b": 60, "l": 40, "r": 40},
                        height=600
                    )
                )
            ], style={"padding": "30px"})
        ]),

        # Tab 3: Table
        dcc.Tab(label='ตารางข้อมูลค่าเทอม', value='tab-table', children=[
            html.Div([
                html.Label("เลือกประเภทค่าใช้จ่าย:", style={"fontWeight": "600", "fontSize": "16px", "marginBottom": "5px"}),
                dcc.Dropdown(
                    id='table-category-dropdown',
                    options=[
                        {"label": "ค่าเทอม (ต่อภาค)", "value": "ค่าเทอม"},
                        {"label": "ค่าเรียนตลอดหลักสูตร", "value": "ค่าเรียนตลอดหลักสูตร"}
                    ],
                    value="ค่าเทอม",
                    clearable=False,
                    style={"width": "300px", "marginBottom": "15px", "borderRadius": "8px"}
                ),

                html.Label("เลือกมหาวิทยาลัย (หลายแห่งได้):", style={"fontWeight": "600", "fontSize": "16px", "marginBottom": "5px"}),
                dcc.Dropdown(
                    id='table-university-dropdown',
                    multi=True,
                    placeholder="เลือกมหาวิทยาลัย",
                    style={"width": "600px", "marginBottom": "25px", "borderRadius": "8px"}
                ),

                dash_table.DataTable(
                    id='tuition-table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=[],
                    filter_action="native",
                    sort_action="native",
                    page_size=10,
                    style_table={'overflowX': 'auto', 'maxWidth': '100%'},
                    style_cell={
                        'textAlign': 'left',
                        'padding': '8px',
                        'fontFamily': 'Kanit, sans-serif',
                        'fontSize': '14px',
                        'minWidth': '100px',
                    },
                    style_header={
                        'backgroundColor': '#004080',
                        'color': 'white',
                        'fontWeight': '700',
                        'fontSize': '15px',
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f9f9f9',
                        }
                    ],
                ),

                html.Div(id="table-stats", style={"marginTop": "25px", "fontSize": "16px", "color": "#444", "fontWeight": "600"}),
            ], style={"padding": "20px 40px"})
        ])
    ])
])


# ---------- Callbacks ----------
@app.callback(
    Output("university-dropdown", "options"),
    Input("tuition-category-dropdown", "value")
)
def update_university_options(selected_category):
    filtered = df[df['Tuition Category'] == selected_category]
    universities = filtered['University'].dropna().unique()
    return [{"label": u, "value": u} for u in sorted(universities)]


@app.callback(
    Output("tuition-graph", "figure"),
    Output("pagination-container", "children"),
    Output("stats-container", "children"),
    Input("tuition-category-dropdown", "value"),
    Input("university-dropdown", "value"),
    Input({'type': 'page-button', 'index': ALL}, 'n_clicks'),
    State({'type': 'page-button', 'index': ALL}, 'index')
)
def update_graph(selected_category, selected_universities, n_clicks_list, index_list):
    ctx = dash.callback_context
    selected_page = 1
    if ctx.triggered and ctx.triggered[0]['prop_id'].split('.')[0].startswith("{"):
        import json
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        triggered_prop = json.loads(triggered_id)
        selected_page = triggered_prop['index']

    filtered = df[df['Tuition Category'] == selected_category]
    if selected_universities:
        filtered = filtered[filtered['University'].isin(selected_universities)]

    univs = sorted(filtered['University'].dropna().unique())
    if selected_universities:
        filtered_page = filtered
    else:
        start = (selected_page - 1) * per_page
        end = start + per_page
        univs_page = univs[start:end]
        filtered_page = filtered[filtered['University'].isin(univs_page)]

    fig = px.bar(
        filtered_page,
        x="University",
        y="Confirm Tution Fee",
        color="Program",
        barmode="group",
        hover_data=["Campus", "Program"],
        title=f"ค่า{'เทอม' if selected_category == 'ค่าเทอม' else 'เรียนตลอดหลักสูตร'}ของสาขาวิศวกรรมคอมพิวเตอร์และวิศวกรรมปัญญาประดิษฐ์",
        labels={"Confirm Tution Fee": "ค่าใช้จ่าย (บาท)", "University": "มหาวิทยาลัย"},
    )
    fig.update_layout(xaxis_tickangle=-45, height=700)

    buttons = []
    total_pages = math.ceil(len(univs) / per_page)
    for i in range(1, min(total_pages, 5) + 1):
        style = {
            "margin": "3px",
            "padding": "8px 16px",
            "fontWeight": "600",
            "border": "1.5px solid #0074D9",
            "borderRadius": "6px",
            "cursor": "pointer",
            "backgroundColor": "#0074D9" if i == selected_page else "white",
            "color": "white" if i == selected_page else "#0074D9",
            "userSelect": "none",
            "transition": "background-color 0.3s ease, color 0.3s ease",
        }
        buttons.append(
            html.Button(str(i), id={'type': 'page-button', 'index': i}, n_clicks=0, style=style)
        )

    if len(filtered_page) > 0:
        stats_text = (
            f"ข้อมูล {filtered_page['Confirm Tution Fee'].count()} รายการ | "
            f"เฉลี่ย: {filtered_page['Confirm Tution Fee'].mean():,.0f} บาท | "
            f"มัธยฐาน: {filtered_page['Confirm Tution Fee'].median():,.0f} บาท | "
            f"สูงสุด: {filtered_page['Confirm Tution Fee'].max():,.0f} บาท | "
            f"ต่ำสุด: {filtered_page['Confirm Tution Fee'].min():,.0f} บาท"
        )
    else:
        stats_text = "ไม่มีข้อมูลสำหรับการแสดงสถิติ"

    return fig, buttons, stats_text


@app.callback(
    Output("table-university-dropdown", "options"),
    Input("table-category-dropdown", "value")
)
def update_table_university_options(selected_category):
    filtered = df[df['Tuition Category'] == selected_category]
    universities = filtered['University'].dropna().unique()
    return [{"label": u, "value": u} for u in sorted(universities)]


@app.callback(
    Output("tuition-table", "data"),
    Output("table-stats", "children"),
    Input("table-category-dropdown", "value"),
    Input("table-university-dropdown", "value")
)
def update_table(selected_category, selected_universities):
    filtered = df[df['Tuition Category'] == selected_category]
    if selected_universities:
        filtered = filtered[filtered['University'].isin(selected_universities)]
    data = filtered.to_dict('records')

    if len(filtered) > 0:
        stats_text = (
            f"ข้อมูล {filtered['Confirm Tution Fee'].count()} รายการ | "
            f"เฉลี่ย: {filtered['Confirm Tution Fee'].mean():,.0f} บาท | "
            f"มัธยฐาน: {filtered['Confirm Tution Fee'].median():,.0f} บาท | "
            f"สูงสุด: {filtered['Confirm Tution Fee'].max():,.0f} บาท | "
            f"ต่ำสุด: {filtered['Confirm Tution Fee'].min():,.0f} บาท"
        )
    else:
        stats_text = "ไม่มีข้อมูลสำหรับการแสดงสถิติ"

    return data, stats_text


if __name__ == "__main__":
    app.run(debug=True)
