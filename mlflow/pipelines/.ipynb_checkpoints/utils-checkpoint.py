from constants import USERNAME, PASSWORD, NAMESPACE, HOST
import requests
import logging


def get_session_cookie():
    session = requests.Session()
    response = session.get(HOST)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"login": USERNAME, "password": PASSWORD}
    session.post(response.url, headers=headers, data=data)
    session_cookie = session.cookies.get_dict()["authservice_session"]

    return session_cookie


def get_or_create_pipeline(
    client,
    pipeline_name: str,
    pipeline_package_path: str,
    version: str,
    pipeline_description: str,
):
    pipeline_id = client.get_pipeline_id(pipeline_name)

    # If no pipeline found by name, create a new pipeline
    # Else get the latest pipeline version
    if pipeline_id is None:
        logging.info(f"Creating a new pipeline: {pipeline_name}")
        pipeline = client.upload_pipeline(
            pipeline_package_path=pipeline_package_path,
            pipeline_name=pipeline_name,
            description=pipeline_description,
        )
    else:
        logging.info(f"Retrieving the existing pipeline: {pipeline_name}")
        pipeline = client.get_pipeline(pipeline_id)

    # Always try to upload a pipeline version.
    pipeline_version = client.upload_pipeline_version(
        pipeline_package_path=pipeline_package_path,
        pipeline_version_name=f"{pipeline_name} {version}",
        pipeline_id=pipeline_id,
    )

    return pipeline_version


def get_or_create_experiment(client, name: str, namespace: str):
    try:
        experiment = client.get_experiment(experiment_name=name, namespace=namespace)
    except Exception:
        logging.info(f"Creating new experiment: {name}")
        experiment = client.create_experiment(experiment_name=name, namespace=namespace)

    return experiment
