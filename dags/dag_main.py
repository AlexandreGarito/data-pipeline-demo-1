from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from main import (
    screener_call,
    screener_transf,
    fte_call,
    add_fte,
    yest_sent_call,
    add_yest_sent,
    write_data_to_csv,
    conn_to_psql,
    upload_to_psql,
    close_conn_to_sql,
    dashboard,
    ROW_LIMIT
)


default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 3, 6, 2),  # start at 2am every day
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG("my_dag", default_args=default_args, schedule_interval="0 2 * * *") as dag:

    run_bash_entrypoint = BashOperator(
        task_id="run_my_entrypoint",
        bash_command="bash my_entrypoint.sh",
    )


    screener_resp_tech, screener_resp_com = PythonOperator(
        task_id="screener_call",
        python_callable=screener_call,
        op_kwargs={"row_limit": ROW_LIMIT},
    )

    tickers_list, filtered_screener = PythonOperator(
        task_id="screener_transf",
        python_callable=screener_transf,
        op_kwargs={
            "row_limit": ROW_LIMIT,
            "screener_resp_tech": screener_resp_tech.output,
            "screener_resp_com": screener_resp_com.output,
        },
    )

    employees_n_list = PythonOperator(
        task_id="fte_call",
        python_callable=fte_call,
        op_kwargs={"tickers_list": tickers_list.output},
    )

    added_fte = PythonOperator(
        task_id="add_fte",
        python_callable=add_fte,
        op_kwargs={
            "employees_n_list": employees_n_list.output,
            "filtered_screener": filtered_screener.output,
        },
    )

    d_list_sentiment = PythonOperator(
        task_id="yest_sent_call",
        python_callable=yest_sent_call,
        op_kwargs={"tickers_list": tickers_list.output},
    )

    final_data = PythonOperator(
        task_id="add_yest_sent",
        python_callable=add_yest_sent,
        op_kwargs={
            "added_fte": added_fte.output,
            "d_list_sentiment": d_list_sentiment.output,
        },
    )

    write_data = PythonOperator(
        task_id="write_data_to_csv",
        python_callable=write_data_to_csv,
        op_kwargs={"final_data": final_data.output},
    )

    pool, connector = PythonOperator(
        task_id="conn_to_psql",
        python_callable=conn_to_psql,
    )

    upload_to_psql = PythonOperator(
        task_id="upload_to_psql",
        python_callable=upload_to_psql,
        op_kwargs={"pool": pool.output},
    )

    close_conn = PythonOperator(
        task_id="close_conn_to_sql",
        python_callable=close_conn_to_sql,
        op_kwargs={
            "pool": pool.output,
            "connector": connector.output,
        },
    )

    generate_dashboard = PythonOperator(
        task_id="dashboard",
        python_callable=dashboard,
    )
    run_bash_entrypoint >> screener_resp_tech, screener_resp_com >> tickers_list
    tickers_list >> employees_n_list >> added_fte >> final_data >> write_data
    tickers_list >> d_list_sentiment >> final_data
    write_data >> pool >> upload_to_psql >> close_conn >> generate_dashboard
