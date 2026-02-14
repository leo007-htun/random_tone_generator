import time
from random_tone_generator import RandomToneGenerator

gen = RandomToneGenerator()   # silent init, no default tone

gen.set_speed(0.7)
gen.set_max_freq(500.0)
print("Phase 1:", gen.get_state())
gen.play_for(10)               # plays only 6 sec

gen.set_speed(0.7)
gen.set_max_freq(2000.0)
print("Phase 2:", gen.get_state())
gen.play_for(6)               # plays only 6 sec
6