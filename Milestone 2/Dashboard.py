# ::::::::::::::::::::::::::::::::::::::::::::::: Libraries :::::::::::::::::::::::::::::::::::::::::::::::
import numpy as np
import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, Input, Output, callback

external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"]

# :::::::::::::::::::::::::::::::::::::::::::::: Loading Data :::::::::::::::::::::::::::::::::::::::::::::
main_data = "Data/Data After Milestone 1.csv"
original_data = "Data/Original Data.csv"
sales = pd.read_csv(main_data, encoding="latin-1")
main = pd.read_csv(original_data, encoding="latin-1")

# ::::::::::::::::::::::::::::::::::::::::::::::: Variables :::::::::::::::::::::::::::::::::::::::::::::::
root = {
    "text"        : "#2d3748",
    "text2"       : "#1d4ed8",
    "text3"       : "#64748b",
    "background1" : "#f8fafc",
    "background2" : "#e2e8f0",
    "primary"     : "#3b82f6",
    "secondary"   : "#9ebfd6",
    "accent"      : "#2ea2dc"
}

total_revenue = sales["Total_sales"].sum().round(2)
total_profit = sales["Profit"].sum().round(2)
total_units_sold = sales["Quantity"].sum().round(2)
avg_discount = (main["Discount"].mean() * 100).round(2)
total_orders = sales["Order Date"].count()
avg_shipping_time = sales["Shipping Time (Days)"].mean().round(2)

fig1_DataPickerRange = dcc.DatePickerRange(
    id='fig1_DataPickerRange',
    start_date=sales['Order Date'].min(),
    end_date=sales['Order Date'].max(),
    display_format='YYYY-MM-DD', 
    className="fig1_DataPickerRange"
)
fig1_Dropdown = dcc.Dropdown(
    id='fig1_Dropdown',
    options=[
        {'label': 'Sales', 'value': 'Sales'},
        {'label': 'Profit', 'value': 'Profit'}
    ],
    value='Sales', 
    className="fig1_Dropdown"
)
fig1_Slider = dcc.Slider(
    id='fig1_Slider',
    min=7,
    max=30,
    step=7,
    marks={7: '7D', 14: '14D', 30: '30D'},
    value=7,
    className="fig1_Slider"
)
fig1 = dcc.Graph(id='fig1', className="fig1")

fig2_Dropdown = dcc.Dropdown(
    id="fig2_Dropdown",
    options=[
        {"label": "Region", "value": "Region"},
        {"label": "Market", "value": "Market"},
        {"label": "Country", "value": "Country"}
    ],
    value="Country",
    className="fig2_Dropdown"
)
fig2_Radioitems = dcc.RadioItems(
    id="fig2_Radioitems",
    options=[
        {"label": "Sales", "value": "Total_sales"},
        {"label": "Profit", "value": "Profit"},
    ],
    value="Total_sales",
    className="fig2_Radioitems",
    inline=True
)
fig2 = dcc.Graph(id="fig2", className="fig2")

fig3_Dropdown1 = dcc.Dropdown(
    id='fig3_Dropdown1',
    options=[
        {'label': 'Horizontal Bar Chart', 'value': 'bar'},
        {'label': 'Treemap', 'value': 'treemap'}
    ],
    value='bar',
    clearable=False,
    className='fig3_Dropdown1'
)
fig3_DropDown = dcc.Dropdown(
    id= 'fig3_DropDown',
    options=[
        {'label':'Sales' ,'value':'Sales'},
        {'label':'Profit' ,'value':'Profit'},
        {'label':'Quantity' ,'value':'Quantity'}
    ],
    value='Sales',
    className='fig3_Dropdown'
)
fig3_checkList = dcc.Checklist(
    id='fig3_checkList',
    options=[{'label': cat, 'value': cat} for cat in sales['Category'].unique()],
    value=["Technology", "Furniture", "Office Supplies"],
    className='fig3_checkList',
    inputStyle={"margin-right": "5px", "margin-left": "5px"},
    labelStyle={"display": "block"}
)
fig3 = dcc.Graph(id='fig3', className="fig3")

fig4_Radioitems = dcc.RadioItems(
    id='fig4_Radioitems',
    options=[
        {'label': 'Day of Week vs. Month', 'value': 'heatmap'},
        {'label': 'Monthly Trends', 'value': 'line'}
    ],
    value='heatmap',
    className="fig4_Radioitems",
    inline=True
)
fig4_Dropdown = dcc.Dropdown(
    id='fig4_Dropdown',
    options=[{'label': cat, 'value': cat} for cat in sales['Category'].unique()],
    value=sales['Category'].unique()[0],
    className="fig4_Dropdown",
    clearable=False
)
fig4 = dcc.Graph(id='fig4', className="fig4")

fig5_RangeSlider = dcc.RangeSlider(
    id='fig5_RangeSlider',
    min=main['Discount'].min(),
    max=main['Discount'].max(),
    step=0.05,
    marks={i: f"{i:.1f}" for i in np.arange(0, 1.01, 0.2) if main['Discount'].min() <= i <= main['Discount'].max()},
    value=[main['Discount'].min(), main['Discount'].max()],
    className="fig5_RangeSlider"
)
fig5_Dropdown = dcc.Dropdown(
    id='fig5_Dropdown',
    options=[{'label': 'All', 'value': 'All'}] + [{'label': cat, 'value': cat} for cat in sales['Category'].unique()],
    value='All',
    className="fig5_Dropdown",
    clearable=False
)
fig5 = dcc.Graph(id='fig5', className="fig5")

# ::::::::::::::::::::::::::::::::::::::::::::::: App Layout ::::::::::::::::::::::::::::::::::::::::::::::
app = Dash(__name__, external_stylesheets = external_stylesheets)

app.layout = html.Div([
    html.H1("Sales Dashboard", className="title"),
    html.Div([
        html.Div([
            html.H3("Total Revenue", className="s_h3"),
            html.H2([html.Span("$"), f"{total_revenue}"])
        ], className="summary_div"),
        html.Div([
            html.H3("Total Profit", className="s_h3"),
            html.H2([html.Span("$"), f"{total_profit}"])
        ], className="summary_div"),
        html.Div([
            html.H3("Total Units Sold", className="s_h3"),
            html.H2([html.Span("$"), f"{total_units_sold}"])
        ], className="summary_div"),
        html.Div([
            html.H3("Average Discount", className="s_h3"),
            html.H2([html.Span("%"), f"{avg_discount}"])
        ], className="summary_div"),
        html.Div([
            html.H3("Total Orders", className="s_h3"),
            html.H2([f"{total_orders}", html.Span("order")])
        ], className="summary_div"),
        html.Div([
            html.H3("AVG Shipping Time", className="s_h3"),
            html.H2([f"{avg_shipping_time}", html.Span("days")])
        ], className="summary_div"),
    ], id="first_row"),
    html.Br(),
    html.Hr(),
    html.Br(),
    html.Div([
        html.H2("Sales & Profit Over Time"),
        html.Div([
            html.Div([
                html.Div([
                    fig1_DataPickerRange,
                    fig1_Dropdown,
                    fig1_Slider,
                ], className="controls")
            ], className="control_bar"),
            html.Div([
                fig1
            ], className="chart"),
            # html.Div([
            #     html.Div([]),
            #     html.Div([]),
            # ], className="insights"),
        ], className="content"),
    ], id="second_row"),
    html.Br(),
    html.Br(),
    html.Div([
        html.H2("Sales by Region, Market or Country"),
        html.Div([
            html.Div([
                html.Div([
                    fig2_Dropdown, 
                    fig2_Radioitems
                ], className="controls")
            ], className="control_bar"),
            html.Div([
                fig2
            ], className="chart"),
            # html.Div([
            #     html.Div([]),
            #     html.Div([]),
            # ], className="insights"),
        ], className="content"),
    ], id="third_row"),
    html.Br(),
    html.Br(),
    html.Div([
        html.H2("Top Performing Products and Categories"),
        html.Div([
            html.Div([
                html.Div([
                    fig3_Dropdown1,
                    fig3_DropDown,
                    fig3_checkList,
                ], className="controls")
            ], className="control_bar"),
            html.Div([
                fig3
            ], className="chart"),
            # html.Div([
            #     html.Div([]),
            #     html.Div([]),
            # ], className="insights"),
        ], className="content"),
    ], id="fourth_row"),
    html.Br(),
    html.Br(),
    html.Div([
        html.H2("Seasonality & Time Patterns"),
        html.Div([
            html.Div([
                html.Div([
                    fig4_Dropdown,
                    fig4_Radioitems,
                ], className="controls")
            ], className="control_bar"),
            html.Div([
                fig4
            ], className="chart"),
            # html.Div([
            #     html.Div([]),
            #     html.Div([]),
            # ], className="insights"),
        ], className="content"),
    ], id="fifth_row"),
    html.Br(),
    html.Br(),
    html.Div([
        html.H2("Discount Impact on Profit"),
        html.Div([
            html.Div([
                html.Div([
                    fig5_RangeSlider,
                    fig5_Dropdown
                ], className="controls")
            ], className="control_bar"),
            html.Div([
                fig5
            ], className="chart"),
            # html.Div([
            #     html.Div([]),
            #     html.Div([]),
            # ], className="insights"),
        ], className="content"),
    ], id="sixth_row"),
    html.Br(),
], id="body")

# :::::::::::::::::::::::::::::::::::::::::::::: Callbacks ::::::::::::::::::::::::::::::::::::::::::::::
@callback(
    Output('fig1', 'figure'),
    [Input('fig1_DataPickerRange', 'start_date'),
    Input('fig1_DataPickerRange', 'end_date'),
    Input('fig1_Slider', 'value'),
    Input('fig1_Dropdown', 'value')]
)
def update_graph(start_date, end_date, ma_window, measure):
    filtered_df = sales[(sales['Order Date'] >= start_date) & (sales['Order Date'] <= end_date)].copy()
    filtered_df = filtered_df.sort_values('Order Date')
    filtered_df['Moving_Avg'] = filtered_df[measure].rolling(window=ma_window).mean()
    
    fig1 = px.line(filtered_df, x='Order Date', y='Moving_Avg', title=f'{measure} Over Time', line_shape='linear', line_dash_sequence=['solid'], color_discrete_sequence=["#3b82f6"])

    fig1.update_layout(
        plot_bgcolor = root['background1'],
        paper_bgcolor = root['background2'],
        font_color = root['text'],
        xaxis_title='Order Date',
        yaxis_title=measure,
        template='plotly_dark',
        hovermode='x unified',
        title_x=0.5,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    if measure == "Profit":
        fig1.update_layout(yaxis=dict(range=[sales["Profit"].min(), sales["Profit"].max()]))
    return fig1

@callback(
    Output("fig2", "figure"),
    [Input("fig2_Dropdown", "value"), 
    Input("fig2_Radioitems", "value")]
)
def update_sales_by_region(selected_category, selected_metric):
    if selected_category == "Country":
        grouped_df = sales.groupby("Country")[selected_metric].sum().reset_index()

        fig2 = px.choropleth(
            grouped_df,
            locations="Country",
            locationmode="country names",
            color=selected_metric,
            title=f"{selected_metric} by Country",
            color_continuous_scale=["#93c5fd", "#60a5fa", "#3b82f6", "#2563eb", "#1d4ed8"]
        )
    else:
        grouped_df = sales.groupby(selected_category)[selected_metric].sum().reset_index()

        fig2 = px.bar(
            grouped_df,
            x=selected_category,
            y=selected_metric,
            title=f"{selected_metric} by {selected_category}",
            text_auto=True,
            color=selected_metric,
            color_continuous_scale=["#93c5fd", "#60a5fa", "#3b82f6", "#2563eb", "#1d4ed8"]
        )
    fig2.update_layout(
        plot_bgcolor=root["background1"],
        paper_bgcolor=root["background2"],
        font_color=root["text"],
        xaxis_title=selected_category if selected_category != "Country" else "Country",
        yaxis_title=selected_metric,
        title_x=0.5,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig2

@callback(
    Output("fig3", "figure"),
    [
        Input("fig3_Dropdown1", "value"),
        Input("fig3_DropDown", "value"),
        Input("fig3_checkList", "value")
    ]
)
def update_graph3(chart_type, measure, selected_categories):
    filtered_df = sales[sales['Category'].isin(selected_categories)]

    grouped_df = filtered_df.groupby(['Category', 'Sub-Category'])[measure].sum().reset_index()

    if chart_type == 'treemap':
        fig3 = px.treemap(
            grouped_df,
            path=['Category', 'Sub-Category'],
            values=measure,
            color=measure,
            title=f'{measure} by Category and Sub-Category'
        )
    else:
        fig3 = px.bar(
            grouped_df,
            x=measure,
            y='Sub-Category',
            orientation='h',
            color=measure,
            text_auto=True,
            title=f'{measure} by Category and Sub-Category',
            color_continuous_scale=["#93c5fd", "#60a5fa", "#3b82f6", "#2563eb", "#1d4ed8"]
        )

    fig3.update_layout(
        plot_bgcolor=root['background1'],
        paper_bgcolor=root['background2'],
        font_color=root['text'],
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    return fig3

@callback(
    Output('fig4', 'figure'),
    [Input('fig4_Radioitems', 'value'),
    Input('fig4_Dropdown', 'value')]
)
def update_seasonality(view_type, category):
    filtered_df = sales[sales['Category'] == category].copy()
    filtered_df['Order Date'] = pd.to_datetime(filtered_df['Order Date'])
    filtered_df['Month'] = filtered_df['Order Date'].dt.strftime('%b')
    filtered_df['Day of Week'] = filtered_df['Order Date'].dt.day_name()
    
    if view_type == 'heatmap':
        pivot_table = filtered_df.pivot_table(index='Day of Week', columns='Month', values='Total_sales', aggfunc='sum')
        fig4 = px.imshow(
            pivot_table,
            labels=dict(x="Month", y="Day of Week", color="Sales"),
            title=f"Sales Heatmap for {category}",
            color_continuous_scale=["#93c5fd", "#60a5fa", "#3b82f6", "#2563eb", "#1d4ed8"]
        )
    else:
        monthly_sales = filtered_df.groupby('Month')['Total_sales'].sum().reset_index()
        fig4 = px.line(
            monthly_sales,
            x='Month',
            y='Total_sales',
            title=f"Monthly Sales Trend for {category}",
            color_discrete_sequence=['#3b82f6']
        )
    
    fig4.update_layout(
        plot_bgcolor=root['background1'],
        paper_bgcolor=root['background2'],
        font_color=root['text'],
        template='plotly_dark',
        title_x=0.5,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig4

@callback(
    Output('fig5', 'figure'),
    [Input('fig5_RangeSlider', 'value'),
    Input('fig5_Dropdown', 'value')]
)
def update_discount_impact(selected_discount_range, selected_category):
    filtered_df = sales[
        (sales['Discount'] >= selected_discount_range[0]) & 
        (sales['Discount'] <= selected_discount_range[1])
    ].copy()

    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]

    fig5 = px.scatter(
        filtered_df,
        x='Discount',
        y='Profit',
        color='Profit',
        title="Impact of Discount on Profit",
        trendline="ols",
        color_continuous_scale=["#93c5fd", "#60a5fa", "#3b82f6", "#2563eb", "#1d4ed8"]
    )

    fig5.update_traces(marker=dict(size=8))

    fig5.update_layout(
        plot_bgcolor=root['background1'],
        paper_bgcolor=root['background2'],
        font_color=root['text'],
        xaxis_title='Discount',
        yaxis_title='Profit',
        template='plotly_dark',
        title_x=0.5,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig5


# ::::::::::::::::::::::::::::::::::::::::::::::: Run App :::::::::::::::::::::::::::::::::::::::::::::::
if __name__ == "__main__":
    app.run(debug=True, port=2020)