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
  def fetch_past(self, ms, type="FDSN"):
    """
    Gets the waveform from the past 'ms' milliseconds to now.
    
    Parameters:
    ms (int): How far back in milliseconds the waveform should start.

    Returns:
    obspy.stream.Stream

    """
    then = UTCDateTime(datetime.now() - timedelta(seconds=ms/1000))
    now = UTCDateTime(datetime.now())

    if type == "FDSN":
        st = self.client.get_waveforms(self.network, self.station, self.location, self.channel, then, now)
    if type == "DART":
		today = UTCDateTime.now().utctimetuple()
		yearAsString = str(today[0])
		dayOfYearAsNum = "{0:0=3d}".format(today[7]) #formats day of year to 3 digits...
		dayOfYearAsString = str(dayOfYearAsNum).zfill(3)
		JSFB_url = "http://service.ncedc.org/DART/NC/JSFB.NC/EHZ..D/JSFB.NC.EHZ..D." + yearAsString + "." + dayOfYearAsString
		
		param_endtime = UTCDateTime().__sub__(14)
		param_starttime = UTCDateTime().__sub__(17)
        st = read(JSFB_url)
		st.trim(param_starttime, param_endtime) #trims to 3 second waveforms between 14 to 17 seconds back in time

    return st
