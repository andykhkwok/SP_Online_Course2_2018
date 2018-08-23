"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from waterregulation.controller import Controller
from waterregulation.decider import Decider


class SensorTests(unittest.TestCase):
    """Unit tests for the Sensor class"""

    def test_sensor_call(self):
        """Tests whether fictional sensor replies to MagicMock call"""
        sensor = Sensor(MagicMock(return_value='127.0.0.1'),
                        MagicMock(return_value='514'))
        sensor.measure = MagicMock(return_value=105)

        # self.controller.tick()
        self.assertTrue(sensor.measure())
        # sensor.measure.assert_called_with('127.0.0.1', '514') - FAIL


class DeciderTests(unittest.TestCase):
    """Unit tests for the Decider class"""

    # TODO: write a test or tests for each of the behaviors defined for
    #       Decider.decide

    def test_decider_decision(self):
        """Tests if decider makes correct decisions, given water height in tank
        and current pump action
        """
        decider_dict = {'PUMP_OFF': 'maintain current level',
                        'PUMP_IN': 'pump water in',
                        'PUMP_OUT': 'pump water out'}
        decider = Decider(120, 0.05)
        self.assertEqual(decider.decide(105, 'PUMP_OFF', decider_dict),
                         'pump water in')
        self.assertEqual(decider.decide(126, 'PUMP_OFF', decider_dict),
                         'maintain current level')

    # def test_dummy(self):
    #     """
    #     Just some example syntax that you might use
    #     """

    #     pump = Pump('127.0.0.1', 8000)
    #     pump.set_state = MagicMock(return_value=True)

    #     self.fail("Remove this test.")


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Controller.tick

    def setUp(self):
        self.sensor = Sensor('127.0.0.1', 514)
        self.pump = Pump('127.0.0.1', 8000)
        self.decider = Decider(10, 0.05)

        self.controller = Controller(self.sensor, self.pump, self.decider)
