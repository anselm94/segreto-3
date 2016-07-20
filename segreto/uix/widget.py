from kivy.uix.anchorlayout import AnchorLayout
from kivy.animation import Animation
from kivy.clock import Clock
import kivy.metrics as metrics
from kivy.properties import StringProperty, ObjectProperty

class Toast(AnchorLayout):
    text = StringProperty("Oops! Error")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show(self, desc):
        self.text = desc
        anim = Animation(y = metrics.dp(50), t = 'in_out_expo')
        anim.start(self)
        Clock.schedule_once(self.exit, 5)

    def exit(self, dt):
        Clock.unschedule(self.exit)
        anim = Animation(y = metrics.dp(-50), t = 'in_out_expo')
        anim.start(self)

    def on_text(self, instance, value):
        self.ids.label.text = value
