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

    def despatch_inventory(self, vel=(0,-4)):
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
