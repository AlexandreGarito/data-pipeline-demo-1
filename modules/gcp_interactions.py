"""Module for all the interactions with GCP for the project"""


from google.cloud import secretmanager


def get_secret(project_id, secret_name):
    """
    This function connects to the GCP Secret Manager and get the value of a secret.
    The connection is made through a GCP authentication Client allowing for automated
    credentials retrieving with, in this case, either GOOGLE_APPLICATION_CREDENTIALS
    environment variable if run locally or attached service account if run in GCP.

    Args:
        project_id (str): the GCP project ID
        secret_name (str): the secret name inside GCP Secret Manager

    Returns:
        str: The secret value
    """

    client = secretmanager.SecretManagerServiceClient()
    path_secret_name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=path_secret_name)
    secret_value = response.payload.data.decode("UTF-8")
    return secret_value
