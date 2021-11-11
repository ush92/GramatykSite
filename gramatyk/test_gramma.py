import unittest
from gramatyk.gramma import Gramma


class TestBasic(unittest.TestCase):

    def test_get_instructions_should_return_proper_text(self):
        expected_text = "// Przykładowa gramatyka:\nS->AB|AC.\nB->BB|zx.\nA->xC|y.\nC->zB|CC.\nQ->Qt|BB|CAB."

        result_text = Gramma.get_instructions()

        self.assertEqual(expected_text, result_text)

    def test_prepare_data_should_trim_text_generate_array(self):
        input_text = " // Przykładowa gramatyka:\nS->AB|AC.\nB->BB|zx.\nA->xC|y.\nC->zB|CC.\nQ->Qt|BB|CAB. "
        sut = Gramma()
        expected_result = ["// Przykładowa gramatyka:",
                           "S->AB|AC.",
                           "B->BB|zx.",
                           "A->dC|y.",
                           "C->zB|CC.",
                           "Q->Qt|BB|CAB."
                           ]

        sut.prepare_data(input_text)

        self.assertEqual(sut.data, expected_result)
