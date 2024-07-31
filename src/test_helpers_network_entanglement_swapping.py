import unittest

from netsquid.qubits import create_qubits

from src.helper.network.Factory.QuantumProcessor import QuantumProcessorFactory
from src.helper.network.entanglement_swapping import perform_and_get_bell_measurement_w_state, get_results

from src.network.StarNetwork import StarNetwork


class TestHelpersNetworkEntanglementSwapping(unittest.TestCase):
    qubits = [q0, q1, q2, q3] = create_qubits(num_qubits=4, system_name="Q")  # Create two qubits w default state |0>
    # create a star network
    star_network: StarNetwork = StarNetwork({})
    repeater_memory = star_network.network.subcomponents["Repeater"].qmemory
    # place the qubits in the repeater memory
    repeater_memory.put(qubits)

    # m_0_positions = perform_bell_measurement(repeater_memory)
    # m_mem_positions = [2, 3]
    # m_2_positions = perform_bell_measurement(repeater_memory, m_mem_positions)
    # # extract the states in M format
    # state_0_positions = m_0_positions[0]["M"][0]
    # state_2_positions = m_2_positions[0]["M"][0]

    def test_apply_gates(self):
        pass

    def test_perform_and_get_bell_measurement_w_state(self):
        m, state = perform_and_get_bell_measurement_w_state(self.repeater_memory)
        # check that the state M values are between 0 and 3
        self.assertTrue(0 <= state <= 3)
        # extract the key of the M values in the dictionary ('M')
        expected_key = 'M'
        key = list(m[0].keys())[0]
        self.assertEqual(expected_key,
                         key)
        # extract the second position
        expected_second = 0.0
        second = m[1]
        self.assertEqual(expected_second,
                         second)

    def test_get_results(self):
        channel_1_pair = [self.q0, self.q3]
        channel_0_pair = [self.q1, self.q2]
        results = get_results([channel_1_pair, channel_0_pair])
        # check that the results are a list
        self.assertIsInstance(results, list)
        # check that the results have two elements
        self.assertEqual(2, len(results))
        # check that the results are a list of dictionaries
        self.assertIsInstance(results[0], dict)
        self.assertIsInstance(results[1], dict)
        # check that the dictionaries have the keys 'qubits', 'fidelity', and 'error'
        self.assertIn('qubits', results[0].keys())
        self.assertIn('fidelity', results[0].keys())
        self.assertIn('error', results[0].keys())
        self.assertIn('qubits', results[1].keys())
        self.assertIn('fidelity', results[1].keys())
        self.assertIn('error', results[1].keys())
        # check that the 'qubits' key has a list of 2 qubits
        self.assertIsInstance(results[0]['qubits'], list)
        self.assertEqual(2, len(results[0]['qubits']))
        self.assertIsInstance(results[1]['qubits'], list)
        self.assertEqual(2, len(results[1]['qubits']))
        # check that the 'fidelity' key has a float value
        self.assertIsInstance(results[0]['fidelity'], float)
        self.assertIsInstance(results[1]['fidelity'], float)
        # check that the 'fidelity' values are between 0 and 1
        self.assertTrue(0 <= results[0]['fidelity'] <= 1)
        self.assertTrue(0 <= results[1]['fidelity'] <= 1)
        # check that the 'error' key has a boolean value
        self.assertIsInstance(results[0]['error'], bool)
        self.assertIsInstance(results[1]['error'], bool)



if __name__ == "__main__":
    unittest.main()
