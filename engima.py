import string
import random

# Define the Enigma machine settings
ROTOR_I = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
ROTOR_II = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
ROTOR_III = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

class Rotor:
    def __init__(self, wiring, notch):
        self.wiring = wiring
        self.notch = notch
        self.position = 0
    
    def forward(self, char):
        pos = (string.ascii_uppercase.index(char) + self.position) % 26
        return self.wiring[pos]
    
    def reverse(self, char):
        pos = (self.wiring.index(char) - self.position) % 26
        return string.ascii_uppercase[pos]
    
    def rotate(self):
        self.position = (self.position + 1) % 26
    
    def at_notch(self):
        return string.ascii_uppercase[self.position] == self.notch

class EnigmaMachine:
    def __init__(self, rotor_order):
        self.rotors = []
        for rotor_type, notch in rotor_order:
            if rotor_type == 1:
                wiring = ROTOR_I
            elif rotor_type == 2:
                wiring = ROTOR_II
            elif rotor_type == 3:
                wiring = ROTOR_III
            else:
                raise ValueError("Invalid rotor type: 
{}".format(rotor_type))
            self.rotors.append(Rotor(wiring, notch))
        self.reflector = REFLECTOR_B
    
    def set_rotor_positions(self, positions):
        for i, pos in enumerate(positions):
            self.rotors[i].position = pos
    
    def encode_char(self, char):
        # Rotate rotors before encoding
        self.rotors[-1].rotate()
        for i in range(len(self.rotors) - 1, 0, -1):
            if self.rotors[i-1].at_notch():
                self.rotors[i-1].rotate()
        # Pass char through rotors
        for rotor in self.rotors[::-1]:
            char = rotor.forward(char)
        # Pass char through reflector
        char = self.reflector[string.ascii_uppercase.index(char)]
        # Pass char back through rotors in reverse order
        for rotor in self.rotors:
            char = rotor.reverse(char)
        return char
    
    def encode(self, message):
        encoded = ""
        for char in message:
            if char in string.ascii_uppercase:
                encoded += self.encode_char(char)
            else:
                encoded += char
        return encoded

# Example usage:
machine = EnigmaMachine([(1, 'Q'), (2, 'E'), (3, 'V')])
machine.set_rotor_positions([0, 0, 0])
message = "HELLO WORLD"
encoded = machine.encode(message)
print("Encoded message:", encoded)
