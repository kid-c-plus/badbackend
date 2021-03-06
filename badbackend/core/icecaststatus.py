import requests
import json
import re
import time

from badbackend.loggers import FileLogger

# -------------
#   Constants
# -------------

# default values all configuration items that can have defaults
# to overwrite these, set their values in the IcecastStatus stanza of
# config.yaml (or the passed-in __init__ config dict if you're just
# importing this module)
DEFAULTS = {
    # length of time, in seconds, to cache data from Icecast 
    # status-json.xsl endpoint
    'cache_timeout' : 5.0,

    # default mountpoint for which to return status, when no
    # argument is provided
    'default_mountpoint'    : "stream"
}

# User-Agent string to use in Icecast status requests. Nice to provide
# this so you can differentiate BadBackend activity from 'requests'
# queries that may indicate someone doing something unsavory to your
# Icecast server
USERAGENT = "Bad Backend"


class IcecastStatus():
    """Class tracking and providing up-to-date status on a provided 
    Icecast server. All data access methods trigger refresh if more than
    `cache_timeout` seconds old

    Methods
    -------
    check_show_running(mountpoint=None) : str
        Returns true if a show is currently airing on the specified
    get_show_name(mountpoint=None) : str
        Returns the name of the currently running show on the specified
        mountpoint, according to the `status-json.xsl` endpoint of the 
        provided Icecast server
    get_song_name(mountpoint=None) : str
        Returns the name of the currently playing song on the specified
        mountpoint, according to the `status-json.xsl` endpoint of the 
        provided Icecast server
    """

    class _CachedServerStatus:
        """Private internal class providing cached server status. This 
        is the object that actually queries the server, so it recieves
        the config object from the parent IcecastStatus (after the 
        DEFAULTS have been added to it).

        Methods
        -------
        get_mountpoint(mountpoint: str) : dict
            Returns Icecast's status-json.xsl status entry for provided
            mountpoint. Automatically refreshes cache if data is older
            than cache timeout value
        """

        def __init__(self, config: dict):
            """Pass IcecastStatus config dict to _CachedServerStatus,
            as it will query the server for up-to-date status."""
            self.config = config
            self.server_status = []
            self.status_timestamp = 0

            self._update_status()

        def _update_status(self):
            """pull new status into self.server_status field and update 
            self.status_timestamp"""

            status_resp = requests.get("%s/status-json.xsl" % 
                self.config['server_url'], 
                headers={'User-Agent': USERAGENT})

            
            if status_resp.status_code == 200:
                status_text = re.sub("([^\\\\])([\"\']): *- *,([\"\'])",
                    "\\1\\2:\"-\",\\3", status_resp.text)
    
                status_obj = json.loads(status_text)
                if ('icestats' in status_obj 
                    and 'source' in status_obj['icestats']):
                    # when multiple mountpoints are present, they're 
                    # collected into a JSON array

                    status = status_obj['icestats']['source']
                    self.server_status = (status 
                        if type(status) == type([]) else [status]
                    self.status_timestamp = time.time()

            else: 
                FileLogger.error("Error querying Icecast server status:
                    %s" % status_resp.text)

        def get_mountpoint(self, mountpoint: str) -> dict:
            """Return the up-to-date status info for the provided 
            mountpoint, or an empty dict if the mountpoint is not 
            found"""

            if (time.time() - self.status_timestamp >= 
                float(self.config['cache_timeout'])):
                self._update_status()

            mount_status = list(filter(lambda mount_status: (
                mount_status['listenurl'].split("/")[-1]), status))
            return mount_status[0] if len(mount_status) else {} 

    def __init__(self, config: dict):
        """Begin tracking Icecast server specified in `config` input. 
        View the `IcecastStatus` stanza in config.yaml for status 
        on expected config input structure."""
        
        self.config = DEFAULTS.copy()
        self.config.update(config)
        
        self.server_status = _CachedServerStatus(self.config)

    def check_show_running(mountpoint=None) -> bool:
        """Return True if a show is running on the provided mountpoint,
        or the default mountpoint in config.yaml if none provided"""

        return 'stream_start' in self.server_status.get_mountpoint(
            mountpoint if mountpoint else self.config['default_mountpoint'])

    def get_show_name(mountpoint=None) -> str:
        """Return the name of the currently running show on the
        provided mountpoint, or the default mountpoint in config.yaml
        if none provided (returns None if no show running on provided
        mountpoint)"""

        mount_status = self.server_status.get_mountpoint(mountpoint
            if mountpoint else self.config['default_mountpoint'])

        return (mount_status['server_name'] if 'stream_start' in 
            mount_status and 'server_name' in mount_status else None)

    def get_song_name(mountpoint=None) -> str:
        """Return the name of the currently playing song on the
        provided mountpoint, or the default mountpoint in config.yaml
        if none provided (returns None if no show running on provided
        mountpoint)"""

        mount_status = self.server_status.get_mountpoint(mountpoint
            if mountpoint else self.config['default_mountpoint'])

        return (mount_status['title'] if 'stream_start' in mount_status
            and 'title' in mount_status and mount_status['title'] == 
            "none" else None)
