import elasticsearch
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

INDEX = "kunshujo_items"
host = 'search-nakamura196-rgvfh3jsqpal3gntof6o7f3ch4.us-east-1.es.amazonaws.com'

profile_name = "default"
region = "us-east-1"

if profile_name == None:
    es = Elasticsearch([host])
else:

    session = boto3.Session(profile_name=profile_name)
    credentials = session.get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                    region, 'es', session_token=credentials.token)

    es = Elasticsearch(
                hosts=[{'host': host, 'port': 443}],
                http_auth=awsauth,
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection
            )

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

mapping = {
  "mappings": {
    
    "dynamic_templates": [
        {
            "my_dynamic_title_analyzer_conf": {
                "match_mapping_type": "*",
                "match": "_title",
                "mapping": {
                    "analyzer": "my_ja_analyzer_conf",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                }
            }
        }
    ]
  },
  "settings": {
    "analysis": {
      "analyzer": {
        "my_ja_analyzer_conf": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "mode": "search",
          "char_filter": [
            "icu_normalizer",
            "kuromoji_iteration_mark"
          ],
          "filter": [
            "kuromoji_baseform",
            "kuromoji_part_of_speech",
            "ja_stop",
            "lowercase",
            "kuromoji_number",
            "kuromoji_stemmer",
            "asciifolding"
          ]
        }
      }
    }
  }
}

if es.indices.exists(index=INDEX):
    es.indices.delete(INDEX)
es.indices.create(index=INDEX, body=mapping)