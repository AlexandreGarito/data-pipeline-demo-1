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

    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div(
        style={"backgroundColor": "#1F2630"},
        children=[
            html.Br(),
            html.H1(
                "Super Data Explorer",
                style={
                    "padding-top": "0px",
                    "padding-left": "20px",
                    "padding-bottom": "20px",
                    "backgroundColor": "#1F2630",
                    "font-family": "league spartan",
                    "color": "#77A4D1",
                    "font-weight": "bold",
                    "font-size": 25,
                },
            ),
            html.H3(
                """github repo : https://github.com/AlexandreGarito/data-pipeline-demo-1""",
                style={
                    "textAlign": "center",
                    "backgroundColor": "#1F2630",
                    "font-family": "league spartan",
                    "color": "#c2d6ea",
                    "font-weight": "bold",
                    "font-size": 20,
                    "padding": "15px 100px 0px 100px",
                },
            ),
            html.H3(
                """The objective of this web app is to demonstrate my ability to extract, transform, load and show in a 
                dashboard a simple set of API data updated daily. This serves as a small "A to Z project" in my data 
                engineering path where I get to experience the constraints of using data from the ETL phase all the way to 
                its use in a pseudo-final product, including some DevOps processes and tools such as CI/CD, Docker and 
                Airflow.""",
                style={
                    "textAlign": "left",
                    "backgroundColor": "#1F2630",
                    "font-family": "league spartan",
                    "color": "#c2d6ea",
                    "font-weight": "bold",
                    "font-size": 13,
                    "padding": "15px 100px 0px 100px",
                },
            ),
                        html.H3(
                """The pipeline is coded in Python.
                Data is extracted with API requests, transformed using pandas, loaded into a GCP Cloud SQL PostgreSQL 
                database, and showcased using the Dash-Plotly web framework (based on Flask).
                The app is run in a Docker container on Google Cloud Platform (GCP). With GCP Cloud Build, the code is 
                automatically pulled from the github repo with each new commit, built as a Docker image, and the container 
                deployed on GCP Cloud Run. At the start of the container, tests are run with pytest, then the data 
                extraction scripts are called, then the Dash-Plotly app and webserver is called.
                Each day at 2AM, a GCP Cloud Composer (managed Airflow) task reboots the container to update daily data.""",
                style={
                    "textAlign": "left",
                    "backgroundColor": "#1F2630",
                    "font-family": "league spartan",
                    "color": "#c2d6ea",
                    "font-weight": "bold",
                    "font-size": 13,
                    "padding": "15px 100px 0px 100px",
                },
            ),
                        html.H3(
                """Free and easily accessible API data was prioritized to facilitate long-term stability of the pipeline,
                so it mostly focuses on the biggest companies of the Technology field.""",
                style={
                    "textAlign": "left",
                    "backgroundColor": "#1F2630",
                    "font-family": "league spartan",
                    "color": "#c2d6ea",
                    "font-weight": "bold",
                    "font-size": 13,
                    "padding": "15px 100px 0px 100px",
                },
            ),
                        html.H3(
                """My original idea was to use the data of those companies by crossing their market capitalization, their 
                number of employees, and their daily current job offerings to give a ranking of these companies when it 
                comes to market cap per employee and market cap per job offer. This would've been a simple approach to find 
                the "best-capitalized job offers" by company. Unfortunately, I realized that daily job offering data is 
                quite tricky to obtain, often paid and often incomplete. So I decided to replace it with Twitter social 
                media sentiment, a data source simple to obtain and also updated daily. Now the dashboard would show the 
                "best-capitalized workforce + social media sentiment". Since the Twitter API ceased to be freely accessible 
                in february 2023, I had to switch to Reddit social sentiment, which is unfortunately more scarce than 
                Twitter sentiment, but it's still the best option I have for now without having to redesign the entire 
                social sentiment part of the pipeline.""",
                style={
                    "textAlign": "left",
                    "backgroundColor": "#1F2630",
                    "font-family": "league spartan",
                    "color": "#c2d6ea",
                    "font-weight": "bold",
                    "font-size": 13,
                    "padding": "15px 100px 0px 100px",
                },
            ),
                        html.H3(
                """As of march 2023, this dashboard is more about being a working small technical demo than anything else, 
                but I intend to update and enrich the dashboard with more useful data as I progress on my data engineering 
                path.""",
                style={
                    "textAlign": "left",
                    "backgroundColor": "#1F2630",
                    "font-family": "league spartan",
                    "color": "#c2d6ea",
                    "font-weight": "bold",
                    "font-size": 13,
                    "padding": "15px 100px 0px 100px",
                },
            ),
            html.H3(
                "Made by Alexandre Garito",
                style={
                    "padding-top": "5px",
                    "padding-left": "20px",
                    "backgroundColor": "#1F2630",
                    "font-family": "league spartan",
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
                            font_family="League Spartan",
                        )
                        .update_traces(
                            hovertemplate=" <b>%{label}</b><br><br>Market Capitalization : %{value}<extra></extra>"
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
                            font_family="League Spartan",
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
                            title="Capitalization per Employee & Sentiment",
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
                                normalized_sentiment="Reddit Sentiment",
                                marketCap="Market Capitalization ($)",
                            ),
                        ).update_layout(
                            scene_camera=camera,
                            font_size=10,
                            font_color="#ffffff",
                            paper_bgcolor="#252E3F",
                            font_family="League Spartan",
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
                            title="Capitalization per Employee & Sentiment",
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
                                normalized_sentiment="Reddit Sentiment",
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
                            font_family="League Spartan",
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
                title="Capitalization per Employee & Sentiment",
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
                    normalized_sentiment="Reddit Sentiment",
                    marketCap="Market Capitalization ($)",
                ),
            ).update_layout(
                scene_camera=camera,
                font_size=10,
                font_color="#ffffff",
                paper_bgcolor="#252E3F",
                font_family="League Spartan",
            )

            scatter_data["data"][0]["marker"]["color"] = "green"

            not_highlighted_df = df[df["companyName"] != company_name]

            not_highlighted_data = px.scatter_3d(
                not_highlighted_df,
                x="fullTimeEmployees",
                y="normalized_sentiment",
                z="marketCap",
                title="Capitalization per Employee & Sentiment",
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
                    normalized_sentiment="Reddit Sentiment",
                    marketCap="Market Capitalization ($)",
                ),
            ).update_layout(
                scene_camera=camera,
                font_size=10,
                font_color="#ffffff",
                paper_bgcolor="#252E3F",
                font_family="League Spartan",
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
                    title="Capitalization per Employee & Sentiment",
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
                        normalized_sentiment="Reddit Sentiment",
                        marketCap="Market Capitalization ($)",
                    ),
                )
                .update_layout(
                    yaxis2=dict(title="Another Y-axis", overlaying="y", position=0.85),
                    font_size=10,
                    font_color="#ffffff",
                    paper_bgcolor="#252E3F",
                    font_family="League Spartan",
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
                    title="Capitalization per Employee & Sentiment",
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
                        normalized_sentiment="Reddit Sentiment",
                        marketCap="Market Capitalization ($)",
                    ),
                )
                .update_layout(
                    yaxis2=dict(title="Another Y-axis", overlaying="y", position=0.85),
                    font_size=10,
                    font_color="#ffffff",
                    paper_bgcolor="#252E3F",
                    font_family="League Spartan",
                )
                .update_yaxes(tickprefix="$")
            )

            scatter_data.add_traces(not_highlighted_data["data"])

            return scatter_data

    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port)
    # app.run_server(host='0.0.0.0', port=8050)
