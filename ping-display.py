#!/usr/bin/env python3
from os import system
from threading import Thread
from time import sleep

class PingPoll:
    pbuffer = []
    average = 0.0
    count = 0
    avg_hist = []

    def poll(self, dns: str = '8.8.8.8') -> str:
        p = self.parse(str(system(f'ping 8.8.8.8 -c 1')))
        pstr: str = ''

        if p['error'] is not None:
            r = 'Timed out'
        elif p['ms'] is not None:
            r = f"{p[' ms']}"
            self.avg_hist.append(p['ms'])

        self.pbuffer.append(r)

        for i in self.pbuffer:
            pstr += f'{i}\n'

        pstr += f'Avg MS: {self.average}'

        return pstr
        

    def parse(self, preturn: str) -> dict:
        r = {
            'error': None,
            'ms': None
        }

        try:
            time = preturn.split('time=')[1]
            time = round(float(time.split(' ')), 2)
            r['ms'] = time
        except Exception as e:
            r['error'] = str(e)

        return r

    def get_buffer(self) -> str:
        if len(self.pbuffer) == 5:
            self.pbuffer = self.pbuffer[1:]
        
        poll = self.poll()
        self.pbuffer.append(poll)

        return poll

    def avg(self, a: float) -> None:
        count += 1
        if self.average == 0.0:
            self.average = a
            self.avg_hist.append(a)
        else:
            self.avg_hist.append(a)
            self.average = round((self.average + a) / count, 2) 

    def __init__(self, dns: str = '8.8.8.8'):
        self.dns = '8.8.8.8'

if __name__ == '__main__':
    pp: PingPoll = PingPoll()
    while True:
        print(pp.get_buffer())
        sleep(1)
        system('clear')