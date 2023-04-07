"""
This dash_plotly_dashboard module uses a unique function to create an interactive
dashboard webserver with Dash & Plotly libraries.

Function:
    - dashboard : creates a simple dashboard with 3 callbacks for interactivity.
    - render_content_marketcap : Renders the left-side charts representing 
      classifications by market cap.
    - render_content_scatter : Renders the right-side charts representing the
      3 dimensions scatter.
    - update_highlighted_point : Interactivity when cursor is on a given company point.
"""
import os
import logging
from datetime import date, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
from sklearn.preprocessing import MinMaxScaler


def dashboard():
    
    logging.info("Dash Plotly dashboard started.")
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    camera = dict(eye=dict(x=0, y=-2.5, z=0.1))

    df = pd.read_csv("data/final_data.csv")
    df["normalized_sentiment"] = scaler.fit_transform(df[["yest_twitter_mean_sentiment_score"]])
    df["normalized_sentiment"] = df["normalized_sentiment"].round(2)


    external_stylesheets = [
        'https://fonts.googleapis.com/css2?family=Lato&display=swap',
        dbc.themes.SLATE
    ]
    # app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    app = Dash(external_stylesheets=external_stylesheets)
    app.css.config.serve_locally = True

    app.layout = html.Div(
        style={"backgroundColor": "#1F2630"},
        children=[
            html.Br(),
            html.H1(
                "Data pipeline demo 1 : micro ETL and web dashboard on GCP",
                style={
                    "textAlign": "center",
                    "padding-top": "50px",
                    "padding-left": "20px",
                    "padding-bottom": "50px",
                    "backgroundColor": "#1F2630",
                    "font-family": "Lato",
                    "color": "#c2d6ea",
                    "font-weight": "bold",
                    "font-size": 30,
                },
            ),
            html.Div(
                [
                    html.Span("Github repository : "),
                    html.A(
                        "https://github.com/AlexandreGarito/data-pipeline-demo-1",
                        href="https://github.com/AlexandreGarito/data-pipeline-demo-1",
                        target="_blank",
                        style={
                            "color": "#c2d6ea",
                            "text-decoration": "underline",
                        },
                    ),
                ],
                style={
                    "textAlign": "center",
                    "backgroundColor": "#1F2630",
                    "font-family": "Lato",
                    "color": "#c2d6ea",
                    "font-weight": "bold",
                    "font-size": 22, 
                    "padding": "20px 0px 0px 0px",
                },
            ),
            html.Br(),
            html.H3(
                """The purpose of this project is to showcase my ability to employ Python in extracting, transforming, 
                loading, and displaying a simple set of API data within an interactive dashboard that updates daily. 
                This serves as a small "A to Z project" in 
                my data engineering journey, where I can gain experience with some tools and challenges involved in the field. 
                This project also involves some DevOps processes and tools such as CI/CD, Docker, and Airflow.
                Although dashboarding is not a core skill in data engineering, here it serves as an accessory tool that 
                demonstrates the functionality of this pipeline.""",
                style={
                    "textAlign": "left",
                    "backgroundColor": "#1F2630",
                    "font-family": "Lato",
                    "color": "#c2d6ea",
                    "font-weight": "normal",
                    "font-size": 15,
                    "padding": "15px 100px 0px 100px",
                },
            ),
            html.H3(
                """The pipeline is coded in Python. The app is run in a Docker container on Google Cloud Platform (GCP). 
                Data is extracted with API requests, transformed using pandas, loaded into a GCP Cloud SQL PostgreSQL 
                database, and showcased in this dashboard using the Dash-Plotly web framework (based on Flask). 
                With GCP Cloud Build, the code is automatically pulled from the GitHub repo with each new commit, 
                built as a Docker image, and a container is deployed on GCP Cloud Run. At the start of the container, 
                unit tests are run with pytest, then the data 
                extraction scripts are called, then the Dash-Plotly app and web server is called.
                Every day at 2 AM UTC, a GCP Cloud Composer (managed Airflow) DAG triggers a container reboot to 
                refresh the data.""",
                style={
                    "textAlign": "left",
                    "backgroundColor": "#1F2630",
                    "font-family": "Lato",
                    "color": "#c2d6ea",
                    "font-weight": "normal",
                    "font-size": 15,
                    "padding": "15px 100px 0px 100px",
                },
            ),
            html.H3(
                """Free and easily accessible API data was prioritized to facilitate long-term stability of the pipeline,
                so it mostly focuses on the biggest companies in the Technology field.""",
                style={
                    "textAlign": "left",
                    "backgroundColor": "#1F2630",
                    "font-family": "Lato",
                    "color": "#c2d6ea",
                    "font-weight": "normal",
                    "font-size": 15,
                    "padding": "15px 100px 0px 100px",
                },
            ),
            html.H3(
                """My original idea was to use the data of those companies by crossing their market capitalization, their 
                number of employees, and their daily current job offerings to give a ranking of these companies when it 
                comes to market cap per employee and market cap per job offer. This would've been a simple approach to find 
                the "best-capitalized job offers" by company. Unfortunately, I realized that daily job offering data is 
                quite tricky to obtain, often paid and often incomplete. So, I decided to replace it with Twitter social 
                media sentiment, a data source simple to obtain and also updated daily. As a result, the dashboard would 
                display the "best-capitalized workforce" for each company, along with their social media sentiment. Since 
                the Twitter API ceased to be freely accessible in February 2023, the API I used ceased to provide it, and I 
                had to switch to Reddit social sentiment, 
                which is unfortunately more scarce than Twitter sentiment, but it's still the best option I have for now 
                without having to redesign the entire social sentiment part of the pipeline.""",
                style={
                    "textAlign": "left",
                    "backgroundColor": "#1F2630",
                    "font-family": "Lato",
                    "color": "#c2d6ea",
                    "font-weight": "normal",
                    "font-size": 15,
                    "padding": "15px 100px 0px 100px",
                },
            ),
            html.H3(
                """As of March 2023, this dashboard primarily serves as a small working technical demo; however, I am committed to 
                update and enhance the dashboard with more valuable data as I advance in my data engineering journey. Also, 
                I discovered after a few days that Cloud Composer (managed Airflow) is actually somewhat expensive to run for 
                an individual, so I'm rebooting my container with a cheaper GCP Cloud Scheduler cron job from now on.""",
                style={
                    "textAlign": "left",
                    "backgroundColor": "#1F2630",
                    "font-family": "Lato",
                    "color": "#c2d6ea",
                    "font-weight": "normal",
                    "font-size": 15,
                    "padding": "15px 100px 30px 100px",
                },
            ),
            html.H3(
                f"Last data update : {date.today()}",
                style={
                    "textAlign": "right",
                    "padding-top": "0px",
                    "padding-right": "20px",
                    "backgroundColor": "#1F2630",
                    "font-family": "Lato",
                    "color": "#c2d6ea",
                    "font-weight": "bold",
                    "font-size": 10,
                },
            ),
            html.H3(
                "Made by Alexandre Garito",
                style={
                    "padding-top": "0px",
                    "padding-left": "20px",
                    "backgroundColor": "#1F2630",
                    "font-family": "Lato",
                    "color": "#43505b",
                    "font-weight": "bold",
                    "font-size": 10,
                },
            ),
            html.Div(
                [
                    dcc.Tabs(
                        style={"fontWeight": "bold", "color": "#c9c9c9"},
                        id="tabs-marketcap",
                        value="tab-treemap",
                        children=[
                            dcc.Tab(label="Treemap", value="tab-treemap"),
                            dcc.Tab(label="Bar Chart", value="tab-barchart"),
                        ],
                        colors={
                            "border": "#252E3F",
                            "primary": "#3a485b",
                            "background": "#3a485b",
                        },
                    )
                ],
                style={
                    "width": "50%",
                    "display": "inline-block",
                    "backgroundColor": "#1F2630",
                    "padding-top": "0px",
                    "padding-left": "20px",
                    "padding-right": "20px",
                    "padding-bottom": "0px",
                },
            ),
            html.Div(
                [
                    dcc.Tabs(
                        style={"fontWeight": "bold", "color": "#c9c9c9"},
                        id="tabs-scatter",
                        value="tab-3d-scatter",
                        children=[
                            dcc.Tab(label="3D Scatter", value="tab-3d-scatter"),
                            dcc.Tab(label="2D Scatter", value="tab-2d-scatter"),
                        ],
                        colors={
                            "border": "#252E3F",
                            "primary": "#3a485b",
                            "background": "#3a485b",
                        },
                    )
                ],
                style={
                    "width": "50%",
                    "display": "inline-block",
                    "backgroundColor": "#1F2630",
                    "padding-top": "0px",
                    "padding-left": "20px",
                    "padding-right": "20px",
                    "padding-bottom": "0px",
                },
            ),
            html.Div(
                id="tabs-content-marketcap",
                style={
                    "width": "50%",
                    "display": "inline-block",
                    "backgroundColor": "#1F2630",
                    "padding-top": "0px",
                    "padding-left": "20px",
                    "padding-right": "20px",
                    "padding-bottom": "20px",
                },
            ),
            html.Div(
                id="tabs-content-scatter",
                style={
                    "width": "50%",
                    "display": "inline-block",
                    "backgroundColor": "#1F2630",
                    "padding-top": "0px",
                    "padding-left": "20px",
                    "padding-right": "20px",
                    "padding-bottom": "20px",
                },
            ),
        ],
    )


    @app.callback(
        Output("tabs-content-marketcap", "children"), Input("tabs-marketcap", "value")
    )
    def render_content_marketcap(tab):
        if tab == "tab-treemap":
            return html.Div(
                [
                    dcc.Graph(
                        id="graph-market-cap",
                        figure=px.treemap(
                            df,
                            path=["companyName"],
                            values="marketCap",
                            hover_name="companyName",
                            hover_data={"companyName": True, "marketCap": True},
                            color="companyName",
                            color_discrete_sequence=px.colors.qualitative.Alphabet,
                            height=800,
                            template="simple_white",
                            title="Market Capitalization by Company ($)",
                            labels={"marketCap": "Market Capitalization"},
                        )
                        .update_layout(
                            font_size=10,
                            font_color="#ffffff",
                            paper_bgcolor="#252E3F",
                            font_family="Lato",
                        )
                        .update_traces(
                            hovertemplate=" <b>%{label}</b><br><br>Market Capitalization : $%{customdata}<extra></extra>",
                            customdata=[f"{x:,.0f}" for x in df["marketCap"]],
                        )
                        .update_traces(marker=dict(cornerradius=20)),
                    )

                ]
            )
        elif tab == "tab-barchart":
            return html.Div(
                [
                    dcc.Graph(
                        id="graph-market-cap",
                        figure=px.bar(
                            df,
                            x="companyName",
                            y="marketCap",
                            hover_name="companyName",
                            hover_data={"companyName": True, "marketCap": True},
                            color="companyName",
                            color_discrete_sequence=px.colors.qualitative.Alphabet,
                            height=800,
                            title="Market Capitalization by Company ($)",
                            labels={
                                "marketCap": "Market Capitalization",
                                "companyName": "Company Name",
                            },
                            # orientation='h'
                        )
                        .update_layout(
                            font_size=10,
                            font_color="#ffffff",
                            paper_bgcolor="#252E3F",
                            font_family="Lato",
                        )
                        .update_traces(
                            hovertemplate=" <b>%{x}</b><br><br>Market Capitalization : %{y}<extra></extra>"
                        ),
                    )
                ]
            )


    @app.callback(
        Output("tabs-content-scatter", "children"), Input("tabs-scatter", "value")
    )
    def render_content_scatter(tab):
        if tab == "tab-3d-scatter":
            return html.Div(
                [
                    dcc.Graph(
                        id="graph-scatter",
                        figure=px.scatter_3d(
                            df,
                            x="fullTimeEmployees",
                            y="normalized_sentiment",
                            z="marketCap",
                            title="Market Capitalization & Number of Employees & Last 15 days Reddit Sentiment",
                            color="normalized_sentiment",
                            hover_name="companyName",
                            log_x=True,
                            log_z=True,
                            size="normalized_sentiment",
                            height=800,
                            size_max=30,
                            color_continuous_scale="rdbu",
                            labels=dict(
                                companyName="Company Name",
                                fullTimeEmployees="Full Time Employees",
                                normalized_sentiment="Last 15 days Reddit Sentiment",
                                marketCap="Market Capitalization ($)",
                            ),
                        ).update_layout(
                            scene_camera=camera,
                            font_size=10,
                            font_color="#ffffff",
                            paper_bgcolor="#252E3F",
                            font_family="Lato",
                        ),
                    )
                ]
            )
        elif tab == "tab-2d-scatter":
            return html.Div(
                [
                    dcc.Graph(
                        id="graph-scatter",
                        figure=px.scatter(
                            df,
                            x="fullTimeEmployees",
                            y="marketCap",
                            title="Market Capitalization & Full Time Employees & Reddit Sentiment (last 15 days)",
                            color="normalized_sentiment",
                            hover_name="companyName",
                            log_x=True,
                            log_y=True,
                            size="normalized_sentiment",
                            height=800,
                            size_max=30,
                            color_continuous_scale="rdbu",
                            labels=dict(
                                companyName="Company Name",
                                fullTimeEmployees="Full Time Employees",
                                normalized_sentiment="Last 15 days Reddit Sentiment",
                                marketCap="Market Capitalization ($)",
                            ),
                        )
                        .update_layout(
                            yaxis2=dict(
                                title="Another Y-axis", overlaying="y", position=0.85
                            ),
                            font_size=10,
                            font_color="#ffffff",
                            paper_bgcolor="#252E3F",
                            font_family="Lato",
                        )
                        .update_yaxes(tickprefix="$"),
                    )
                ]
            )


    @app.callback(
        Output("graph-scatter", "figure"),
        Input("graph-market-cap", "hoverData"),
        Input("tabs-scatter", "value"),
    )
    def update_highlighted_point(hoverData, tab):
        
        if tab == "tab-3d-scatter":

            # Exception handling below is the only way I found to preserve the interactivity of the charts.
            try:
                company_name = hoverData["points"][0]["label"]
                highlighted_df = df[df["companyName"] == company_name]
            except (KeyError, TypeError):
                company_name = "dummy"
                highlighted_df = df
            
            scatter_data = px.scatter_3d(
                highlighted_df,
                x="fullTimeEmployees",
                y="normalized_sentiment",
                z="marketCap",
                title="Market Capitalization & Full Time Employees & Reddit Sentiment (last 15 days)",
                color="normalized_sentiment",
                hover_name="companyName",
                log_x=True,
                log_z=True,
                size="normalized_sentiment",
                height=800,
                size_max=30,
                color_continuous_scale="rdbu",
                labels=dict(
                    companyName="Company Name",
                    fullTimeEmployees="Full Time Employees",
                    normalized_sentiment="Last 15 days Reddit Sentiment",
                    marketCap="Market Capitalization ($)",
                ),
            ).update_layout(
                scene_camera=camera,
                font_size=10,
                font_color="#ffffff",
                paper_bgcolor="#252E3F",
                font_family="Lato",
            )

            scatter_data["data"][0]["marker"]["color"] = "green"

            not_highlighted_df = df[df["companyName"] != company_name]

            not_highlighted_data = px.scatter_3d(
                not_highlighted_df,
                x="fullTimeEmployees",
                y="normalized_sentiment",
                z="marketCap",
                title="Market Capitalization & Full Time Employees & Reddit Sentiment (last 15 days)",
                color="normalized_sentiment",
                hover_name="companyName",
                log_x=True,
                log_z=True,
                size="normalized_sentiment",
                height=800,
                size_max=30,
                color_continuous_scale="rdbu",
                labels=dict(
                    companyName="Company Name",
                    fullTimeEmployees="Full Time Employees",
                    normalized_sentiment="Last 15 days Reddit Sentiment",
                    marketCap="Market Capitalization ($)",
                ),
            ).update_layout(
                scene_camera=camera,
                font_size=10,
                font_color="#ffffff",
                paper_bgcolor="#252E3F",
                font_family="Lato",
            )

            scatter_data.add_traces(not_highlighted_data["data"])
            
            return scatter_data

        elif tab == "tab-2d-scatter":
            
            # Exception handling below is the only way I found to preserve the interactivity of the charts.
            try:
                company_name = hoverData["points"][0]["label"]
                highlighted_df = df[df["companyName"] == company_name]
            except (KeyError, TypeError):
                company_name = "dummy"
                highlighted_df = df

            scatter_data = (
                px.scatter(
                    highlighted_df,
                    x="fullTimeEmployees",
                    y="marketCap",
                    title="Market Capitalization & Full Time Employees & Reddit Sentiment (last 15 days)",
                    color="normalized_sentiment",
                    hover_name="companyName",
                    log_x=True,
                    log_y=True,
                    size="normalized_sentiment",
                    height=800,
                    size_max=30,
                    color_continuous_scale="rdbu",
                    labels=dict(
                        companyName="Company Name",
                        fullTimeEmployees="Full Time Employees",
                        normalized_sentiment="Last 15 days Reddit Sentiment",
                        marketCap="Market Capitalization ($)",
                    ),
                )
                .update_layout(
                    yaxis2=dict(title="Another Y-axis", overlaying="y", position=0.85),
                    font_size=10,
                    font_color="#ffffff",
                    paper_bgcolor="#252E3F",
                    font_family="Lato",
                )
                .update_yaxes(tickprefix="$")
            )

            scatter_data["data"][0]["marker"]["color"] = "green"

            not_highlighted_df = df[df["companyName"] != company_name]

            not_highlighted_data = (
                px.scatter(
                    not_highlighted_df,
                    x="fullTimeEmployees",
                    y="marketCap",
                    title="Market Capitalization & Full Time Employees & Reddit Sentiment (last 15 days)",
                    color="normalized_sentiment",
                    hover_name="companyName",
                    log_x=True,
                    log_y=True,
                    size="normalized_sentiment",
                    height=800,
                    size_max=30,
                    color_continuous_scale="rdbu",
                    labels=dict(
                        companyName="Company Name",
                        fullTimeEmployees="Full Time Employees",
                        normalized_sentiment="Last 15 days Reddit Sentiment",
                        marketCap="Market Capitalization ($)",
                    ),
                )
                .update_layout(
                    yaxis2=dict(title="Another Y-axis", overlaying="y", position=0.85),
                    font_size=10,
                    font_color="#ffffff",
                    paper_bgcolor="#252E3F",
                    font_family="Lato",
                )
                .update_yaxes(tickprefix="$")
            )

            scatter_data.add_traces(not_highlighted_data["data"])

            return scatter_data

    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port)
    # app.run_server(host='0.0.0.0', port=8050)
