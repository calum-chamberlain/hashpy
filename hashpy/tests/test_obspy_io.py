
import unittest

from hashpy import HashPype, HashError
from obspy.core.event import read_events


class TestObsPyIO(unittest.TestCase):
    def basic_test(self):
        event = read_events('data/example.xml')[0]

        # Set configuration at creation with a dict...
        # ...can from file or interactively, etc
        config = {"npolmin": 9,
                  "max_agap": 90,
                  "vmodels": ['data/vz.kds_orig']}

        hp = HashPype(**config)
        hp.input(event, format="OBSPY")
        hp.load_velocity_models()
        hp.generate_trial_data()
        hp.calculate_takeoff_angles()

        pass1 = hp.check_minimum_polarity()
        pass2 = hp.check_maximum_gap()

        if pass1 and pass2:
            hp.calculate_hash_focalmech()
            hp.calculate_quality()
            print(hp.output(format="OBSPY"))  # get obspy event
        else:
            raise HashError("Didn't pass user checks!")


if __name__ == "__main__":
    unittest.main()
