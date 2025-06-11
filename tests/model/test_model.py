
import unittest
import torch

from tnpo.modelo import modelTnpo
import os

class TestModel(unittest.TestCase):
    def setUp(self):
        self.model = modelTnpo(model_name="DoubleItModel",
                            model_type="torchscript",
                            model_path='./model/doubleit-model.pt')
        self.model.load_model()

    def test_model_output(self):
        expected_output = torch.tensor([4, 8, 12])
        output = self.model.infer([2, 4, 6])
        self.assertTrue(torch.equal(output, expected_output))

