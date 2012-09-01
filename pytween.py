# pytween.py - a module for parameter tweening for pyprocessing
# Copyright (c) 2012 Carson J. Q. Farmer
# Released under a modified BSD License (see below)
# Module was ported to Python from Michael Aufreiter's Processing.js script,
# which bears the following copyright notice:
#
# TERMS OF USE - EASING EQUATIONS
# Open source under the BSD License.
# Copyright (c) 2001 Robert Penner
# JavaScript version copyright (c) 2006 by Philippe Maegerman
# Adapted to work along with Processing.js (c) 2009 by Michael Aufreiter
# 
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

#    * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#    * Neither the name of the author nor the names of contributors may
# be used to endorse or promote products derived from this software
# without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE,
# DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import time, math

class Tween:
    def __init__(self, obj, prop, func=None, begin=0, finish=0, duration=None):
        
        # default params
        self.change = 0
        self.prev_time = 0
        self.prev_pos = 0
        self.looping = False
        self._playing = False
        self._time = 0
        self._position = 0
        self._start_time = 0
        self._finish = 0
        self.func = self.linear

        # input params
        self.obj = obj
        self.prop = prop
        self.begin = begin
        self._pos = begin
        
        # bit of a hack added here: not sure why we have to div by 2?
        self.set_duration(duration/2.)
        if not func is None:
            self.func = func
        self.set_finish(finish)
    
    def set_time(self, t):
        self.prev_time = self._time
        if t > self.get_duration():
            if self.looping:
                self.rewind(t - self._duration)
                self.update()
            else:
                self._time = self._duration
                self.update()
                self.stop()
        elif t < 0:
            self.rewind()
            self.update()
        else:
            self._time = t
            self.update()

    def get_time(self):
        return self._time

    def set_duration(self, d):
        self._duration = 1 if d is None or d <= 0 else d

    def get_duration(self):
        return self._duration

    def set_position(self, p):
        self.prev_pos = self._pos
        setattr(self.obj, self.prop, p)
        self._pos = p

    def get_position(self, t):
        if t is None:
            t = self._time
        return self.func(self, t, self.begin, self.change, self._duration)

    def set_finish(self, f):
        self.change = f - self.begin

    def get_finish(self):
        return self.begin + self.change

    def is_playing(self):
        return self._playing
 
    def start(self):
        self.rewind()
        self._playing = True

    def rewind(self, t=None):
        self.stop()
        self._test = 0
        self._time = 0 if t is None else t
        self.fix_time()
        self.update()

    def fast_forward(self):
        self._time = self._duration
        self.fix_time()
        self.update()

    def update(self):
        self.set_position(self.get_position(self._time))

    def tick(self):
        if self._playing:
          self.next_frame()

    def next_frame(self):
        self.set_time(self.get_timer() - self._start_time)

    def stop(self):
        self._playing = False

    def continue_to(self, finish, duration):
        self.begin = self._pos
        self.set_finish(finish)
        if not self._duration is None:
            self.set_duration(duration)
        self.start()

    def resume(self):
        self.fix_time()
        self._playing = True

    def yoyo(self):
        self.continue_to(self.begin, self._time)

    def fix_time(self):
        self._start_time = self.get_timer() - self._time

    def get_timer(self):
        return time.time() - self._time

    # Tweening defs

    def linear(self, t, b, c, d):
        return c*t/d+b

    def backEaseIn(self, t, b, c, d, s=None):
        if s is None:
            s = 1.70158
        t = t/d
        return c*(t)*t*((s+1)*t - s) + b

    def backEaseOut(self, t, b, c, d, s=None):
        if s is None:
            s = 1.70158
        t= t/d-1
        return c*(t*t*((s+1.)*t + s) + 1.) + b

    def backEaseInOut(self, t, b, c, d, s=None):
        if s is None:
            s = 1.70158 
        s *= 1.525
        t /= d/2.
        if t < 1:
            return c/2.*(t*t*((s+1)*t - s)) + b
        t -= 2.
        return c/2.*(t*t*((s+1)*t + s) + 2.) + b

    def elasticEaseIn(self, t, b, c, d, a=None, p=None):
        if t == 0:
            return b
        t /= d
        if t == 1:
            return b+c  
        if p is None:
            p = d*.3
        if a is None or a < math.abs(c):
            a = c
            s = p/4
        else:
            s = p/(2.*math.pi) * math.asin (c/a)
        t -= 1
        return -(a*2.**(10.*t) * math.sin( (t*d-s)*(2.*math.pi)/p )) + b

    def elasticEaseOut(self, t, b, c, d, a=None, p=None):
        if t==0:
            return b
        t/=d
        if t==1:
            return b+c
        if p is None:
            p=d*.3
        if a is None or a < math.abs(c):
            a=c
            s=p/4.
        else:
            s = p/(2.*math.pi) * math.asin(c/a)
        return (a*math.pow(2.,-10.*t) * math.sin((t*d-s)*(2.*math.pi)/p ) + c + b)
        
    def elasticEaseInOut(self, t, b, c, d, a=None, p=None):
        if t==0:
            return b
        t /= d/2.
        if t==2:
            return b+c
        if p is None:
            p=d*(.3*1.5)
        if a is None or a < math.abs(c):
            a = c
            s = p/4.
        else:
            s = p/(2.*math.pi) * math.asin(c/a)
        if (t < 1):
            t -= 1.
            return -.5*(a*(2.**(10.*t)) * math.sin((t*d-s)*(2.*math.pi)/p)) + b
        t -= 1.
        return a*(2.**(-10.*t)) * math.sin((t*d-s)*(2.*math.pi)/p)*.5 + c + b

    def bounceEaseOut(self, t, b, c, d):
        t /= d
        if t < (1./2.75):
            return c*(7.5625*t*t) + b
        elif t < (2./2.75):
            t-=(1.5/2.75)
            return c*(7.5625*t*t + .75) + b
        elif t < (2.5/2.75):
            t-=(2.25/2.75)
            return c*(7.5625*t*t + .9375) + b
        else:
            t-=(2.625/2.75)
            return c*(7.5625*t*t + .984375) + b

    def bounceEaseIn(self, t, b, c, d):
        return c - self.bounceEaseOut(d-t, 0, c, d) + b

    def bounceEaseInOut(self, t, b, c, d):
        if t < d/2:
            return self.bounceEaseIn(t*2., 0, c, d) * .5 + b
        else:
            return self.bounceEaseOut(t*2.-d, 0, c, d) * .5 + c*.5 + b

    def strongEaseInOut(self, t, b, c, d):
        t /= d
        return c*t*t*t*t*t + b

    def regularEaseIn(self, t, b, c, d):
        t /= d
        return c*t*t + b

    def regularEaseOut(self, t, b, c, d):
        t /= d
        return -c*t*(t-2.) + b

    def regularEaseInOut(self, t,b,c,d):
        t /= d/2.
        if t < 1:
            return c/2.*t*t + b
        t -= 1.
        return -c/2. * (t*(t-2.) - 1.) + b
    
    def strongEaseIn(self, t, b, c, d):
        t /= d
        return c*t*t*t*t*t + b

    def strongEaseOut(self, t,b,c,d):
        t = t/d-1.
        return c*(t*t*t*t*t + 1.) + b

    def strongEaseInOut(self, t,b,c,d):
        t/=d/2.
        if t < 1:
            return c/2.*t*t*t*t*t + b
        t -= 2.
        return c/2.*(t*t*t*t*t + 2.) + b

