import json

from google.cloud import bigquery
from google.oauth2 import service_account

from .base import BaseDataWareouseAdapter


class BigQueryAdapter(BaseDataWareouseAdapter):
    def __init__(self, config):
        self.config = config
        with open(self.config["keyfile"], "r") as keyfile:
            keyfile_content = json.load(keyfile)
        credentials = service_account.Credentials.from_service_account_info(
            keyfile_content
        )
        self.client = bigquery.Client(
            credentials=credentials, project=self.config["project"]
        )

    def execute(self, sql):
        try:
            query_job = self.client.query(sql)
            result = query_job.result()
            return [dict(row) for row in result], result.schema
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, []

    def close(self):
        # BigQuery client does not require explicit close
        pass
