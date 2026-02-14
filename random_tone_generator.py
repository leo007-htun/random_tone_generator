import random
import numpy as np
import sounddevice as sd


class RandomToneGenerator:
    def __init__(
        self,
        sample_rate=44100,
        base_freq=100.0,
        min_freq=100.0,
        max_freq=8000.0,
        amplitude=0.2,
        speed=1.0,
        base_sweep_min=0.04,
        base_sweep_max=0.25,
        base_hold_min=0.00,
        base_hold_max=0.05,
        min_duration_floor=0.003,
    ):
        self.sample_rate = sample_rate
        self.base_freq = float(base_freq)
        self.min_freq = float(min_freq)
        self.max_freq = float(max_freq)
        self.amplitude = float(amplitude)
        self.speed = float(speed)

        self.base_sweep_min = float(base_sweep_min)
        self.base_sweep_max = float(base_sweep_max)
        self.base_hold_min = float(base_hold_min)
        self.base_hold_max = float(base_hold_max)
        self.min_duration_floor = float(min_duration_floor)

        self._phase = 0.0

    def set_speed(self, speed: float):
        if speed <= 0:
            raise ValueError("speed must be > 0")
        self.speed = float(speed)

    def set_max_freq(self, max_freq: float):
        if max_freq < self.min_freq:
            raise ValueError("max_freq must be >= min_freq")
        self.max_freq = float(max_freq)

    def get_state(self):
        return {
            "base_freq": self.base_freq,
            "min_freq": self.min_freq,
            "max_freq": self.max_freq,
            "amplitude": self.amplitude,
            "speed": self.speed,
        }

    def _scaled_times(self):
        sweep_min = max(self.min_duration_floor, self.base_sweep_min / self.speed)
        sweep_max = max(self.min_duration_floor, self.base_sweep_max / self.speed)
        hold_min = max(0.0, self.base_hold_min / self.speed)
        hold_max = max(0.0, self.base_hold_max / self.speed)
        return sweep_min, sweep_max, hold_min, hold_max

    def _sweep(self, f0, f1, dur):
        n = max(1, int(self.sample_rate * dur))
        freq_curve = np.linspace(f0, f1, n, endpoint=False)
        phase_inc = 2 * np.pi * freq_curve / self.sample_rate
        phase_curve = self._phase + np.cumsum(phase_inc)
        y = self.amplitude * np.sin(phase_curve)

        fade_len = min(256, n // 8)
        if fade_len > 1:
            fade = np.linspace(0, 1, fade_len)
            y[:fade_len] *= fade
            y[-fade_len:] *= fade[::-1]

        self._phase = float(phase_curve[-1] % (2 * np.pi))
        return y.astype(np.float32)

    def _hold(self, f, dur):
        n = max(1, int(self.sample_rate * dur))
        phase_inc = 2 * np.pi * f / self.sample_rate
        phase_curve = self._phase + phase_inc * np.arange(1, n + 1)
        y = self.amplitude * np.sin(phase_curve)
        self._phase = float(phase_curve[-1] % (2 * np.pi))
        return y.astype(np.float32)

    def _write(self, stream, block):
        stream.write(block.reshape(-1, 1))

    def play_for(self, seconds: float):
        """
        Plays only for `seconds`, then returns.
        Pattern:
          1) 100 -> rand -> 100
          2) 100 -> rand -> rand -> 100
        """
        if seconds <= 0:
            return

        sweep_min, sweep_max, hold_min, hold_max = self._scaled_times()

        elapsed = 0.0
        with sd.OutputStream(samplerate=self.sample_rate, channels=1, dtype="float32") as stream:
            while elapsed < seconds:
                # Pattern 1
                a = random.uniform(self.min_freq, self.max_freq)

                d = random.uniform(sweep_min, sweep_max)
                b = self._sweep(self.base_freq, a, d); self._write(stream, b); elapsed += d
                if elapsed >= seconds: break

                h = random.uniform(hold_min, hold_max)
                if h > 0:
                    b = self._hold(a, h); self._write(stream, b); elapsed += h
                    if elapsed >= seconds: break

                d = random.uniform(sweep_min, sweep_max)
                b = self._sweep(a, self.base_freq, d); self._write(stream, b); elapsed += d
                if elapsed >= seconds: break

                h = random.uniform(hold_min, hold_max)
                if h > 0:
                    b = self._hold(self.base_freq, h); self._write(stream, b); elapsed += h
                    if elapsed >= seconds: break

                # Pattern 2
                bfreq = random.uniform(self.min_freq, self.max_freq)
                cfreq = random.uniform(self.min_freq, self.max_freq)

                d = random.uniform(sweep_min, sweep_max)
                b = self._sweep(self.base_freq, bfreq, d); self._write(stream, b); elapsed += d
                if elapsed >= seconds: break

                h = random.uniform(hold_min, hold_max)
                if h > 0:
                    b = self._hold(bfreq, h); self._write(stream, b); elapsed += h
                    if elapsed >= seconds: break

                d = random.uniform(sweep_min, sweep_max)
                b = self._sweep(bfreq, cfreq, d); self._write(stream, b); elapsed += d
                if elapsed >= seconds: break

                h = random.uniform(hold_min, hold_max)
                if h > 0:
                    b = self._hold(cfreq, h); self._write(stream, b); elapsed += h
                    if elapsed >= seconds: break

                d = random.uniform(sweep_min, sweep_max)
                b = self._sweep(cfreq, self.base_freq, d); self._write(stream, b); elapsed += d
