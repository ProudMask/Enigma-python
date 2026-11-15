import subprocess
import sys
import unittest
from enigma import ALPHABET, EnigmaMachine, Rotor, ROTOR_I


class EnigmaTests(unittest.TestCase):
    def test_reference_vector(self):
        self.assertEqual(EnigmaMachine().encode('AAAAA'), 'BDZGO')

    def test_double_step(self):
        machine = EnigmaMachine()
        machine.set_rotor_positions('ADU')
        positions = []
        for _ in range(3):
            machine.encode_char('A')
            positions.append(machine.positions)
        self.assertEqual(positions, ['ADV', 'AEW', 'BFX'])

    def test_rotor_inverse_at_all_positions(self):
        rotor = Rotor(ROTOR_I, 'Q')
        for position in range(26):
            rotor.position = position
            for char in ALPHABET:
                self.assertEqual(rotor.reverse(rotor.forward(char)), char)

    def test_round_trip_and_nonletters(self):
        machine = EnigmaMachine()
        machine.set_rotor_positions('XYZ')
        text = 'Hello, WORLD! 123 مرحبا'
        encoded = machine.encode(text)
        machine.set_rotor_positions('XYZ')
        self.assertEqual(machine.encode(encoded), 'HELLO, WORLD! 123 مرحبا')
        before = machine.positions
        machine.encode(' !123مرحبا')
        self.assertEqual(machine.positions, before)

    def test_invalid_configuration(self):
        for order in ([], [(1, 'Q')] * 3, [(1, 'X'), (2, 'E'), (3, 'V')]):
            with self.assertRaises(ValueError):
                EnigmaMachine(order)
        machine = EnigmaMachine()
        for positions in ('AA', 'aaa', [0, 0, 26], [True, 0, 0]):
            with self.assertRaises(ValueError):
                machine.set_rotor_positions(positions)

    def test_stateful_encoding(self):
        machine = EnigmaMachine()
        combined = machine.encode('AA') + machine.encode('AAA')
        self.assertEqual(combined, EnigmaMachine().encode('AAAAA'))

    def test_cli_and_legacy_import(self):
        result = subprocess.run([sys.executable, 'enigma.py', 'AAAAA'], capture_output=True, text=True, check=True, timeout=10)
        self.assertEqual(result.stdout.strip(), 'BDZGO')
        imported = subprocess.run([sys.executable, '-c', 'import engima, enigma'], capture_output=True, text=True, timeout=10)
        self.assertEqual(imported.returncode, 0)
        self.assertEqual(imported.stdout, '')


if __name__ == '__main__':
    unittest.main()
