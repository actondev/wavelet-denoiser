import unittest
import subprocess
import os
import sys

class DenoisingWithArgumentsTest(unittest.TestCase):

    testFilePath = "./test/resources/sp01_airport_sn5_44100.wav"
    outFilePath = "./test/artifacts/sp01_airport_sn5_44100_denoised.wav"
    cleanFilePath = "./test/resources/sp01_44100.wav"
    expectedMetricStdOut = "0.9\n"

    def test_running_denoiser_with_arguments(self):
        self.assert_denoise_command_with_argument_works()
        self.assert_denoised_file_metric()

    def assert_denoise_command_with_argument_works(self):
        cmdArgs = [
            "python3",
            "./src/denoiser-argument.py",
            "-i",
            DenoisingWithArgumentsTest.testFilePath,
            "-a",
            "2",
            "-b",
            "1",
            "-c",
            "1",
            "-d",
            "0.1",
            "-akg",
            "0.1",
            "-ako",
            "2",
            "-aks",
            "asc",
            "-type",
            "2",
            "-o",
            DenoisingWithArgumentsTest.outFilePath
        ]

        # TODO WHY THE FUCK doesn't this work with just passing the cmdArgs??
        # usually it works, but when the command is python3 (meant to run a python file) the python interpreter pops up
        # but passing the command in a normal string works
        output = subprocess.run(
            " ".join(cmdArgs),
            shell=True, stdout=subprocess.PIPE,
            universal_newlines=True)
        self.assertEqual(0, output.returncode)
        self.assertIn("will write denoised file to", output.stdout)
        self.assertIn("OK", output.stdout)
        print("denoised file created :)")

    def assert_denoised_file_metric(self):
        cmdArgs = [
            "python3",
            "src/metric-cci.py",
            "-a",
            DenoisingWithArgumentsTest.cleanFilePath,
            "-b",
            DenoisingWithArgumentsTest.outFilePath,
        ]
        output = subprocess.run(
            " ".join(cmdArgs),
            shell=True, stdout=subprocess.PIPE,
            universal_newlines=True)
        self.assertEqual(0, output.returncode)
        self.assertEqual(
            DenoisingWithArgumentsTest.expectedMetricStdOut, output.stdout)
        print("denoised file has expected metric :)")
