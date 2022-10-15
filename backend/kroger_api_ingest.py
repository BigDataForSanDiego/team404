import requests
from requests.auth import HTTPBasicAuth
from requests_oauth2client import BearerToken
from requests_oauth2client import OAuth2Client
from requests_oauth2client import OAuth2ClientCredentialsAuth

import base64
import os
import inspect

kroger_token_url = "https://api.kroger.com/v1/connect/oauth2/token?grant_type=client_credentials&scope=product.compact"
kroger_base_url = "https://api.kroger.com/v1/"

client_id = os.environ['KROGER_CLIENT_ID']
client_secret = os.environ['KROGER_CLIENT_SECRET']

scope_endpoint = "product.compact"

def get_oauthclient(token_url, client_id, client_secret):
  oauth2client = OAuth2Client(
    token_endpoint = token_url,
    auth =(client_id, client_secret)
  )
  return oauth2client

def get_location_session(oauth):
  auth = OAuth2ClientCredentialsAuth(
    oauth
  )
  session = requests.Session()
  session.auth = auth 
  return session

def query_location_from_session(session, zipcode, radiusInMiles = None, limit = None):
  #TODO: input validation
  payload = {"filter.zipCode.near": str(zipcode)}  
  
  if limit != None:
    payload['filter.limit'] = str(limit) 
  if radiusInMiles != None:
    payload['filter.radiusInMiles'] = str(radiusInMiles)

  resp = session.get(kroger_base_url+"/locations", params=payload)
  return resp


if __name__ == "__main__":
  authclient = get_oauthclient(kroger_token_url, client_id, client_secret)
  req = get_location_session(authclient)

  #do the query from the api here
  response = query_location_from_session(req, 92128, limit=10)
  print(response.json())
