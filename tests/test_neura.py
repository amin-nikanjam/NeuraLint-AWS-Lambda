import unittest
import os
os.chdir("tests")
import sys
sys.path.append('..')
from endToEnd import main

os.environ["TEST_MODE"] = "1"

class NeuraTest(unittest.TestCase):
    def test_neura(self):
        desired_output="""mix_bugs_1.py\n\rLayer 1 ==> A learning layer should no longer include a bias when it is followed by batchnorm., The local window size for spatial filtering should generally increase or stay the same throughout the convolutional layers.\n\rLayer 3 ==> Batchnorm layer should be before the dropout.\n\rLayer 6 ==> A learning layer should no longer include a bias when it is followed by batchnorm.\n\rLayer 8 ==> Batchnorm layer should be before the dropout.\n\rLayer 12 ==> A learning layer should no longer include a bias when it is followed by batchnorm.\n\rLayer 14 ==> Batchnorm layer should be before the dropout."""
        print('Start testing...')
        output = main("mix_bugs_1.py", [32,28,28,1], [32,10], "tf", "result")
        assert output==desired_output
        print('Testing completed.')


if __name__ == '__main__':
    unittest.main()