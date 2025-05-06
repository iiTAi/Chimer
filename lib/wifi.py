from network import (
    WLAN,
    STA_IF,
    STAT_CONNECTING,
    STAT_GOT_IP,
    STAT_CONNECT_FAIL,
    STAT_WRONG_PASSWORD,
)
from time import sleep


WAIT_TIME = 10


class WiFi:
    """Class to manage WiFi connection

    This class is used to connect to a WiFi network using the Raspberry Pi Pico 2 W.
    """

    def __init__(
            self,
            ssid: str,
            password: str,
            initial_connect: bool = True,) -> None:
        """Constructor

        Args:
            ssid (str): wlan ssid
            password (str): wlan password
            initial_connect (bool, optional): if True, connect to the wlan immediately. Defaults to True.
        """
        self.ssid = ssid
        self.password = password
        self.wlan = WLAN(STA_IF)
        if initial_connect:
            self.connect()

    def connect(self) -> bool:
        """Connect to the WiFi network

        Returns:
            bool: True if connected, False otherwise

        Note:
            This method will be called after the object is created.
        """
        print("Connecting to WiFi...")
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        if self.__check_status():
            print(f"IP Address: {self.wlan.ifconfig()[0]}")
            return True
        else:
            return False
        
    def disconnect(self) -> None:
        """Disconnect from the WiFi network
        """
        print("Disconnecting from WiFi...")
        self.wlan.disconnect()
        self.wlan.active(False)
        print("Disconnected from WiFi")

    def is_connected(self) -> bool:
        """Check if the device is connected to the WiFi network

        Returns:
            bool: True if connected, False otherwise
        """
        return self.wlan.isconnected()
    
    def __check_status(self) -> bool:
        """Check the status of the WiFi connection

        Returns:
            bool: True if connected, False otherwise

        Note:
            This method will be called while connecting to the WiFi network.
        """
        for _ in range(WAIT_TIME):
            status = self.wlan.status()
            if status == STAT_CONNECTING:
                print("Connecting...")
            elif status == STAT_GOT_IP:
                print("Connected to WiFi")
                return True
            elif status == STAT_CONNECT_FAIL:
                print("Connection failed")
                return False
            elif status == STAT_WRONG_PASSWORD:
                print("Wrong password")
                return False
            else:
                print(f"Unknown status: {status}")
                return False
            sleep(1)
        print("Connection timed out")
        return False