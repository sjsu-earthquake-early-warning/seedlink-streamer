#!usr/bin/python
import waveformfetcher
import boto3
import json
import time
import numpy
import torch
from torch import nn
import torch.nn.functional as F

# Define the model (from gh)
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=32, kernel_size=21, padding=10)
        self.conv2 = nn.Conv1d(in_channels=32, out_channels=64, kernel_size=15, padding=7)
        self.conv3 = nn.Conv1d(in_channels=64, out_channels=128, kernel_size=11, padding=5)
        
        self.batchnorm32 = nn.BatchNorm1d(num_features=32)
        self.batchnorm64 = nn.BatchNorm1d(num_features=64)
        self.batchnorm128 = nn.BatchNorm1d(num_features=128)
        self.batchnorm512 = nn.BatchNorm1d(num_features=512)
        
        self.fc1 = nn.Linear(4736, 512)
        self.fc2 = nn.Linear(512, 512)
        self.fc3 = nn.Linear(512, 2)
        
        self.maxpool = nn.MaxPool1d(kernel_size=2, stride=2)     
        
        self.dropout2d = nn.Dropout2d(p=0.5)
        self.dropout = nn.Dropout(p=0.5)
    def forward(self, x):
        x = self.conv1(x.unsqueeze(1))
        x = F.relu(self.batchnorm32(x))
        x = self.maxpool(x)
        
        x = self.conv2(x)
        x = F.relu(self.batchnorm64(x))
        x = self.maxpool(x)
        
        x = self.conv3(x)
        x = F.relu(self.batchnorm128(x))
        x = self.maxpool(x)
        
        # Flatten input for fully connected layers
        x = x.view(x.shape[0], -1) 
        
        x = self.dropout(self.fc1(x))
        x = F.relu(self.batchnorm512(x))
        
        x = self.dropout(self.fc2(x))
        x = F.relu(self.batchnorm512(x))
        
        x = F.log_softmax(self.fc3(x), dim=1)
        return x

# Load model, parallelize, and set to eval mode
# NOTE: Must parallelize: see https://discuss.pytorch.org/t/solved-keyerror-unexpected-key-module-encoder-embedding-weight-in-state-dict/1686
model = CNN()
def parallelize(model):
  device_ids = [i for i in range(torch.cuda.device_count())]
  model = torch.nn.DataParallel(model, device_ids=device_ids)
  return model
model = parallelize(model)
model.load_state_dict(torch.load('./model.pth', map_location='cpu'))
model.eval()

def send_to_lambda(client, data, pred):
  # Format data
  payload = {
    "data": data,
    "pred": pred
  }
  payload = json.dumps(payload).encode('utf-8')

  print(payload)

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
    st = fetcher.fetch_past(3000, type="DART") # first parameter does nothing unless it's FDSN
    data_list = list(map(lambda x: int(x), st.data.tolist()))

    # data = list(map(lambda x: int(x), st[0].data.tolist())) #removed this to fix: TypeError: 'float' object is not iterable

    data_numpy = numpy.array(data_list[0:300])
    data_numpy = numpy.expand_dims(data_numpy, axis=2)
    data_tensor = torch.from_numpy(data_numpy).type(torch.float).transpose(0, 1)

    log_probs = model.forward(data_tensor)
    probs = torch.exp(log_probs)

    top_p, top_class = probs.topk(1, dim=1)

    # send data to lambda function
    send_to_lambda(client, data_list, top_class[0][0].item())

if __name__ == '__main__':
  while True:
     try:
       main()
     except:
       pass
     time.sleep(3)

