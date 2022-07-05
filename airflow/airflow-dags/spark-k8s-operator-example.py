
"""
This is an example DAG which uses SparkKubernetesOperator and SparkKubernetesSensor.
In this example, we create two tasks which execute sequentially.
The first task is to submit sparkApplication on Kubernetes cluster(the example uses spark-pi application).
and the second task is to check the final state of the sparkApplication that submitted in the first state.
Spark-on-k8s operator is required to be already installed on Kubernetes
https://github.com/GoogleCloudPlatform/spark-on-k8s-operator
https://github.com/HPEEzmeral/airflow-on-k8s/blob/ecp-5.3.0/example_dags/example_spark_kubernetes_operator.py
https://github.com/HPEEzmeral/airflow-on-k8s/blob/ecp-5.3.0/example_dags/example_spark_kubernetes_operator_pi.yaml
https://docs.containerplatform.hpe.com/54/reference/kubernetes-applications/spark/run_DAGs_using_spark_operator.html
"""

from datetime import timedelta, datetime

# [START import_module]
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to operate!
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
from airflow.utils.dates import days_ago

# [END import_module]

# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'max_active_runs': 1,
    'retries': 3
}
# [END default_args]

# [START instantiate_dag]

dag = DAG(
    'spark_pi',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    tags=['example']
)


dummy_start = DummyOperator(
    task_id='start',
    dag=dag
)

dummy_end = DummyOperator(
    task_id='end',
    dag=dag
)

submit = SparkKubernetesOperator(
    task_id='spark_pi_submit',
    namespace="default",
    application_file="example_spark_kubernetes_operator_pi.yaml",
    kubernetes_conn_id="kubernetes_default",
    do_xcom_push=True,
    dag=dag,
    
)

dummy_start >>  submit >> dummy_end
