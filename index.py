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
    FunctionName='taiTest',
    InvocationType='RequestResponse',    # Invoke synchronously (just for dev purposes)
    # InvocationType='Event',              # Invoke asynchronously (we don't need to wait)
    Payload=payload
  )
  print(response['Payload'].read())

def main():
  # Initialize boto3, fetcher
  client = boto3.client('lambda')
  fetcher = waveformfetcher.WaveformFetcher()

  # To simulate continuous fetching,
  for x in range(1):
    st = fetcher.fetch_past(1, type="DART")
    data = list(map(lambda x: int(x), st.data.tolist()))
    ###datatest = "tester"
    # data = list(map(lambda x: int(x), st[0].data.tolist())) #removed this to fix: TypeError: 'float' object is not iterable

    # send data to lambda function
    send_to_lambda(client, data)

if __name__ == '__main__':
  main()
