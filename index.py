#!usr/bin/python
""" TODO: Invoke Lambda function """

import waveformfetcher
# import boto3
# client = boto3.client('lambda')

def main():
  # Initialize waveform.
  fetcher = waveformfetcher.WaveformFetcher()
  
  # To simulate continuous fetching,
  for x in range(5):
    st = fetcher.fetch_past(10000)
    st.plot()

  # Below is how to invoke a Lambda function.
  # response = client.invoke(
    # FunctionName='string',
    # InvocationType='Event',
    # LogType='None'|'Tail',
    # ClientContext='string',
    # Payload=b'bytes'|file,
    # Qualifier='string'
  # )

  return

if __name__ == '__main__':
  main()