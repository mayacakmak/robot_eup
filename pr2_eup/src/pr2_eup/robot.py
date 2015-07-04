from interface import Interface
from location_db import LocationDb
from sound_db import SoundDb
from navigation import Navigation
from voice import Voice
from event_monitor import EventMonitor
from pr2_eup.msg import InterfaceParams
from pr2_eup.msg import InterfaceSubmission
import rospy
import tf
import time

class RobotFactory(object):
    def build(self):
        """Builds a robot object.

        Returns: Robot. A robot object.
        """

        # Navigation
        tf_listener = tf.TransformListener()
        location_db = LocationDb('dummy', _tf_listener)
        navigation = Navigation(location_db, tf_listener)

        # Interface
        interface = Interface()

        # Speech and sounds
        sound_db = SoundDb('dummy')
        voice = Voice(sound_db)

        # Head
        head = Head()

        # Arms
        arms = Arms()

        robot = Robot(interface, navigation, tf_listener)
        return robot

class Robot(object):
    def __init__(self, interface, navigation):
        self.interface = interface
        self.navigation = navigation

    @staticmethod
    def start(action_function, **kwargs):
        monitor = EventMonitor(
            target=action_function,
            kwargs=kwargs)
        monitor.start()
        return monitor

    @staticmethod
    def wait(action_monitor):
        return action_monitor.join()

    @staticmethod
    def do(action_function, **kwargs):
        monitor = EventMonitor(
            target=action_function,
            kwargs=kwargs)
        monitor.start()
        return Robot.wait(monitor)

    @staticmethod
    def wait_for_event(function, timeout):
        """Calls the given function, but bounds the time by the given timeout.
    
        The function will be called with no arguments. If it returns before the
        timeout, then this function will return event_complete=True and the result
        of the function. Otherwise, this function will return (False, None).

        Args:
          function: function. A no-argument function to call.
          timeout: float. The time, in seconds, to wait for the function to return.
        """
        import signal
    
        class TimeoutError(Exception):
            pass
    
        def handler(signum, frame):
            raise TimeoutError()
    
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(timeout)
        event_complete = False
        result = None
        try:
            result = function()
            event_complete = True
        except TimeoutError as exc:
            event_complete = False
            result = None
        finally:
            signal.alarm(0)
    
        return event_complete, result
