# Enigma Python

An educational three-rotor Enigma simulator subset with validated settings and reproducible examples. Supports rotors I/II/III in any distinct order, reflector B, fixed ring settings AAA, and no plugboard. This historical cipher is not suitable for protecting modern secrets.

## Run

Python 3.10 or later; no third-party packages required:

```bash
python enigma.py AAAAA --positions AAA --rotors 1 2 3
# BDZGO
python enigma.py BDZGO --positions AAA --rotors 1 2 3
# AAAAA
python -m unittest discover -s tests -v
```

The original filename `engima.py` remains as a compatibility wrapper. Importing either module does not encode or print an example.

## Python API

```python
from enigma import EnigmaMachine

machine = EnigmaMachine([(1, 'Q'), (2, 'E'), (3, 'V')])
machine.set_rotor_positions('AAA')  # left, middle, right
ciphertext = machine.encode('HELLO WORLD')
machine.set_rotor_positions('AAA')  # reset before decoding
assert machine.encode(ciphertext) == 'HELLO WORLD'
```

Integer positions `[0, 0, 0]` remain supported. Machine state advances across encode calls; reset the starting positions or create an identically configured machine to reverse a message. Lowercase ASCII letters are encoded as uppercase. Spaces, punctuation, digits, and non-ASCII characters are preserved and do not advance rotors. Preserved nonletters are a convenience of this program, not historical keyboard behavior.

## Corrections and model

Rotor traversal applies position offsets on both entry and exit, in each direction. Rotor stepping happens before each letter: the right rotor always steps; the middle steps when it or the right rotor is at its notch; the left steps when the middle is at its notch. Notch states are read before any rotor moves, reproducing the middle rotor's double step.

For order I/II/III starting at ADU, the next window positions are ADV, AEW, and BFX. Defaults AAA encode AAAAA as BDZGO. These are regression examples for the supported subset; round-trip tests alone would not establish historical accuracy.

Input validation checks distinct supported rotors, matching notches, valid wiring permutations, and three positions. The original module had a broken string literal and ran an example at import; those behaviors are corrected.

## Scope and references

No variable ring settings, plugboard, other reflectors/rotors, four-rotor variants, or wartime message procedures are modeled. This is not an exhaustive historical implementation or a modern cryptographic system, and it contains no ML model.

- [Rotor wiring and stepping specifications](https://codesandciphers.org.uk/enigma/rotorspec.htm)
- [David Hamer: the Enigma double-stepping mechanism](https://www.cryptomuseum.com/people/hamer/files/double_stepping.pdf)
