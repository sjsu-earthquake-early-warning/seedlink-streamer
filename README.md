# seedlink-streamer README

This script requires one to set up a Python3 Virtual Environment with packages shown below.

* Python3 Virtual Environment Packages Required
  * `pip3 install obspy`
  * `pip3 install boto3`
  * `pip3 install numpy`
  * `pip3 install torch`
  * `pip3 install waveformfetcher`

After setting up Python Virtual Environment.
* source activate your environment if you haven't already
* clone this repository: `git clone https://github.com/sjsu-earthquake-early-warning/seedlink-streamer.git`
* navigate to seedlink-streamer folder
* type in `python3 index.py` to start the script
  * if you want to run the script in the background type in `nohup python3 index.py &`
  * To kill the process type `ps` to list the processes
  * Then type `kill PID(PID being the number of the process` to stop it.
