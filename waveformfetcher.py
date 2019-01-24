from datetime import datetime, timedelta
from obspy.clients.fdsn import Client
from obspy import UTCDateTime, read

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
  def fetch_past(self, ms, type="FDSN"):
    """
    Depending on type, gets the waveform from the past 'ms' milliseconds to now or the whole day.
    
    Parameters:
    ms (int): How far back in milliseconds the waveform should start.
    type (str): "FDSN" | "DART" . "FDSN" uses the FDSN Web Service Specification and retrieves data from past ms while "DART" uses the NCEDC DART web url and retrieves daily data. 

    Returns:
    obspy.stream.Stream

    """
    then = datetime.now() - timedelta(seconds=ms/1000)
    now = datetime.now()
    st = None

    if type == "FDSN":
      st = self.client.get_waveforms(self.network, self.station, self.location, self.channel, then, now)
      how_long_it_took = datetime.now() - now
    if type == "DART":
      if self.provider == "NCEDC":
        # Get necessary information to construct the URL
        year = now.year
        day_of_year = str(now.timetuple().tm_yday).zfill(3)

        # Construct the URL.
        # Long, but we figured it out through inference.
        url = f"http://service.ncedc.org/DART/{self.network}/{self.station}.{self.network}/{self.channel}..D/{self.station}.{self.network}.{self.channel}..D.{year}.{day_of_year}"

        st = read(url)
        how_long_it_took = datetime.now() - now

    # print(f"Time from past ({type}) (h:mm:ss): {how_long_it_took}")
    return st
