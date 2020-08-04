from dataclasses import dataclass

@dataclass
class Config:
    color_off = (0, 0, 0)
    color_on = (255, 255, 255)
    clock_rate = 500

    @property
    def color_scheme(self):
        off = ",".join(str(a) for a in self.color_off)
        on = ",".join(str(a) for a in self.color_on)
        return f"{off}:{on}"

    @color_scheme.setter
    def color_scheme(self, scheme):
        off, on = scheme.split(':')
        self.color_off = tuple(int(a) for a in off.split(','))
        self.color_on = tuple(int(a) for a in on.split(','))

    @property
    def clock_period(self):
        return 1/self.clock_rate

    @clock_period.setter
    def clock_period(self, period):
        self.clock_rate = 1/period
