from datetime import datetime, timedelta
from obspy.clients.fdsn import Client
from obspy import UTCDateTime

class WaveformFetcher:
  def __init__(self, provider=None, network=None, station=None, location=None, channel=None):
    if provider == None:
      provider = "NCEDC"  # N. California Earthquake Data Center
    if network == None:
      network = "NC"      # Northern California
    if station == None:
      station = "JSFB"    # Stanford Station
    # if location == None:
    #   location = "00"     # Basically an index for co-located sensors.
    if channel == None:
      channel = "EHZ"     # Extremely Short Period High Gain Z-Oriented

    self.provider = provider
    self.network = network
    self.station = station
    self.location = location
    self.channel = channel

    # Initialize the client.
    self.client = Client(provider)
  def fetch_past(self, ms):
    """
    Gets the waveform from the past 'ms' milliseconds to now.
    
    Parameters:
    ms (int): How far back in milliseconds the waveform should start.

    Returns:
    obspy.stream.Stream

    """
    then = UTCDateTime(datetime.now() - timedelta(seconds=ms/1000))
    now = UTCDateTime(datetime.now())
    st = self.client.get_waveforms(self.network, self.station, self.location, self.channel, then, now)
    return st
