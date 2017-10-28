# Copyright (c) 2015-2016, The Authors and Contributors
# <see AUTHORS file>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.properties import ReferenceListProperty
from kivy.properties import ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint, random


class OrdersParcel(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class StockParcel(Widget):
    def receive_inventory(self, parcel):
        if self.collide_widget(parcel):
            vx, vy = parcel.velocity
            offset = (parcel.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            parcel.velocity = vel.x, vel.y + offset
            return True


class SimulationFramework(Widget):
    parcel = ObjectProperty(None)
    stock = ObjectProperty(None)

    def despatch_inventory(self, vel=(0, -4)):
        # use variables for size x, y. Increment for growth
        self.parcel.center = (self.width / 2, self.height / 2 - 58)
        print(self.parcel.center)
        self.stock.center = self.center
        self.parcel.velocity = vel
        # self.stock.center, self.stock.size = self.center, (80, 80)

    def set_globe(self, vel=(0, -4)):
        self.parcel.center = (self.width / 2, self.height)
        print(self.parcel.center)
        self.stock.center = self.center
        self.parcel.velocity = vel

    def update(self, dt):
        self.parcel.move()
        # if (self.parcel.y < self.y) or (self.parcel.top > self.top):
        #    self.parcel.velocity_y *= -1
        if self.parcel.y < self.y:
            self.set_globe(vel=(0, -4))
        if self.parcel.y > self.height:
            self.set_globe(vel=(0, -4))

        if self.stock.receive_inventory(self.parcel):
            self.update(self)
            self.despatch_inventory()


class SimulationGuiApp(App):
    def build(self):
        sim = SimulationFramework()
        sim.set_globe()
        Clock.schedule_interval(sim.update, 1.0 / 240.0)
        return sim

    globe = ObjectProperty(None)


if __name__ == '__main__':
    SimulationGuiApp().run()
