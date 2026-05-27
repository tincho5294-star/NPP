import pygame
import time
import sys
import math
pygame.font.init()
pygame.mixer.init()
dial_font=pygame.font.SysFont("arial",12)
style_font=pygame.font.SysFont("lucidaconsole",30)
dial_clicking_sound=pygame.mixer.Sound('dial_clicking_sound.mp3')
dial_drag_cancel_sound=pygame.mixer.Sound('dial_drag_cancel.mp3')
type_1_and_2_button_sound=pygame.mixer.Sound('type_1_and_2_button.mp3')
type_3_and_4_button_sound=pygame.mixer.Sound('type_4_and_3_button.mp3')
dt=1.0/60.0
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
def lerp_color(c1, c2, t):
    return (
        int(lerp(c1[0], c2[0], t)),
        int(lerp(c1[1], c2[1], t)),
        int(lerp(c1[2], c2[2], t))
    )
def clamp(v,a,b):
    return max(a,min(b,v))
def heat_exchange(a_temp,b_temp,flow_rate,dt):
    t=clamp(flow_rate*dt,0,1)
    new_a_temp=lerp(a_temp,b_temp,t)
    new_b_temp=lerp(b_temp,a_temp,t)
    return new_a_temp,new_b_temp
def normalize360(ang):
    return ang%360
def mouse_angle_deg(cx,cy,mx,my):
    dx=mx-cx
    dy=cy-my
    return normalize360(math.degrees(math.atan2(dy,dx)))
def safe_div(a,b):
    try: 
        s=a/b
    except ZeroDivisionError:
        return 0
    else:
        return s
def lerp(a, b, t):
    return a + (b - a) * t
class Marker:
    def __init__(self,x,y,owner=None,toggle=False,_type=None):
        self.x=x
        self.y=y
        self.owner=owner
        self.toggle=toggle
        self._type="on" if _type is None else _type
    def draw(self,screen):
        if self.toggle:
            if self._type=="on":
                color=(193, 255, 193)
            elif self._type=="off":
                color=(255,107,107)
        elif not self.toggle:
            if self._type=="on":
                color=(0,100,0)
            elif self._type=="off":
                color=(139,0,0)
        pygame.draw.rect(screen,(30,30,30),(self.x,self.y,12,12))
        pygame.draw.rect(screen,color,(self.x,self.y,10,10))
class Button:
    def __init__(self,x,y,name,_type,toggle=False,ready=False,radius=40,hitpad=12,lid_open=False): 
        self.x=x
        self.y=y
        self.name=name
        self._type=_type
        self.toggle=bool(toggle)
        self.ready=bool(ready)
        self.radius=radius
        self.hitpad=hitpad
        self.lid_open=bool(lid_open)
        self.lid_x=self.x
        self.lid_y=self.y
        self.lid_half_w=0
        self.lid_half_h=0
        self.lid_surface=None
        self.lid_w=90
        self.lid_h=90
        if self._type == 2:
            self.w = self.radius * 2 + 10
            self.h = self.radius * 2 + 10
            self.lid_size = [self.w, self.h]
            self.lid_half_w = self.w // 2
            self.lid_half_h = self.h // 2
            self.lid_surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            pygame.draw.rect(self.lid_surface, (135, 206, 235, 100), (0, 0, self.w, self.h))
            pygame.draw.rect(self.lid_surface, (200, 200, 200, 150), (0, 0, self.w, self.h), 2)
    def hit_test(self, mx, my):
        if self._type == 1:
            rr = (self.radius + self.hitpad)**2
            if (mx - self.x)**2 + (my - self.y)**2 <= rr:
                type_1_and_2_button_sound.play()
                return True, "button_pressed"

        elif self._type == 2:
            if self.lid_x - self.lid_half_w <= mx <= self.lid_x + self.lid_half_w and self.lid_y - self.lid_half_h <= my <= self.lid_y + self.lid_half_h:
                type_1_and_2_button_sound.play()
                return True, "lid_touched"
            else:
                rr = (self.radius + self.hitpad)**2
                if (mx - self.x)**2 + (my - self.y)**2 <= rr:
                    type_1_and_2_button_sound.play()
                    return True, "button_pressed"
        elif self._type==3:
            w,h=40,20
            if self.x <= mx <= self.x + w and self.y <= my <= self.y + h:
                type_3_and_4_button_sound.play()
                return True,None
        
        elif self._type==4:
            w,h=160,20
            if self.x <= mx <= self.x + w and self.y <= my <= self.y + h:
                type_3_and_4_button_sound.play()
                return True,None
        return False, None
    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            match self.hit_test(e.pos[0], e.pos[1]):
                case (True, "lid_touched"):
                    self.lid_open = not self.lid_open
                case (True, "button_pressed"):

                    if self.ready:
                        self.toggle = not self.toggle
                case (True, None):

                    if self.ready:
                        self.toggle = not self.toggle
    def update(self):
        if self.lid_open:
            self.lid_y=lerp(self.lid_y,self.y-90,dt*2.0)
        else:
            self.lid_y=lerp(self.lid_y,self.y,dt*2.0)
    def draw(self, screen):
        type_4_w, type_4_h = 160, 20
        type_3_w, type_3_h = 40, 20
        

        if self._type == 1:

            pygame.draw.circle(screen, (30, 30, 30), (self.x, self.y), self.radius + 5)
            
            if not self.ready:
                color = (80, 80, 80)
            elif self.toggle:
                color = (193, 255, 193)
            else:
                color = (0, 128, 0)
            pygame.draw.circle(screen, color, (self.x, self.y), self.radius)


        elif self._type == 2:

            pygame.draw.circle(screen, (30, 30, 30), (self.x, self.y), self.radius + 5)
            

            if not self.ready:
                color = (80, 80, 80)
            elif self.toggle:
                color = (255, 100, 100)
            else:
                color = (200, 0, 0)
            pygame.draw.circle(screen, color, (self.x, self.y), self.radius)
            screen.blit(self.lid_surface, (self.lid_x - self.lid_half_w, self.lid_y - self.lid_half_h))


        elif self._type == 3:
            if not self.ready:
                color = (100, 100, 100)
            elif self.toggle:
                color = (255, 255, 255)
            else:
                color = (200, 200, 200)
            pygame.draw.rect(screen, color, (self.x, self.y, type_3_w, type_3_h))

            pygame.draw.rect(screen, (30, 30, 30), (self.x, self.y, type_3_w, type_3_h), 2)


        elif self._type == 4:
            if not self.ready:
                color = (100, 100, 100)
            elif self.toggle:
                color = (255, 100,100)
            else:
                color = (200, 0, 0)
            pygame.draw.rect(screen, color, (self.x, self.y, type_4_w, type_4_h))
            pygame.draw.rect(screen, (30, 30, 30), (self.x, self.y, type_4_w, type_4_h), 2)

class StyleManager:
    def __init__(self):
        self.total_style = 0
        self.style_log = []
        self.style = [
            {"name": "CRITICAL", "score": 200},
            {"name": "SUPERCRITICAL", "score": 400},
            {"name": "CRAM", "score": 25},
            {"name": "MELTDOWN", "score": 4000},
            {"name": "LOCA", "score": 4000},
            {"name": "JUGGLE", "score": 25}
        ]
        self.earned_style = 0
        self.style_rank = ["DULL","CRITICAL","BADASS","ADRENALINE","SURREAL","SSUPERB","SSSUPERCRITICAL","XTREME"]
        self.current_rank=None
        self.style_multiplier = 1
        self.rank_dur = 100
        self.rank_decay_rate = 0.999
        self.visual_t = 0
        self.max_display = 7
    def add_style_log(self, style_entry, timer=5):
        entry = style_entry.copy()
        entry["timer"] = timer
        self.style_log.append(entry)
    def update(self):
        for c in self.style_log:
            if "timer" not in c:
                self.total_style += c["score"]*self.style_multiplier
                c["timer"] = 5
                self.rank_dur+=c["score"]*self.style_multiplier
        if len(self.style_log) > self.max_display:
            self.style_log = self.style_log[-self.max_display:]

        for c in self.style_log[:]:
            c["timer"] -= 1*dt
            if c["timer"] <= 0:
                self.style_log.remove(c)
        self.rank_dur=clamp(self.rank_dur,0,900)
        rank_number=self.rank_dur/100
        if rank_number>=8:
            self.current_rank=self.style_rank[7]
        elif rank_number>=7:
            self.current_rank=self.style_rank[6]
        elif rank_number>=6:
            self.current_rank=self.style_rank[5]
        elif rank_number>=5:
            self.current_rank=self.style_rank[4]
        elif rank_number>=4:
            self.current_rank=self.style_rank[3]
        elif rank_number>=3:
            self.current_rank=self.style_rank[2]
        elif rank_number>=2:
            self.current_rank=self.style_rank[1]
        elif rank_number>=1:
            self.current_rank=self.style_rank[0]
        else:
            self.current_rank=None
        
        self.style_multiplier = clamp(self.style_multiplier * self.rank_decay_rate,1,5)
        self.rank_dur*=self.rank_decay_rate
    def draw(self, screen, x, y):
        target_t = clamp((self.style_multiplier - 1.0) / 4.0, 0, 1)
        self.visual_t = lerp(self.visual_t, target_t, 0.05)
        t = self.visual_t

        base_w, base_h = 125,200
        w = lerp(base_w, base_w * 1.25, t)
        h = lerp(base_h, base_h * 1.25, t)
        
        draw_x = x - (w - base_w) / 2
        draw_y = y - (h - base_h) / 2

        WHITE, YELLOW, RED = (255, 255, 255), (255, 255, 0), (255, 0, 0)
        if t < 0.5:
            m_color = lerp_color(WHITE, YELLOW, t * 2)
        else:
            m_color = lerp_color(YELLOW, RED, (t - 0.5) * 2)

        pygame.draw.rect(screen, (0, 0, 0), (draw_x, draw_y, w, h))
        pygame.draw.rect(screen, m_color, (draw_x, draw_y, w, h), 2)

        log_spacing = 22 * (h / base_h)
        log_base_offset = 58 * (h / base_h)
        for i, c in enumerate(reversed(self.style_log)):
            log_y = draw_y + h - log_base_offset - (i * log_spacing)
            log_timer = c.get("timer", 0)
            log_color = (0, 255, 255) if log_timer > 30 else (100, 100, 100)
            draw_text(f"+ {c['name']}", style_font, log_color, screen, draw_x + 5, log_y)

        draw_text(f"x{self.style_multiplier:.2f}", style_font, m_color, screen, draw_x + 5, draw_y + h - 25)
class Knob:
    def __init__(self,x,y,name,vmin=0,vmax=100,amin_1=40,amax_1=140,amax_2=330,amin_2=210,amid=90,value=0,radius=40,hitpad=12,_type=None,toggle=False): 
        self.x=x
        self.y=y
        self.name=name
        self.vmin=vmin
        self.vmax=vmax
        self.amin_1=amin_1
        self.amax_1=amax_1
        self.amin_2=amin_2
        self.amax_2=amax_2
        self.amid=amid
        self.value=value
        self.radius=radius
        self.hitpad=hitpad
        self.is_dragging=False
        self._type=2 if _type is None else _type
        self.last_switch_angle=math.radians(self.value_to_angle(self.value))
        self.toggle=toggle
        self.sound_step=5
        self.sound_tolerance=0.4
        self.last_sound_tick=None
        self.freshness=1.5
        self.last_released_value=self.value
        
        if self._type == 1:
            self.on_marker = Marker(self.x + 28, self.y - 6, owner=self, _type="on")
            self.off_marker = Marker(self.x - 40, self.y - 6, owner=self, _type="off")
            self.on_marker.toggle = self.toggle
            self.off_marker.toggle = not self.toggle

    def get_angle_limits(self):
        if self._type==1:
            return self.amin_1, self.amax_1
        return self.amin_2, self.amax_2

    def value_to_angle(self,v):
        if self._type==2:
            t=0.0 if self.vmax==self.vmin else (v-self.vmin)/(self.vmax-self.vmin)
            t=clamp(t,0,1)
            return normalize360(lerp(self.amax_2,self.amin_2+360,t))
        amin, amax = self.get_angle_limits()
        t=0.0 if self.vmax==self.vmin else (self.vmax-v)/(self.vmax-self.vmin)
        return lerp(amin,amax,clamp(t,0,1))

    def angle_to_value(self,ang):
        if self._type==2:
            ang=normalize360(ang)
            ang=ang if ang>=self.amax_2 else ang+360
            ang=clamp(ang,self.amax_2,self.amin_2+360)
            t=0.0 if self.amin_2+360==self.amax_2 else (ang-self.amax_2)/(self.amin_2+360-self.amax_2)
            return self.vmin+t*(self.vmax-self.vmin)
        amin, amax = self.get_angle_limits()
        ang=normalize360(ang)
        ang=clamp(ang,amin,amax)
        t=0.0 if amax==amin else (amax-ang)/(amax-amin)
        return self.vmin+t*(self.vmax-self.vmin)

    def drag(self,mx,my):
        drag_ang=normalize360(mouse_angle_deg(self.x,self.y,mx,my)+180)
        if self._type==2:
            if 210 < drag_ang < 330:
                if drag_ang < 270: drag_ang=300
                else: drag_ang=330
        
        new_value=self.angle_to_value(drag_ang)
        if self._type==1:
            if new_value<=self.vmin:
                self.value=self.vmin
                self.toggle=False
            elif new_value>=self.vmax:
                self.value=self.vmax
                self.toggle=True
            

            self.on_marker.toggle = self.toggle
            self.off_marker.toggle = not self.toggle
        else:
            self.value=new_value
        tick=round((self.value-self.vmin)/self.sound_step)
        tick_value=self.vmin+(tick*self.sound_step)
        on_tick=abs(self.value-tick_value)<=self.sound_tolerance

        if on_tick:
            if tick != self.last_sound_tick:
                dial_clicking_sound.play()
                self.last_sound_tick=tick
        elif tick == self.last_sound_tick:
            self.last_sound_tick=None

    def draw(self,screen):
        pygame.draw.rect(screen, (30, 30, 30), (self.x - 45, self.y - 45, 90, 90))
        global dial_font
        name_surf = dial_font.render(self.name, True, (200, 200, 200))
        name_rect = name_surf.get_rect(center=(self.x, self.y + self.radius-10))
        screen.blit(name_surf, name_rect)
        gauge_w,gauge_h=5,80
        gauge_ratio=(self.freshness)/1.5
        f = int(self.freshness * 100)

        if f > 80:
            gauge_color = (255,173,0)
        elif f > 10:
            gauge_color = (255,255,255)
        else:
            gauge_color = (255,0,0)
        pygame.draw.rect(screen,gauge_color,(self.x+55,self.y-45,gauge_w,gauge_h*gauge_ratio))
        if self._type==1:
            if self.value in (self.vmin, self.vmax):
                ang = math.radians(self.value_to_angle(self.value))
                ang_deg=math.degrees(ang)
                self.last_switch_angle=ang
            else:
                ang=self.last_switch_angle
                ang_deg=math.degrees(ang)
            pygame.draw.circle(screen,(175,175,175),(self.x,self.y),10)
            finx=self.x+math.cos(math.radians(self.amax_1))*self.radius
            finy=self.y-math.sin(math.radians(self.amax_1))*self.radius
            sinx=self.x+math.cos(math.radians(self.amin_1))*self.radius
            siny=self.y-math.sin(math.radians(self.amin_1))*self.radius
            vinx=self.x+math.cos(ang)*(self.radius*0.225)
            viny=self.y-math.sin(ang)*(self.radius*0.225)
            left_vinx=self.x+math.cos(ang+0.5*(math.pi))*(self.radius*0.075)
            left_viny=self.y-math.sin(ang+0.5*(math.pi))*(self.radius*0.075)
            right_vinx=self.x+math.cos(ang+1.5*(math.pi))*(self.radius*0.075)
            right_viny=self.y-math.sin(ang+1.5*(math.pi))*(self.radius*0.075)
            
            pygame.draw.line(screen,(200,200,200),(self.x,self.y),(finx,finy),3)
            pygame.draw.line(screen,(200,200,200),(self.x,self.y),(sinx,siny),3)
            
            length = int(self.radius * 1.0)
            w=9
            pointer = pygame.Surface((length * 2, length * 2), pygame.SRCALPHA)
            pygame.draw.rect(pointer,(60,60,60),(length - w // 2, 0,w,length),border_radius=3)
            rot=pygame.transform.rotate(pointer,ang_deg+90)
            rect = rot.get_rect(center=(self.x, self.y))
            screen.blit(rot,rect)
            
            pygame.draw.circle(screen, (60,60,60), (self.x, self.y), 9)
            pygame.draw.polygon(screen,(250,250,250),[(left_vinx,left_viny),(right_vinx,right_viny),(vinx,viny)])
            self.on_marker.draw(screen)
            self.off_marker.draw(screen)

        elif self._type==2:
            for i in range(self.amax_2-180,(self.amin_2+180)+1,60):
                value_t=(i-(self.amax_2-180))/((self.amin_2+360)-(self.amax_2))
                i_value=int(lerp(0,100,value_t))
                value_text=dial_font.render(str(i_value),True,(175,175,175))
                ix=self.x-math.cos(math.radians(normalize360(i)))*25
                iy=self.y+math.sin(math.radians(normalize360(i)))*25
                pygame.draw.line(screen,(175,175,175),(self.x,self.y),(ix,iy))
            pygame.draw.circle(screen,(175,175,175),(self.x,self.y),10)
            ang = math.radians(self.value_to_angle(self.value))
            ang_deg=math.degrees(ang)
            spoke_radius = int(self.radius * 1.08)
            finx=self.x+math.cos(math.radians(self.amax_2))*spoke_radius
            finy=self.y-math.sin(math.radians(self.amax_2))*spoke_radius
            sinx=self.x+math.cos(math.radians(self.amin_2))*spoke_radius
            siny=self.y-math.sin(math.radians(self.amin_2))*spoke_radius
            minx=self.x+math.cos(math.radians(self.amid))*spoke_radius
            miny=self.y-math.sin(math.radians(self.amid))*spoke_radius
            vinx=self.x+math.cos(ang)*(self.radius*0.225)
            viny=self.y-math.sin(ang)*(self.radius*0.225)
            left_vinx=self.x+math.cos(ang+0.5*(math.pi))*(self.radius*0.075)
            left_viny=self.y-math.sin(ang+0.5*(math.pi))*(self.radius*0.075)
            right_vinx=self.x+math.cos(ang+1.5*(math.pi))*(self.radius*0.075)
            right_viny=self.y-math.sin(ang+1.5*(math.pi))*(self.radius*0.075)
            
            pygame.draw.line(screen,(185,185,185),(self.x,self.y),(finx,finy),2)
            pygame.draw.line(screen,(185,185,185),(self.x,self.y),(sinx,siny),2)
            pygame.draw.line(screen,(185,185,185),(self.x,self.y),(minx,miny),2)
            
            length = int(self.radius * 1.0)
            w=9
            pointer = pygame.Surface((length * 2, length * 2), pygame.SRCALPHA)
            pygame.draw.rect(pointer,(60,60,60),(length - w // 2, 0,w,length),border_radius=3)
            rot=pygame.transform.rotate(pointer,ang_deg+90)
            rect = rot.get_rect(center=(self.x, self.y))
            screen.blit(rot,rect)
            
            pygame.draw.circle(screen, (60,60,60), (self.x, self.y), 9)
            pygame.draw.polygon(screen,(250,250,250),[(left_vinx,left_viny),(right_vinx,right_viny),(vinx,viny)])

    def handle_event(self,e):
        if e.type==pygame.MOUSEBUTTONDOWN:
            if e.button==1:
                mx, my = e.pos
                if self.hit_test(mx,my):
                    self.is_dragging=True
        elif e.type==pygame.MOUSEBUTTONUP and e.button==1:
            if self.is_dragging:
                if abs(self.value-self.last_released_value) > 1e-6:
                    sm.style_multiplier*=self.freshness
                    self.freshness-=0.7
                    for knob in knobs:
                        if self.name==knob.name:
                            continue
                        else:
                            knob.freshness+=0.5
                            knob.freshness=clamp(knob.freshness,0,1.5)
                            CR_throttle.freshness+=0.5
                            CR_throttle.freshness=clamp(CR_throttle.freshness,0,1.5)
                    self.last_released_value=self.value
                dial_drag_cancel_sound.play()
            self.is_dragging=False
        elif e.type==pygame.MOUSEMOTION and self.is_dragging:
            self.drag(e.pos[0],e.pos[1])
        self.freshness=clamp(self.freshness,0,1.5)
    def hit_test(self,mx,my):
        rr=(self.radius+self.hitpad)**2
        return (mx-self.x)**2+(my-self.y)**2<=rr
class Throttle:
    def __init__(self, x, y, name, vmin=0, vmax=100, w=40, h=150, value=100):
        self.x, self.y, self.name = x, y, name
        self.vmin, self.vmax = vmin, vmax
        self.w, self.h = w, h
        self.value = value
        self.is_dragging = False
        self.handle_h = 20
        self.sound_step=5
        self.sound_tolerance=0.4
        self.last_sound_tick=None
        self.freshness=1.5
        self.last_released_value=self.value
        self.drag_history=[]
        self.cram_triggered=False
        self.cram_window=0.3
        self.cram_cooldown=2.0
        self.last_cram_time=-self.cram_cooldown
    def y_to_value(self, my):
        top = self.y - (self.h / 2)
        mh = my - top
        t = clamp(safe_div(mh, self.h), 0, 1)
        return lerp(self.vmax, self.vmin, t)

    def get_handle_y(self):
        t = safe_div(self.value - self.vmin, self.vmax - self.vmin)
        t = clamp(t, 0, 1)
        return (self.y + self.h/2 - self.handle_h) - t * (self.h - self.handle_h)

    def hit_test(self, mx, my):
        hy = self.get_handle_y()
        return (self.x - 5 <= mx <= self.x + self.w + 5 and 
                hy <= my <= hy + self.handle_h)

    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.hit_test(e.pos[0], e.pos[1]):
                self.is_dragging = True
                self.drag_history=[(pygame.time.get_ticks() / 1000.0, self.value)]
                self.cram_triggered=False
        elif e.type == pygame.MOUSEBUTTONUP:
            if self.is_dragging:
                release_delta = abs(self.value-self.last_released_value)
                if release_delta > 1e-6:
                    sm.style_multiplier*=self.freshness
                    self.freshness-=0.7
                    self.freshness=clamp(self.freshness,0,1.5)
                    for knob in knobs:
                        knob.freshness+=0.5
                        knob.freshness=clamp(knob.freshness,0,1.5)
                    self.last_released_value=self.value
                dial_drag_cancel_sound.play()
            self.is_dragging = False
            self.drag_history.clear()
            self.cram_triggered=False
            
        if e.type == pygame.MOUSEMOTION and self.is_dragging:
            self.value = self.y_to_value(e.pos[1])
            now = pygame.time.get_ticks() / 1000.0
            self.drag_history.append((now, self.value))
            cutoff = now - self.cram_window
            self.drag_history = [(t, v) for t, v in self.drag_history if t >= cutoff]
            values = [v for _, v in self.drag_history]
            if (
                not self.cram_triggered
                and now - self.last_cram_time >= self.cram_cooldown
                and values
                and (max(values) - min(values) >= 60)
            ):
                sm.add_style_log(sm.style[2])
                self.cram_triggered=True
                self.last_cram_time=now
        tick=round((self.value-self.vmin)/self.sound_step)
        tick_value=self.vmin+(tick*self.sound_step)
        on_tick=abs(self.value-tick_value)<=self.sound_tolerance

        if on_tick:
            if tick != self.last_sound_tick:
                dial_clicking_sound.play()
                self.last_sound_tick=tick
        elif tick == self.last_sound_tick:
            self.last_sound_tick=None
    def draw(self, screen):
        gauge_w,gauge_h=5,220
        gauge_ratio=self.freshness/1.5
        f = int(self.freshness * 100)

        if f > 80:
            gauge_color = (255,173,0)
        elif f > 10:
            gauge_color = (255,255,255)
        else:
            gauge_color = (255,0,0)
        pygame.draw.rect(screen,gauge_color,(self.x+60,self.y-self.h/2-10,gauge_w,gauge_h*gauge_ratio))
        pygame.draw.rect(screen, (45, 45, 45), (self.x - 10, self.y - self.h/2 - 10, self.w + 20, self.h + 20), border_radius=8)


        slot_w = 6  
        slot_color = (10, 10, 10) 
        

        pygame.draw.rect(screen, slot_color, (self.x + 5, self.y - self.h/2 + 5, slot_w, self.h - 10), border_radius=3)

        pygame.draw.rect(screen, slot_color, (self.x + self.w - 5 - slot_w, self.y - self.h/2 + 5, slot_w, self.h - 10), border_radius=3)


        hy = self.get_handle_y()



        pygame.draw.rect(screen, (180, 0, 0), (self.x - 5, hy, self.w + 10, self.handle_h), border_radius=3)
        


        pygame.draw.circle(screen, (30, 30, 30), (self.x + 5 + slot_w/2, hy + self.handle_h/2), 4)
        pygame.draw.circle(screen, (30, 30, 30), (int(self.x + self.w - 5 - slot_w/2), int(hy + self.handle_h/2)), 4)
class Computer:
    def __init__(self,x,y,screen_x,screen_y,name):
        self.x=x
        self.y=y
        self.screen_x=screen_x
        self.screen_y=screen_y
        self.name=name
        self.keyboard_w,self.keyboard_h=150,40
        self.is_typing=False
        self.font=pygame.font.SysFont("consolas",14)
        self.small_font=pygame.font.SysFont("consolas",12)
        self.console=self.Console(self)
    def hit_test(self,mx,my):
        monitor_x=self.x
        monitor_y=self.y-self.screen_y-12
        in_keyboard=self.x <= mx <= self.x + self.keyboard_w and self.y <= my <= self.y + self.keyboard_h
        in_monitor=monitor_x <= mx <= monitor_x + self.screen_x and monitor_y <= my <= monitor_y + self.screen_y
        return in_keyboard or in_monitor
    def handle_event(self,e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.hit_test(e.pos[0], e.pos[1]):
                self.is_typing=True
                self.console.active=True
            else:
                self.is_typing=False
                self.console.active=False
        self.console.handle_event(e)
    def draw(self,screen):
        monitor_x=self.x
        monitor_y=self.y-self.screen_y-12
        screen_color=(255,255,255)
        frame_color=(25,25,25)
        keyboard_color=(85,85,85) if self.console.active else (65,65,65)

        pygame.draw.rect(screen,(screen_color),(monitor_x,monitor_y,self.screen_x,self.screen_y),2)
        pygame.draw.rect(screen,(0,0,0),(monitor_x+4,monitor_y+4,self.screen_x-8,self.screen_y-8))

        pygame.draw.rect(screen,frame_color,(self.x-4,self.y-4,self.keyboard_w+8,self.keyboard_h+8))
        pygame.draw.rect(screen,keyboard_color,(self.x,self.y,self.keyboard_w,self.keyboard_h))

        key_w,key_h=16,12
        start_x=self.x+9
        start_y=self.y+8
        for row in range(2):
            for col in range(7):
                pygame.draw.rect(screen,(45,45,45),(start_x+col*19,start_y+row*15,key_w,key_h))

        title=self.font.render(self.name,True,(255,255,255))
        screen.blit(title,(monitor_x+8,monitor_y+8))
        self.console.draw(screen,monitor_x+8,monitor_y+28,self.screen_x-16,self.screen_y-36)
    class Console:
        def __init__(self,owner):
            self.owner=owner
            self.message=[
                "Current version:",
                "KiwiOS v2.0",
                "Report plant faults here.",
                "Enter to report. exit() to exit."
            ]
            self.input_text=""
            self.active=False
            self.max_reports=4
            self.reports=[]
            self.status="Waiting for maintenance report..."
        def submit_report(self):
            report=self.input_text.strip()
            if not report:
                self.status="Empty report ignored."
                return
            if report.lower()=="exit()":
                self.input_text=""
                self.active=False
                self.owner.is_typing=False
                self.status="Console disconnected."
                return
            timestamp=time.strftime("%H:%M:%S")
            entry=f"[{timestamp}] {report}"
            self.reports.append(entry)
            if len(self.reports)>self.max_reports:
                self.reports=self.reports[-self.max_reports:]
            self.status="Fault report transmitted to maintenance."
            self.input_text=""
        def wrap_lines(self,text,max_width,font):
            words=text.split(" ")
            if not words:
                return [""]
            lines=[]
            current=words[0]
            for word in words[1:]:
                candidate=current+" "+word
                if font.size(candidate)[0] <= max_width:
                    current=candidate
                else:
                    lines.append(current)
                    current=word
            lines.append(current)
            return lines
        def fit_tail(self,text,max_width,font):
            if font.size(text)[0] <= max_width:
                return text
            while text and font.size("..."+text)[0] > max_width:
                text=text[1:]
            return "..."+text if text else ""
        def handle_event(self,e):
            if not self.active:
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.active=False
                    self.owner.is_typing=False
                    self.status="Console disconnected."
                elif e.key == pygame.K_RETURN:
                    self.submit_report()
                elif e.key == pygame.K_BACKSPACE:
                    self.input_text=self.input_text[:-1]
                else:
                    if e.unicode and e.unicode.isprintable():
                        self.input_text+=e.unicode
                        self.input_text=self.input_text[:96]
        def draw(self,screen,x,y,w,h):
            view=pygame.Rect(x,y,w,h)
            old_clip=screen.get_clip()
            screen.set_clip(view)
            line_y=y
            color=(255,255,255)
            for line in self.message:
                for wrapped in self.wrap_lines(line,w,self.owner.small_font):
                    label=self.owner.small_font.render(wrapped,True,color)
                    screen.blit(label,(x,line_y))
                    line_y+=14

            status_top=y+h-52
            log_top=y+h-82
            separator_color=(255,255,255)
            pygame.draw.line(screen,separator_color,(x,log_top-4),(x+w,log_top-4),1)
            pygame.draw.line(screen,separator_color,(x,status_top-4),(x+w,status_top-4),1)

            log_y=log_top
            log_lines=[]
            for report in self.reports[-1:]:
                log_lines.extend(self.wrap_lines(report,w,self.owner.small_font))
            if not log_lines:
                log_lines=["No active reports."]
            for wrapped in log_lines[-2:]:
                label=self.owner.small_font.render(wrapped,True,(255,255,255))
                screen.blit(label,(x,log_y))
                log_y+=14

            status_y=status_top
            status_lines=self.wrap_lines(self.status,w,self.owner.small_font)
            for wrapped in status_lines[:2]:
                label=self.owner.small_font.render(wrapped,True,(255,255,255))
                screen.blit(label,(x,status_y))
                status_y+=14

            prompt=f"> {self.fit_tail(self.input_text,w-18,self.owner.font)}"
            if self.active and (pygame.time.get_ticks()//400)%2==0:
                prompt+="_"
            label=self.owner.font.render(prompt,True,(255,255,255))
            screen.blit(label,(x,y+h-18))
            screen.set_clip(old_clip)
class GridCell:
    def __init__(self,x,y,ix,iy,area,core):
        self.core=core
        self.x=x
        self.y=y
        self.next_temp=20
        self.ix=ix
        self.iy=iy
        self.uranium_mass=3.5
        self.neutron=1
        self.temp=20
        self.xenon=0
        self.search_size=20
        self.void_coeff=0
        self.color=(0,255,0)
        self.neighbors=[]
        self.CR_depth=100
        self.Area=area
        self.search_size=20
        self.next_neutrons=1
        self.neutron_speed=0.2
    def get_color(self):
        R=clamp((255*(self.temp/325)),0,255)
        G=clamp((255*((2000-(self.temp*5))/500)),0,255)
        B=0
        if self.temp>400:
            R = clamp(255 * ((1500 - self.temp) / 1100), 0, 255)
        self.color=(R,G,B)
    def get_neighbor(self):
        if self.Area is None:
            return
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            nx = self.ix + dx
            ny = self.iy + dy
            
            if 0 <= nx < self.search_size and 0 <= ny < self.search_size:
                neighbor=grid[ny][nx]
                if neighbor.Area is not None:
                    self.neighbors.append(neighbor)
    def draw(self,screen):
        if self.Area is None:
            return
        w,h=10,10
        pygame.draw.rect(screen,(30,30,30),(self.x,self.y,w,h))
        pygame.draw.rect(screen,self.color,(self.x,self.y,w-2,h-2))
    def update(self):
        for n in self.neighbors:
            self.next_neutrons,n.next_neutrons=heat_exchange(self.neutron,n.neutron,1,dt)
        if self.Area is None:
            return
        self.neutron_speed=lerp(self.neutron_speed,self.neutron_speed*((1.05-(self.core.water_level*0.1))*(1.85-self.core.water_density)),dt)
        if not math.isfinite(self.neutron_speed):
            self.neutron_speed=0.2
        self.neutron_speed=clamp(self.neutron_speed,0,1.3)
        reaction=(self.neutron*self.uranium_mass*(1.3-self.neutron_speed))*0.2
        if not math.isfinite(reaction):
            reaction=0
        burn_rate=0.991
        k=2-(((self.CR_depth*1.05)/100)+(self.core.boron_conc*0.05)+(self.xenon*0.5))
        self.next_neutrons=lerp(self.next_neutrons,self.neutron*k,dt)
        if not math.isfinite(self.next_neutrons):
            self.next_neutrons=1
        self.next_neutrons=clamp(self.next_neutrons,0,1000000)
        self.next_temp=self.temp+(reaction*dt)
        for n in self.neighbors:
            self.next_temp,n.next_temp=heat_exchange(self.next_temp,n.next_temp,0.005,dt)
        if not math.isfinite(self.next_temp):
            self.next_temp=self.temp
        try:
            self.uranium_mass*=burn_rate**(reaction*dt)
        except OverflowError:
            self.uranium_mass*=1e-33
        if not math.isfinite(self.uranium_mass):
            self.uranium_mass=0
        self.uranium_mass=clamp(self.uranium_mass,0,3.5)
        self.next_temp,self.core.water_temp=heat_exchange(self.next_temp,self.core.water_temp,0.05*((self.core.coolant_flow_rate)*self.core.water_mass),dt)
        if not math.isfinite(self.core.water_temp):
            self.core.water_temp=20
        if not math.isfinite(self.next_temp):
            self.next_temp=self.temp
        self.next_temp=max(20,self.next_temp)
        self.neutron=self.next_neutrons
        self.temp=self.next_temp
class Reactor:
    def __init__(self,name):
        self.name=name
        self.water_temp=20
        self.avg_temp=20
        self.avg_xenon=0
        self.void_coeff=0
        self.boron_conc=0
        self.coolant_flow_rate=0
        self.sprinkler=0
        self.heater=0
        self.fine_heater=0
        self.fine_sprinkler=0
        self.coolant_temp=20
        self.pressure=15
        self.max_pressure=20
        self.boiling_point=300
        self.boiling=False
        self.water_level=1
        self.water_mass=1
        self.water_density=0
        self.circ_water_mass=0
    def update(self):
        self.boiling=self.avg_temp>self.boiling_point
        if self.boiling:
            self.max_pressure=math.inf
            new_pressure = lerp(self.pressure, self.pressure * 7, 0.01*(self.avg_temp/100))
        else:
            self.max_pressure=20
            pressure=lerp(self.pressure,self.max_pressure,((self.heater/100)+((self.fine_heater/100)/2))*0.05*dt)
            new_pressure=lerp(pressure,15,((self.sprinkler/100)+((self.fine_sprinkler/100)/2))*0.05*dt)
        self.pressure=new_pressure
        self.boiling_point=300+self.pressure*3.5
        boron_t=abs((knobs[5].value/100)-(knobs[6].value/100))*(self.coolant_flow_rate/100)*(knobs[8].value/100)*dt*0.05
        max_saturation = (0.00001 * (self.water_temp ** 2) + 0.00033 * self.water_temp + 0.01) * self.water_mass
        max_saturation=clamp(max_saturation,0,1)
        self.heater=knobs[0].value
        self.sprinkler=knobs[2].value
        self.fine_heater=knobs[1].value
        self.fine_sprinkler=knobs[3].value
        self.coolant_flow_rate=knobs[4].value
        self.water_level=(self.water_mass*self.water_temp)/500
        self.water_level=clamp(self.water_level,0,1)
        self.water_density=safe_div(self.water_mass,self.water_level)
        self.water_mass+=(knobs[8].value*0.001)*dt
        self.water_mass-=(knobs[9].value*0.001)*dt
        if not math.isfinite(self.water_mass):
            self.water_mass=1
        self.water_mass=clamp(self.water_mass,0,10)
        self.circ_water_mass+=(knobs[9].value*0.001)*dt
        self.circ_water_mass-=(knobs[8].value*0.001)*dt
        self.circ_water_mass=clamp(self.circ_water_mass,0,1)
        self.water_density=clamp(self.water_density,0,1)
        if self.circ_water_mass>0:
            self.boron_conc = lerp(self.boron_conc,max_saturation if knobs[5].value>=knobs[6].value else 0,(boron_t*(1.3-self.water_density)))
        if not math.isfinite(self.boron_conc):
            self.boron_conc=0
        self.boron_conc=max(0,self.boron_conc)
class Pump:
    def __init__(self):
        self.force=0
        self.toggle=False
    def update(self):
        self.force=lerp(self.force,1 if self.toggle else 0,dt*2 if self.toggle else dt)
class SteamGenerator:
    def __init__(self):
        self.pressure=1
        self.water_mass=1
        self.steam_valve=0
cell_temp_total=0
all_cell_temp=[]
selected_area=[]
AREA_BUTTON_NAMES = {"A", "B", "C", "D", "E", "F", "G", "H"}
current_control_panel=1
reactor=Reactor("default")
grid=[]
grid_size=20
cell_size=10
grid_origin_x=300
grid_origin_y=50
core_center=(grid_size-1)/2
core_radius=8
sector_names=["A","B","C","D","E","F","G","H"]
for iy in range(grid_size):
    row=[]
    for ix in range(grid_size):
        x=grid_origin_x+(ix*cell_size)
        y=grid_origin_y+(iy*cell_size)
        dist_sq=((ix-core_center)**2)+((iy-core_center)**2)
        if dist_sq<=core_radius**2:
            ang=normalize360(math.degrees(math.atan2(core_center-iy,ix-core_center)))
            sector_index=int((ang/360.0)*len(sector_names))%len(sector_names)
            area=sector_names[sector_index]
        else:
            area=None
        cell=GridCell(x,y,ix,iy,area,reactor)
        if area is None:
            cell.uranium_mass=0.0
            cell.neutron=0.0
        row.append(cell)
    grid.append(row)

for row in grid:
    for cell in row:
        cell.get_neighbor()
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Knob Test")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
sm=StyleManager()
knobs=[
    Knob(300,400, "Heater", value=0, radius=40, _type=2),
    Knob(300,500, "Fine Control Heater", value=0, radius=40, _type=2),
    Knob(180,400, "Sprinkler", value=0, radius=40, _type=2),
    Knob(180,500, "Fine Control Sprinkler", value=0, radius=40, _type=2),
    Knob(420, 300, "Coolant Flow Rate", value=0, radius=40, _type=2),
    Knob(420, 400, "Boration", value=0, radius=40, _type=2),
    Knob(420, 500,"Demin. control", value=0, radius=40, _type=2),
    Knob(300, 300, "switch", vmin=0, vmax=100, value=0, radius=40, _type=1),
    Knob(60,400,"Makeup Valve",value=0,radius=40,_type=2),
    Knob(60,500,"Letdown Valve",value=0,radius=40,_type=2)
    ]
CR_throttle = Throttle(550, 370, "Control Rod", vmin=0, vmax=100, w=40, h=200)
buttons = [
    Button(490, 490, "A", 3, toggle=False, ready=True),
    Button(530, 490, "B", 3, toggle=False, ready=True),
    Button(570, 490, "C", 3, toggle=False, ready=True),
    Button(610, 490, "D", 3, toggle=False, ready=True),
    Button(490, 510, "E", 3, toggle=False, ready=True),
    Button(530, 510, "F", 3, toggle=False, ready=True),
    Button(570, 510, "G", 3, toggle=False, ready=True),
    Button(610, 510, "H", 3, toggle=False, ready=True),
    Button(490, 530, "ALL", 4, toggle=False, ready=True),
    Button(700, 530, "test", 2, toggle=False, ready=True)
]
plant_terminal=Computer(635,260,155,210,"Plant Console")
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        plant_terminal.handle_event(e)
        for knob in knobs:
            knob.handle_event(e)
        CR_throttle.handle_event(e)
        for button in buttons:
            button.handle_event(e)
        if e.type == pygame.MOUSEBUTTONDOWN:
            all_button = next((button for button in buttons if button.name == "ALL"), None)
            if all_button and all_button.toggle:
                for button in buttons:
                    if button.name in AREA_BUTTON_NAMES:
                        button.toggle = True
    all_cell_temp.clear()
    for row in grid:
        for cell in row:
            cell.update()

    for button in buttons:
        button.update()

    screen.fill((60, 60, 60))
    for row in grid:
        for cell in row:
            if cell.Area is not None:
                all_cell_temp.append(cell.temp)
            cell_temp_total=sum(all_cell_temp)
            reactor.avg_temp=cell_temp_total/208
    for row in grid:
        for cell in row:
            cell.get_color()
            cell.draw(screen)
    reactor.avg_temp=cell_temp_total/208
    selected_area.clear()
    for button in buttons:
        button.draw(screen)
        label = font.render(button.name, True, (240, 240, 240) if (button._type== 1 or button._type==2) else (30,30,30))
        if button._type in (1, 2):
            label_rect = label.get_rect(center=(button.x, button.y + button.radius + 24))
        else:
            width = 40 if button._type == 3 else 160
            label_rect = label.get_rect(center=(button.x + width // 2, button.y+12))
        if button.toggle and button.name in AREA_BUTTON_NAMES:
            selected_area.append(button.name)
        screen.blit(label, label_rect)
    if selected_area:
        selected_area_set = set(selected_area)
        cr_value = CR_throttle.value
        for row in grid:
            for cell in row:
                if cell.Area in selected_area_set:
                    cell.CR_depth = cr_value
                    
    CR_throttle.draw(screen)
    for knob in knobs:
        knob.draw(screen)
    reactor.update()
    sm.update()
    sm.draw(screen,500,40)
    plant_terminal.draw(screen)
    pygame.display.flip()
    clock.tick(60)
    print(reactor.avg_temp)
pygame.quit()
sys.exit()
