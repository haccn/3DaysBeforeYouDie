import moderngl

from scripts.mgl_utils import *

class time_cycle():
    def __init__(self,app):
        self.app = app
        self.ctx = app.ctx
        self.time = 1

        self.times = [{"state" : "Day"},{"state" : "Night"}]
        self.state = 0

        self.program = load_program(self.ctx,"day")

        self.render_object = render_object(self.ctx,self.program,self.app.quad_buffer)

        self.t = 0


    def update(self):

        if self.times[self.state]["dur"] < self.app.deltatime - self.time:
            self.state += 1
            self.time = self.app.deltatime

        if self.state > len(self.times):
            self.state = 0

    def render(self):
        frame_tex = surf_to_texture(self.ctx,self.app.display)
        frame_tex.use(0)
        self.program['tex'] = 0

        t = (self.app.deltatime - self.time) / self.times[self.state]["dur"]

        if t >= 1:
            t = 1

        self.program["time"] = t

        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
        
        

