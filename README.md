# random_tone_generator

A small Python utility to generate randomized tone sweeps and holds in real time.

## Features

- Real-time audio output via `sounddevice`
- Random sweep patterns:
  - `base -> random -> base`
  - `base -> random -> random -> base`
- Adjustable:
  - playback speed
  - min/max frequency
  - amplitude
- Explicit playback duration with `play_for(seconds)`

## function calls
<<<<<<< HEAD
    gen.set_speed(speed)         # float, must be > 0
    
    gen.set_max_freq(max_freq)   # float, must be >= min_freq
    
    gen.set_min_freq(min_freq)   # float, must be <= max_freq   
    
    gen.set_base_freq(base_freq) # float                       
    
    gen.set_amplitude(amplitude) # float in [0.0, 1.0]       
    
    state = gen.get_state()      # returns dict of current settings
    
    gen.play_for(seconds)        # play for N seconds (explicit mode)
=======

                    gen.set_speed(speed)         # float, must be > 0

                    gen.set_max_freq(max_freq)   # float, must be >= min_freq

                    gen.set_min_freq(min_freq)   # float, must be <= max_freq  
        
                    gen.set_base_freq(base_freq) # float                       

                    gen.set_amplitude(amplitude) # float in [0.0, 1.0]        

                    state = gen.get_state()      # returns dict of current settings

                    gen.play_for(seconds)        # play for N seconds 
>>>>>>> 8d9c653 (WIP: save local changes)

---

## Installation

```bash
pip install random_tone_generator



