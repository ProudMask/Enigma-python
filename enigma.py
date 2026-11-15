"""Educational three-rotor Enigma subset: rings AAA, reflector B, no plugboard."""
import argparse
import string

ALPHABET = string.ascii_uppercase
ROTOR_I = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
ROTOR_II = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'
ROTOR_III = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'
REFLECTOR_B = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
SPECS = {1: (ROTOR_I, 'Q'), 2: (ROTOR_II, 'E'), 3: (ROTOR_III, 'V')}


class Rotor:
    def __init__(self, wiring, notch):
        if not isinstance(wiring, str) or len(wiring) != 26 or set(wiring) != set(ALPHABET):
            raise ValueError('Rotor wiring must be a permutation of A-Z')
        if not isinstance(notch, str) or len(notch) != 1 or notch not in ALPHABET:
            raise ValueError('Notch must be one uppercase A-Z letter')
        self.wiring = wiring
        self.notch = notch
        self.position = 0

    def forward(self, char):
        shifted = (ALPHABET.index(char) + self.position) % 26
        return ALPHABET[(ALPHABET.index(self.wiring[shifted]) - self.position) % 26]

    def reverse(self, char):
        shifted = ALPHABET[(ALPHABET.index(char) + self.position) % 26]
        return ALPHABET[(self.wiring.index(shifted) - self.position) % 26]

    def rotate(self):
        self.position = (self.position + 1) % 26

    def at_notch(self):
        return ALPHABET[self.position] == self.notch


class EnigmaMachine:
    def __init__(self, rotor_order=None):
        rotor_order = [(1, 'Q'), (2, 'E'), (3, 'V')] if rotor_order is None else list(rotor_order)
        if len(rotor_order) != 3:
            raise ValueError('Exactly three distinct rotors are required, left to right')
        ids = []
        self.rotors = []
        for item in rotor_order:
            if not isinstance(item, (tuple, list)) or len(item) != 2:
                raise ValueError('Each rotor setting must be a (rotor number, notch) pair')
            number, notch = item
            if isinstance(number, bool) or not isinstance(number, int) or number not in SPECS or number in ids:
                raise ValueError('Use each of rotors 1, 2, and 3 exactly once')
            if notch != SPECS[number][1]:
                raise ValueError('Notch must match the selected historical rotor')
            ids.append(number)
            self.rotors.append(Rotor(*SPECS[number]))
        self.reflector = REFLECTOR_B

    @property
    def positions(self):
        return ''.join(ALPHABET[rotor.position] for rotor in self.rotors)

    def set_rotor_positions(self, positions):
        if isinstance(positions, str):
            if len(positions) != 3 or any(char not in ALPHABET for char in positions):
                raise ValueError('Positions must be three uppercase letters, e.g. AAA')
            values = [ALPHABET.index(char) for char in positions]
        else:
            try:
                values = list(positions)
            except TypeError as exc:
                raise ValueError('Positions must be three integers or uppercase letters') from exc
            if len(values) != 3 or any(isinstance(value, bool) or not isinstance(value, int) or not 0 <= value < 26 for value in values):
                raise ValueError('Positions must be three integers from 0 to 25')
        for rotor, value in zip(self.rotors, values):
            rotor.position = value

    def step(self):
        left, middle, right = self.rotors
        middle_notch, right_notch = middle.at_notch(), right.at_notch()
        if middle_notch:
            left.rotate()
        if middle_notch or right_notch:
            middle.rotate()
        right.rotate()

    def encode_char(self, char):
        if not isinstance(char, str) or len(char) != 1 or char not in ALPHABET:
            raise ValueError('encode_char requires one uppercase A-Z letter')
        self.step()
        for rotor in reversed(self.rotors):
            char = rotor.forward(char)
        char = self.reflector[ALPHABET.index(char)]
        for rotor in self.rotors:
            char = rotor.reverse(char)
        return char

    def encode(self, message):
        if not isinstance(message, str):
            raise ValueError('Message must be text')
        return ''.join(self.encode_char(char.upper()) if char in string.ascii_letters else char for char in message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('message')
    parser.add_argument('--positions', default='AAA')
    parser.add_argument('--rotors', type=int, nargs=3, default=[1, 2, 3], metavar=('LEFT', 'MIDDLE', 'RIGHT'))
    args = parser.parse_args()
    try:
        if any(number not in SPECS for number in args.rotors):
            raise ValueError('Supported rotor numbers are 1, 2, and 3')
        machine = EnigmaMachine([(number, SPECS[number][1]) for number in args.rotors])
        machine.set_rotor_positions(args.positions)
        print(machine.encode(args.message))
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
