#!usr/bin/python
import waveformfetcher
import boto3
import json

def send_to_lambda(client, data):
  # Format data
  payload = {
    "data": data
  }
  payload = json.dumps(payload).encode('utf-8')

  response = client.invoke(
    FunctionName='hello-world',
    # InvocationType='RequestResponse',    # Invoke synchronously (just for dev purposes)
    InvocationType='Event',              # Invoke asynchronously (we don't need to wait)
    Payload=payload
  )
  # print(response['Payload'].read())

def main():
  # Initalize boto3, fetcher
  client = boto3.client('lambda')
  fetcher = waveformfetcher.WaveformFetcher()

  # To simulate continuous fetching,
  for x in range(1):
    st = fetcher.fetch_past(3000)
    data = list(map(lambda x: int(x), st[0].data.tolist()))
    send_to_lambda(client, data)

  return

if __name__ == '__main__':
  main()
