import pandas as pd
import plotly.express as px
import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State, ALL
import math


# โหลดข้อมูล
df = pd.read_excel("data/cleaned_tuition_data.xlsx")

# กรองเฉพาะสาขาคอมพิวเตอร์และเอไอ
df = df[df['Faculty'].str.contains("วิศวกรรมคอมพิวเตอร์|วิศวกรรมปัญญาประดิษฐ์|วิศวกรรมหุ่นยนต์", na=False)]

# แปลงคอลัมน์เป็นตัวเลข และคัดข้อมูลที่มีค่าเทอม
df['Cleaned Tuition Fee'] = pd.to_numeric(df['Cleaned Tuition Fee'], errors='coerce')
df = df[df['Cleaned Tuition Fee'] > 0]

app = Dash(__name__)
app.title = "MyTCAS Dashboard - ค่าเทอมวิศวกรรมคอมพิวเตอร์และวิศวกรรมปัญญาประดิษฐ์"

unique_univs = sorted(df['University'].dropna().unique())
per_page = 5
total_pages = math.ceil(len(unique_univs) / per_page)
max_page_display = 5
max_page = min(total_pages, max_page_display)

app.layout = html.Div([
    html.H1(
        "📊 MyTCAS Dashboard: ค่าเทอมวิศวกรรมคอมพิวเตอร์และวิศวกรรมปัญญาประดิษฐ์",
        style={"textAlign": "center"}
    ),

    html.Div([
        html.Label("เลือกประเภทค่าใช้จ่าย:"),
        dcc.Dropdown(
            id='tuition-category-dropdown',
            options=[
                {"label": "ค่าเทอม (ต่อภาค)", "value": "ค่าเทอม"},
                {"label": "ค่าเรียนตลอดหลักสูตร", "value": "ค่าเรียนตลอดหลักสูตร"}
            ],
            value="ค่าเทอม",
            clearable=False
        ),
    ], style={"width": "300px", "margin": "auto", "marginBottom": "20px"}),

    html.Div([
        html.Label("เลือกมหาวิทยาลัยเพื่อเปรียบเทียบ (เลือกได้หลายแห่ง):"),
        dcc.Dropdown(
            id='university-dropdown',
            multi=True,
            placeholder="เลือกมหาวิทยาลัย"
        )
    ], style={"width": "600px", "margin": "auto", "marginBottom": "20px"}),

    dcc.Graph(id="tuition-graph"),

    # Pagination buttons ใต้กราฟ
    html.Div(id='pagination-container', style={"textAlign": "center", "marginTop": "20px", "marginBottom": "40px"}),

    html.Div(
        "หมายเหตุ: แสดงเฉพาะข้อมูลที่มีตัวเลขค่าใช้จ่ายระบุไว้ชัดเจน",
        style={"textAlign": "center", "marginTop": "10px"}
    )
])

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
    Input("tuition-category-dropdown", "value"),
    Input("university-dropdown", "value"),
    Input({'type': 'page-button', 'index': ALL}, 'n_clicks'),
    State({'type': 'page-button', 'index': ALL}, 'index')
)
def update_graph(selected_category, selected_universities, n_clicks_list, index_list):
    ctx = dash.callback_context

    # กำหนดหน้าเริ่มต้นเป็น 1
    selected_page = 1

    # ถ้ามีการกดปุ่มหน้า ให้เลือกหน้าที่กดล่าสุด
    if ctx.triggered and ctx.triggered[0]['prop_id'].split('.')[0].startswith("{"):
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        import json
        triggered_prop = json.loads(triggered_id)
        selected_page = triggered_prop['index']

    filtered = df[df['Tuition Category'] == selected_category]

    if selected_universities:
        filtered = filtered[filtered['University'].isin(selected_universities)]

    univs = sorted(filtered['University'].dropna().unique())
    per_page = 5

    # ถ้าเลือกมหาวิทยาลัยแบบเจาะจงและไม่ใช่ทั้งหมด ให้แสดงทั้งหมดเลยไม่แบ่งหน้า
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
        y="Cleaned Tuition Fee",
        color="Program",
        barmode="group",
        hover_data=["Campus", "Program"],
        title=f"ค่า{'เทอม' if selected_category == 'ค่าเทอม' else 'เรียนตลอดหลักสูตร'}ของสาขาวิศวกรรมคอมพิวเตอร์และวิศวกรรมปัญญาประดิษฐ์",
        labels={"Cleaned Tuition Fee": "ค่าใช้จ่าย (บาท)", "University": "มหาวิทยาลัย"},
    )
    fig.update_layout(xaxis_tickangle=-45, height=700)

    # สร้างปุ่มเลขหน้า
    buttons = []
    total_pages = math.ceil(len(univs) / per_page)
    max_pages = min(total_pages, max_page_display)

    for i in range(1, max_pages + 1):
        style = {
            "margin": "3px",
            "padding": "8px 14px",
            "fontWeight": "bold",
            "border": "1px solid #0074D9",
            "borderRadius": "4px",
            "cursor": "pointer",
            "backgroundColor": "#0074D9" if i == selected_page else "white",
            "color": "white" if i == selected_page else "#0074D9",
            "userSelect": "none",
        }
        buttons.append(
            html.Button(str(i), id={'type': 'page-button', 'index': i}, n_clicks=0, style=style)
        )

    return fig, buttons


if __name__ == "__main__":
    app.run(debug=True)
