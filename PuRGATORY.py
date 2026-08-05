#lil goofy school project ahh looking project
#"Excuse me SON"
#"lets LARP. https://media.tenor.com/WO2nrHqW6n8AAAAe/ryu-ishigori-jjk.png"
#https://x.com/jotaein133124
#이 코드를 리뷰하려는자, 희망을 버려라.
#조태인의 쌈@뽕 삐리깡뽕 한 개발 플리 
#1. ULTRACHURCH https://www.youtube.com/watch?v=KTCC053fLqs&list=RDAchqe_GDUTM&index=2
#2. Tenebre Rosso Sangue https://www.youtube.com/watch?v=L5q4uYj-gyg&list=RDL5q4uYj-gyg&start_radio=1
#3. The Cybergrind https://www.youtube.com/watch?v=e9EqU9y69vU&list=RDe9EqU9y69vU&start_radio=1
#4. WAR https://www.youtube.com/watch?v=kDqTB3fV3sw&list=RDkDqTB3fV3sw&start_radio=1
#5. No Devil Lived On https://www.youtube.com/watch?v=_ysPpT7-f4o&list=RD_ysPpT7-f4o&start_radio=1
#6. War Without Reason https://www.youtube.com/watch?v=Elj4zDLqJvw&list=RDElj4zDLqJvw&start_radio=1
#7. Danse Macabre https://www.youtube.com/watch?v=AjGb1w88Lr0&list=RDAjGb1w88Lr0&start_radio=1
#8. Event Horizon https://www.youtube.com/watch?v=_ysPpT7-f4o&list=RD_ysPpT7-f4o&start_radio=1
#9. Closing Time https://www.youtube.com/watch?v=ikSUjsRBVtQ&list=RDikSUjsRBVtQ&start_radio=1
import pygame
import time
import sys
import math
import random
from collections import deque
pygame.font.init()
pygame.mixer.init()
dial_font=pygame.font.SysFont("arial",12)
sector_font=pygame.font.SysFont("arial",20)
meter_font=pygame.font.SysFont("arial",10)
style_font=pygame.font.SysFont("lucidaconsole",30)
dial_clicking_sound=pygame.mixer.Sound('dial_clicking_sound.mp3')
dial_drag_cancel_sound=pygame.mixer.Sound('dial_drag_cancel.mp3')
type_1_and_2_button_sound=pygame.mixer.Sound('type_1_and_2_button.mp3')
type_3_and_4_button_sound=pygame.mixer.Sound('type_4_and_3_button.mp3')
CVCS_text=sector_font.render("CVCS",True,(255,255,255))
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
class LightSource:
    def __init__(self,x,y,DistanceFromGround,brightness,range):
        self.x=x
        self.y=y
        self.DistanceFromGround=DistanceFromGround
        self.brightness=brightness
        self.range=range
        self.layer=[{"Surface":None,"radius":self.range},
                    {"Surface":None,"radius":self.range*0.9},
                    {"Surface":None,"radius":(self.range*0.9)*0.9},
                    {"Surface":None,"radius":((self.range*0.9)*0.9)},
                    {"Surface":None,"radius":(((self.range*0.9)*0.9))*0.9}, #pure masterpiece i swear
                    {"Surface":None,"radius":((((self.range*0.9)*0.9))*0.9)*0.9},
                    {"Surface":None,"radius":(((((self.range*0.9)*0.9))*0.9)*0.9)*0.9},
                    {"Surface":None,"radius":((((((self.range*0.9)*0.9))*0.9)*0.9)*0.9)*0.9}, 
                    {"Surface":None,"radius":(((((((self.range*0.9)*0.9))*0.9)*0.9)*0.9)*0.9)*0.9}]
        self.lightsurface=pygame.Surface((self.range*2,self.range*2),pygame.SRCALPHA)
    def LightUp(self):
        for l in self.layer:
            l_R=clamp((255*(1-(l["radius"]/self.range))*self.brightness)*2,0,255)
            l_G=clamp((255*(1-(l["radius"]/self.range))*self.brightness)*2,0,255)
            l_B=clamp((255*(1-(l["radius"]/self.range))*self.brightness)*2,0,255)
            l_A=20
            pygame.draw.circle(self.lightsurface,(l_R,l_G,l_B,l_A),(self.range,self.range),l["radius"])
            screen.blit(self.lightsurface, (self.x-self.range,self.y-self.range))
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
            {"name": "CRAM", "score": 900},
            {"name": "MELTDOWN", "score": 4000},
            {"name": "LOCA", "score": 4000},
            {"name": "JUGGLE", "score": 900},
            {"name": "ONSET","score": 200},
            {"name": "RECKLESS","score":5}
        ]
        self.earned_style = 0
        self.style_rank = ["DULL","CHERENKOV","BADASS","ADRENALINE","SURREAL","SSUPERB","SSSUPERCRITICAL","PURGATORY"]
        self.current_rank=None
        self.style_multiplier = 1
        self.rank_dur = 100
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
        rank_number=self.rank_dur//100
        self.current_rank=self.style_rank[int(rank_number-1)]
        self.style_multiplier = clamp(self.style_multiplier - 0.1*dt,1,5)
        self.rank_dur=clamp(self.rank_dur-(10*dt),0,900)
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
    def __init__(self,x,y,name,panel_number,light,distancefromground,vmin=0,vmax=100,amin_1=40,amax_1=140,amax_2=330,amin_2=210,amid=90,value=0,radius=40,hitpad=12,_type=None,toggle=False): 
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
        self.light=light
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
        self.DistanceFromGround=distancefromground
        self.last_released_value=self.value
        self.last_released_time=pygame.time.get_ticks()
        self.panel_number=panel_number
        self.shadow_surface=pygame.Surface((800,600),pygame.SRCALPHA)
        self.shadow_alpha=150
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
        if self.panel_number==current_control_panel:
            dx=self.light.x-(self.x - 45)
            dy=(self.y-45)-self.light.y
            dir_ground=self.DistanceFromGround-self.light.DistanceFromGround
            dist_ground=abs(self.DistanceFromGround-self.light.DistanceFromGround)
            shadow_rect_coordinates=((self.x - 45)+math.cos(math.atan2(dy,dx))*safe_div(dist_ground/25,math.atan2(dir_ground,math.hypot(dx,dy))),(self.y - 45)-math.sin(math.atan2(dy,dx))*safe_div(dist_ground/25,math.atan2(dir_ground,math.hypot(dx,dy))))
            pygame.draw.rect(self.shadow_surface,(0,0,0,self.shadow_alpha),(shadow_rect_coordinates[0],shadow_rect_coordinates[1],90,90))
            screen.blit(self.shadow_surface,(0,0))
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
                first_point=(self.x+math.cos((ang+math.pi)+0.5*math.pi)*(self.radius*0.1),self.y-math.sin((ang+math.pi)+0.5*math.pi)*(self.radius*0.1))
                second_point=(self.x+math.cos((ang+math.pi)+1.5*math.pi)*(self.radius*0.1),self.y-math.sin((ang+math.pi)+1.5*math.pi)*(self.radius*0.1))
                third_point=(self.x+math.cos((ang+math.pi)-math.pi/27)*self.radius,self.y-math.sin((ang+math.pi)-math.pi/27)*self.radius)
                fourth_point=(self.x+math.cos((ang+math.pi)+math.pi/27)*self.radius,self.y-math.sin((ang+math.pi)+math.pi/27)*self.radius)
                pygame.draw.polygon(screen,(60,60,60),[first_point,second_point,third_point,fourth_point])
                pygame.draw.circle(screen, (60,60,60), (self.x, self.y), 9)
                pygame.draw.polygon(screen,(250,250,250),[(left_vinx,left_viny),(right_vinx,right_viny),(vinx,viny)])
                self.on_marker.draw(screen)
                self.off_marker.draw(screen)

            elif self._type==2:
                for i in range(self.amax_2-180,(self.amin_2+180)+1,60):
                    value_t=(i-(self.amax_2-180))/((self.amin_2+360)-(self.amax_2))
                    i_value=int(lerp(0,100,value_t))
                    value_text=dial_font.render(str(round(i_value,0)),True,(175,175,175))
                    ix=self.x-math.cos(math.radians(normalize360(i)))*28
                    iy=self.y+math.sin(math.radians(normalize360(i)))*28
                    if i_value<50:
                        screen.blit(value_text,(ix+10,iy-14))
                    elif i_value==50:
                        screen.blit(value_text,(ix+5,iy-14))
                    elif i_value==100:
                        screen.blit(value_text,(ix-20,iy-14))
                    else:
                        screen.blit(value_text,(ix-10,iy-14))
                    pygame.draw.line(screen,(175,175,175),(self.x,self.y),(ix,iy))
                for si in range(self.amax_2-180,(self.amin_2+180)+1,15):
                    six=self.x-math.cos(math.radians(normalize360(si)))*15
                    siy=self.y+math.sin(math.radians(normalize360(si)))*15
                    pygame.draw.line(screen,(175,175,175),(self.x,self.y),(six,siy))
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
                w=9
                first_point=(self.x+math.cos((ang+math.pi)+0.5*math.pi)*(self.radius*0.1),self.y-math.sin((ang+math.pi)+0.5*math.pi)*(self.radius*0.1))
                second_point=(self.x+math.cos((ang+math.pi)+1.5*math.pi)*(self.radius*0.1),self.y-math.sin((ang+math.pi)+1.5*math.pi)*(self.radius*0.1))
                third_point=(self.x+math.cos((ang+math.pi)-math.pi/27)*self.radius,self.y-math.sin((ang+math.pi)-math.pi/27)*self.radius)
                fourth_point=(self.x+math.cos((ang+math.pi)+math.pi/27)*self.radius,self.y-math.sin((ang+math.pi)+math.pi/27)*self.radius)
                shadow_points=[
                    {"x":None,"y":None,"point":first_point},
                    {"x":None,"y":None,"point":second_point},
                    {"x":None,"y":None,"point":third_point},
                    {"x":None,"y":None,"point":fourth_point}
                ]
                for s in shadow_points:
                    owner_point=s["point"]
                    dx=self.light.x-owner_point[0]
                    dy=owner_point[1]-self.light.y
                    dir_ground=self.DistanceFromGround-self.light.DistanceFromGround
                    dist_ground=abs(self.DistanceFromGround-self.light.DistanceFromGround)
                    s["x"]=owner_point[0]+math.cos(math.atan2(dy,dx))*safe_div(self.DistanceFromGround/25,math.atan2(dir_ground,math.hypot(dx,dy)))
                    s["y"]=owner_point[1]-math.sin(math.atan2(dy,dx))*safe_div(self.DistanceFromGround/25,math.atan2(dir_ground,math.hypot(dx,dy)))
                shadow_circle_x=self.x+math.cos(math.atan2(dy,dx))*safe_div(self.DistanceFromGround/25,math.atan2(dir_ground,math.hypot(dx,dy)))
                shadow_circle_y=self.y-math.sin(math.atan2(dy,dx))*safe_div(self.DistanceFromGround/25,math.atan2(dir_ground,math.hypot(dx,dy)))
                shadow_first=shadow_points[0]
                shadow_second=shadow_points[1]
                shadow_third=shadow_points[2]
                shadow_fourth=shadow_points[3]
                self.shadow_surface.fill((0,0,0,0))
                pygame.draw.circle(self.shadow_surface,(0,0,0,self.shadow_alpha),(shadow_circle_x,shadow_circle_y),9)
                pygame.draw.polygon(self.shadow_surface,(0,0,0,self.shadow_alpha),[(shadow_first["x"],shadow_first["y"]),(shadow_second["x"],shadow_second["y"]),(shadow_third["x"],shadow_third["y"]),(shadow_fourth["x"],shadow_fourth["y"])])
                screen.blit(self.shadow_surface,(0,0))
                pygame.draw.polygon(screen,(60,60,60),[first_point,second_point,third_point,fourth_point])
                pygame.draw.circle(screen, (60,60,60), (self.x, self.y), 9)
                pygame.draw.polygon(screen,(250,250,250),[(left_vinx,left_viny),(right_vinx,right_viny),(vinx,viny)])

    def handle_event(self,e):
        if self.panel_number!=current_control_panel:
            self.is_dragging=False
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
                self.last_released_time=pygame.time.get_ticks()
                juggle_history.append({"time":self.last_released_time})
                dial_drag_cancel_sound.play()
        if e.type==pygame.MOUSEBUTTONUP and e.button==1:
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
                    self.last_released_time=pygame.time.get_ticks()
                    juggle_history.append({"time":self.last_released_time})
                dial_drag_cancel_sound.play()
            self.is_dragging=False
        if e.type==pygame.MOUSEBUTTONDOWN:
            if e.button==1:
                mx, my = e.pos
                if self.hit_test(mx,my):
                    self.is_dragging=True
        elif e.type==pygame.MOUSEMOTION and self.is_dragging:
            self.drag(e.pos[0],e.pos[1])
        self.freshness=clamp(self.freshness,0,1.5)
    def hit_test(self,mx,my):
        rr=(self.radius+self.hitpad)**2
        return (mx-self.x)**2+(my-self.y)**2<=rr
class PlayerManager:
    def __init__(self):
        self.hard=0
        self.health=100
        self.next_health=100
        self.max_health=100
        self.min_health=0
        self.payout=0
        self.wealth=120
        self.fired=False
    def update(self,style,max_style,min_style):
        self.hard=self.max_health-self.health
        target_health=self.max_health*((style-min_style)/(max_style-min_style))
        self.next_health=lerp(self.health,target_health,dt)
        self.health=lerp(self.health,self.next_health,0.01/(1+(self.hard/100)) if (self.next_health>self.health) else dt)
    def draw(self,screen,x,y):
        w=20
        h=100
        ratio=(self.health-self.min_health)/(self.max_health-self.min_health)
        HP_y=(y+h)-(h*ratio)
        pygame.draw.rect(screen,(30,30,30),(x,y,w,h*(1-ratio)))
        pygame.draw.rect(screen,(100,100,100),(x,y,w,h*ratio))
        pygame.draw.rect(screen,(255,0,0),(x,HP_y,w,h*ratio))
        
class Meter:
    def __init__(self,x,y,w,h,value,min_value,max_value,timeline_length):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.value=value
        self.timeline_length=timeline_length
        self.min_value=min_value
        self.max_value=max_value
        self.latest_time=0
        self.value_surface=meter_font.render(str(round(self.value,1)),False,(255,140,0))
        self.points=deque()
    def value_to_y(self,value):
        value_ratio=clamp((value-self.min_value)/(self.max_value-self.min_value),0,1)
        return lerp((self.y+self.h),self.y,value_ratio)
    def time_to_x(self,time):
        time_ratio=min((time-max((self.latest_time-self.timeline_length),0))/(self.timeline_length),1)
        return lerp(self.x,(self.x+self.w),time_ratio)
    def update(self):
        self.latest_time+=dt
        if self.value>=self.max_value:
            self.max_value=self.value
        self.points.append({"time":self.latest_time,"value":self.value})
        while self.points and self.points[0]["time"] < self.latest_time-self.timeline_length:
            self.points.popleft()
        self.value_surface=meter_font.render(str(round(self.value,1)),True,(255,140,0))
    def draw(self,screen):
        pygame.draw.rect(screen,(30,30,30),(self.x-5,self.y-5,self.w+30,self.h+10))
        pygame.draw.rect(screen,(15,15,15),(self.x,self.y,self.w+20,self.h))
        for i in range(self.x,(self.x+self.w)+1,int(self.w/5)):
            pygame.draw.line(screen,(25,25,25),(i,self.y),(i,(self.y+self.h)))
        for k in range(self.y,(self.y+self.h)+1,int(self.h/5)):
            pygame.draw.line(screen,(25,25,25),(self.x,k),((self.x+self.w),k))
        for p in self.points:
            py=self.value_to_y(p["value"])
            px=self.time_to_x(p["time"])
            if self.latest_time-self.timeline_length<=p["time"]:
                pygame.draw.circle(screen,(255, 140, 0),(px,py),1)
        screen.blit(self.value_surface,(self.x+self.w,self.value_to_y(self.value)))
        pygame.draw.line(screen,(255,100,0),(self.time_to_x(self.latest_time),self.value_to_y(self.value)),(self.x+self.w,self.value_to_y(self.value)))
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
        self.w_cell=GridCell.WaterCell(self.x,self.y,self,ix,iy,core,area)
    def get_color(self):
        R=clamp((255*(self.temp/325)),0,255)
        G=clamp(safe_div((255*((2000-(self.temp*5))/500)),(self.w_cell.pressure/20)),0,255)
        B=clamp(255*(self.w_cell.pressure/20),0,255)
        if self.temp>400:
            R = clamp(255 * ((1500 - self.temp) / 1100), 0, 255)
        self.color=(R,G,B)
    def get_neighbor(self):
        if self.Area is None:
            return
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        
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
        w,h=15,15
        pygame.draw.rect(screen,(30,30,30),(self.x,self.y,w,h))
        pygame.draw.rect(screen,self.color,(self.x,self.y,w-2,h-2))
    def update(self):
        if self.Area is None:
            return
        for n in self.neighbors:
            self.next_neutrons,n.next_neutrons=heat_exchange(self.next_neutrons,n.next_neutrons,1,dt)
        self.neutron_speed=lerp(self.neutron_speed,self.neutron_speed*((1.05-((self.core.water_level/7000)*0.1))*(1.85-self.core.water_density)),dt)
        if not math.isfinite(self.neutron_speed):
            self.neutron_speed=0.2
        self.neutron_speed=clamp(self.neutron_speed,0,1.3)
        reaction=(self.neutron*self.uranium_mass*(1/self.neutron_speed))
        if not math.isfinite(reaction):
            reaction=0
        burn_rate=0.991
        k=2-(((self.CR_depth*1.05)/100)+(self.core.boron_conc*0.5))
        xenon_poison=1+(self.xenon*0.4)
        self.next_neutrons=lerp(self.next_neutrons,(self.neutron*k)/(xenon_poison*0.8),dt*2)
        if not math.isfinite(self.next_neutrons):
            self.next_neutrons=1
        self.next_neutrons=clamp(self.next_neutrons,0,1e30)
        self.next_temp=self.temp+((reaction/(1+(self.core.water_mass/7000)*0.05))*dt)
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
        if not math.isfinite(self.core.water_temp):
            self.core.water_temp=20
        if not math.isfinite(self.next_temp):
            self.next_temp=self.temp
        self.next_temp=max(20,self.next_temp)
        self.neutron=self.next_neutrons
        self.temp=self.next_temp
        xenon_production=reaction*0.015*dt
        xenon_burnoff=self.neutron*0.01*dt
        xenon_decay=self.xenon*0.0025*dt
        self.xenon+=xenon_production-xenon_burnoff-xenon_decay
        self.xenon=max(0,self.xenon)
    class WaterCell: #the class of PURE AGONY.
        def __init__(self,x,y,gridcell,ix,iy,reactor,area):
            self.search_size=20
            self.temp=20
            self.neighbors=[]
            self.x=x
            self.y=y
            self.ix=ix
            self.iy=iy
            self.core=reactor
            self.owner=gridcell
            self.area=area
            self.max_mass=7000-(25*math.hypot(abs(grid_origin_x-self.x),abs(grid_origin_y-self.y)))
            self.max_level=self.max_mass
            self.mass=self.max_mass
            self.level=self.max_mass
            self.water_velocity=0
            self.water_direction=normalize360(360)
            self.offset_x=(self.x+7.5)+math.cos(math.radians(self.water_direction))*(7.5*self.water_velocity)
            self.offset_y=(self.y+7.5)-math.sin(math.radians(self.water_direction))*(7.5*self.water_velocity)
            self.turbulence_intensity=0
            self.viscosity=10/self.temp
            self.last_water_direction=self.water_direction
            self.max_hypot=math.hypot(7.5,30)
            self.void=0
            self.void_temp=self.temp
            self.boiling_point=320
            self.pressure=15
            self.density=safe_div(self.mass,self.level)
        def get_neighbor(self):
            if self.area is None:
                return
            directions = [
                (0, 1), (0, -1), (1, 0), (-1, 0),
                (1, 1), (1, -1), (-1, 1), (-1, -1)
            ]
                
            for dx, dy in directions:
                nx = self.ix + dx
                ny = self.iy + dy
                    
                if 0 <= nx < self.search_size and 0 <= ny < self.search_size:
                    neighbor=water_grid[ny][nx]
                    if neighbor.area is not None:
                        self.neighbors.append(neighbor)
        def update(self):
            if self.area is not None:
                self.level=self.mass*(self.temp**0.016)
                self.density=safe_div(self.mass,self.level)
                oscillation=random.uniform(-0.5,0.5)
                self.viscosity=10/self.temp
                D=0.01
                reynolds=(((self.water_velocity*5)*D)/self.viscosity)*10000
                self.turbulence_intensity=0.16 * (reynolds ** 0.25) #who is this mi bombo diddy epstein triple t fanum taxing level 10 rizzler gyatt blud 🥶🥶🗣🔥🔥🔥🥀🥀😭✌
                self.max_mass=clamp(self.max_mass,0,7000)
                self.max_level=clamp(self.max_level,0,7000)
                self.owner.temp,self.temp=heat_exchange(self.owner.temp,self.temp,(0.1+((self.water_velocity*0.9)/100)*(self.level/7000))*self.turbulence_intensity,dt)
                self.water_direction=self.water_direction+(self.water_direction-self.last_water_direction+oscillation)*(self.turbulence_intensity*15)
                self.last_water_direction=self.water_direction
                g=9.81
                for n in self.neighbors:
                    touching_area=(7000-(abs(n.level-self.level)))
                    self.water_velocity,n.water_velocity=heat_exchange(self.water_velocity,n.water_velocity,max(1-math.hypot(abs(self.offset_x-n.offset_x),abs(self.offset_y-n.offset_y))/self.max_hypot,0),dt)
                    self.water_direction,n.water_direction=heat_exchange(self.water_direction,n.water_direction,max(1-math.hypot(abs(self.offset_x-n.offset_x),abs(self.offset_y-n.offset_y))/self.max_hypot,0),dt)
                    self.mass,n.mass=heat_exchange(self.mass,n.mass,0.5+((self.owner.core.coolant_flow_rate/100)*0.5),dt)
                self.boiling=self.temp>self.boiling_point
                self.void_temp,self.temp=heat_exchange(self.void_temp,self.temp,0.016,dt)
                if not self.boiling:
                    self.void_temp=self.temp
                self.pressure=((self.core.pressurizer_temp*(((self.mass+(self.void*1600))*self.temp)/700000))/20)*(1+self.water_velocity)
                self.boiling_point=100*math.log10(9+abs(complex(self.pressure).real)**2.5)
                evaporation=(0.1*self.temp)*dt
                condensation=(0.02*self.pressure*self.void)*dt
                self.void+=evaporation-condensation
                self.mass-=evaporation-condensation
        def draw(self,screen):
            if self.owner.Area is not None:
                self.offset_x=(self.x+7.5)+math.cos(math.radians(normalize360(self.water_direction)))*clamp(7.5*self.water_velocity,0,7.5)
                self.offset_y=(self.y+7.5)-math.sin(math.radians(normalize360(self.water_direction)))*clamp(7.5*self.water_velocity,0,7.5)
                center_x=self.x+7.5
                center_y=self.y+7.5
                R=clamp(lerp(0,255,self.water_velocity),0,255)
                G=0
                B=0
                color=(R,G,B)
                pygame.draw.circle(screen,(100,100,100),(center_x,center_y),7.5,1)
                pygame.draw.line(screen,color,(center_x,center_y),(self.offset_x,self.offset_y))
class Reactor:
    def __init__(self,name):
        self.name=name
        self.void=0
        self.boron=0
        self.void=0
        self.void_temp=20
        self.precipitated_boron=0
        self.pressurizer_temp=20
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
        self.water_level=7000
        self.water_mass=7000
        self.water_density=0
        self.circ_water_mass=0
        self.void_temp=20
        self.CircSys=Reactor.CircSystems(None,None)
    def update(self):
        self.heater=knobs[0].value
        self.sprinkler=knobs[2].value
        self.fine_heater=knobs[1].value
        self.fine_sprinkler=knobs[3].value
        self.coolant_flow_rate=knobs[4].value
        circ_flow=((knobs[9].value/100)*(knobs[8].value/100))
        if self.circ_water_mass>0:
            self.water_mass+=450*(knobs[8].value/100)*dt
        if self.circ_water_mass<1000:
            self.water_mass-=450*(knobs[9].value/100)*dt
        if not math.isfinite(self.water_mass):
            self.water_mass=7000
        self.water_mass=clamp(self.water_mass,0,7000)
        self.circ_water_mass+=(450*(knobs[9].value/100))*dt
        self.circ_water_mass-=(450*(knobs[8].value/100))*dt
        self.circ_water_mass=clamp(self.circ_water_mass,0,1000)

        self.water_level=(self.water_mass+(self.water_temp/20))
        self.water_level=clamp(self.water_level,0,7000)

        max_saturation = (0.00001 * (self.water_temp ** 2) + 0.00033 * self.water_temp + 0.01) * (self.water_mass/7000)
        max_saturation=clamp(max_saturation,0,1)

        self.boron+=450*((circ_flow*((knobs[5].value/100)-(knobs[6].value/100))*(1-self.boron_conc))-(max(0,(self.boron-(7000*max_saturation)))))*dt
        self.precipitated_boron+=max((450*(circ_flow*((knobs[5].value/100)-(knobs[6].value/100))*(self.boron_conc))+(((self.boron)-(7000*max_saturation)))*dt),0)
        self.boron=clamp(self.boron,0,7000)

        self.boron_conc=self.boron/self.water_mass
        if not math.isfinite(self.boron_conc):
            self.boron_conc=0
        self.boron_conc=max(0,self.boron_conc)

        self.water_density=safe_div(self.water_mass,self.water_level)
        self.water_density=clamp(self.water_density,0,1)


        self.pressurizer_temp=lerp(self.pressurizer_temp,self.pressurizer_temp+20*((self.heater/100)+0.5*(self.fine_heater/100)),dt)
        self.pressurizer_temp=lerp(self.pressurizer_temp,20,((self.sprinkler/100)+0.5*(self.fine_sprinkler/100))*dt)
        self.pressure=(self.pressurizer_temp*(((self.water_mass+(self.void*1600))*self.water_temp)/700000))/20
        self.boiling_point=100*math.log10(9+abs(complex(self.pressure).real)**2.5)
        self.boiling=self.avg_temp>self.boiling_point
        self.water_mass=7000-self.void
    class CircSystems:    # ah shi here we go again
        def __init__(self,entrance_cell,exit_cell):
            self.entrance=entrance_cell
            self.exit=exit_cell
            self.inlet_valve=1
            self.outlet_valve=1
            self.coolant_flow_rate=0
            self.demin_dur=120000
            self.makeup_tank_mass=120000
            self.circ_mass=7000
            self.circ_pressure=1
            self.CVCS_entry=[]
            self.water_entry=[]
            for p in range(626):
                step=p*(dt*0.1)
                prefilled_water={"amount":7000*dt,"velocity":0,"progress":step,"temp":20,"boron":0}
                self.water_entry.append(prefilled_water)
            for c in range(626):
                CVCS_step=c*(dt*0.1)
                CVCS_prefilled_water={"amount":3500*dt,"velocity":0,"progress":CVCS_step,"temp":20,"boron":0}
                self.CVCS_entry.append(CVCS_prefilled_water)
        def update(self):
            if self.entrance is not None:
                self.coolant_flow_rate=pumps[0].force
                receiving=(450*self.inlet_valve*dt)*self.entrance.w_cell.water_velocity if ((450*dt)*self.entrance.w_cell.water_velocity)<=self.entrance.w_cell.mass*dt else self.entrance.w_cell.mass
                self.entrance.w_cell.mass=self.entrance.w_cell.mass-receiving if receiving<=self.entrance.w_cell.mass else 0
                self.water_entry.append({"amount":receiving,"velocity":self.entrance.w_cell.water_velocity,"progress":0,"temp":self.entrance.w_cell.temp})
                for p in self.water_entry:
                    p["velocity"]=lerp(p["velocity"],self.coolant_flow_rate,dt)
                    p["progress"]+=(1/15)*p["velocity"]*dt
                    if p["progress"]>=1:
                        self.exit.w_cell.mass+=(p["amount"]*self.outlet_valve*p["velocity"]) if p["amount"]>=(p["amount"]*self.outlet_valve*p["velocity"]) else p["amount"]
                        p["amount"]-=(p["amount"]*self.outlet_valve*p["velocity"]) if p["amount"]>=(p["amount"]*self.outlet_valve*p["velocity"]) else p["amount"]
                        p["temp"],self.exit.w_cell.temp=heat_exchange(p["temp"],self.exit.w_cell.temp,p["velocity"]*self.outlet_valve,dt)
                        p["velocity"],self.exit.w_cell.water_velocity=heat_exchange(p["velocity"],self.exit.w_cell.water_velocity,1,dt)
                    if (0.6-dt)<=p["progress"]<=(0.6+dt):
                        p["amount"]=p["amount"]-(7000*dt*(knobs[9].value/100)) if p["amount"]>=(7000*dt*(knobs[9].value/100)) else 0
                    p["progress"]=clamp(p["progress"],0,1)
                    p["amount"]=max(0,p["amount"])
                self.water_entry = [p for p in self.water_entry if p["amount"] > 0]
                for i in range(len(self.water_entry)):
                    previous=self.water_entry[i-1] if i>0 else None
                    current=self.water_entry[i]
                    later = self.water_entry[i+1] if i+1 < len(self.water_entry) else None
                    if previous is not None:
                        previous["velocity"],current["velocity"]=heat_exchange(previous["velocity"],current["velocity"],max(safe_div(1,dt)*(dt-abs((current["progress"]-dt)-previous["progress"])),0),dt)
                        previous["temp"],current["temp"]=heat_exchange(previous["temp"],current["temp"],max(safe_div(1,dt)*(dt-abs((current["progress"]-dt)-previous["progress"]))*abs(1-(previous["velocity"]-current["velocity"]),0)),dt)
                    if later is not None:
                        current["velocity"],later["velocity"]=heat_exchange(current["velocity"],later["velocity"],max(safe_div(1,dt)*(dt-abs((later["progress"]-dt)-current["progress"])),0),dt)
                        current["temp"],later["temp"]=heat_exchange(current["temp"],later["temp"],max(safe_div(1,dt)*(dt-abs((later["progress"]-dt)-current["progress"]))*abs(1-(current["velocity"]-later["velocity"])),0),dt)
                for shit in self.CVCS_entry:
                    flow_rate=pumps[1].force
                    boration=knobs[5].value*5
                    shit["velocity"]=lerp(shit["velocity"],flow_rate,dt)
                    shit["progress"]+=(1/15)*shit["velocity"]*dt
                    if 4.984<=shit["progress"]<=5.016:
                        if self.demin_dur>=0:
                            shit["boron"]=int(max(shit["boron"]-3*(knobs[7].value/100),0))
                            self.demin_dur=int(max(self.demin_dur-3*(knobs[7].value/100),0))
                    if 6.984<=shit["progress"]<=7.016:
                        shit["boron"]=int(max(shit["boron"]+))
                    for i_shit in range(len(self.CVCS_entry)):
                        shit_previous=self.CVCS_entry[i_shit-1] if i>0 else None
                        shit_current=self.CVCS_entry[i_shit]
                        shit_later=self.CVCS_entry[i_shit+1] if i_shit+1 < len(self.CVCS_entry) else None
                        if shit_previous is not None:
                            #shit_yourself() 
                            shit_previous["velocity"],shit_current["velocity"]=heat_exchange(shit_previous["velocity"],shit_current["velocity"],max(safe_div(1,dt)*(dt-abs((shit_current["progress"]-dt)-shit_previous["progress"])),0),dt)
                            shit_previous["temp"],shit_current["temp"]=heat_exchange(shit_previous["temp"],shit_current,max(safe_div(1,dt)*(dt-abs((current["progress"]-dt)-previous["progress"]))*abs(1-(previous["velocity"]-current["velocity"]),0)),dt)
class Pump:
    def __init__(self,name,parent_knob):
        self.force=0
        self.parent_knob=parent_knob
        self.toggle=True #TODO: gotta make parent toggle knob somewhere i think
    def update(self):
        target_force=(self.parent_knob.value/100)
        self.force=lerp(self.force,target_force if self.toggle else 0,dt*2 if self.toggle else dt)
class SteamGenerator:
    def __init__(self,core,name):
        self.name=name
        self.core=core
        self.water_temp=20
        self.pressure=6
        self.steam_mass=0
        self.water_mass=2000
        self.water_flow=1
        self.water_level=2000
        self.steam_valve=1
        self.steam=0
        self.boiling_point=0
    def update(self):
        self.pressure=(self.water_temp*(0.1+(self.steam/2000)*0.9))/20
        self.boiling_point=100*math.log10(9+self.pressure**2.9)
        self.core.water_temp,self.water_temp=heat_exchange(self.core.water_temp,self.water_temp,0.05*(self.water_flow*(self.water_mass/2000)),dt)
class Turbine:
    def __init__(self,SteamGenerator):
        self.SteamGenerator=SteamGenerator
        self.steam=0
        self.pressure=0
        self.steam_temp=20
        self.RPM=0
        self.total_generation=0
        self.force=0
        self.generation=0
    def update(self):
        self.pressure=(self.steam_temp*(0.1+(self.steam/2000)*0.9))/20
        self.SteamGenerator.water_temp,self.steam_temp=heat_exchange(self.SteamGenerator.water_temp,self.steam_temp,0.05*(0.005+self.SteamGenerator.steam_valve*(100-0.005)),dt)
        self.SteamGenerator.pressure,self.steam_pressure=heat_exchange(self.SteamGenerator.water_temp,self.pressure,0.05*(0.002+self.SteamGenerator.steam_valve*(100-0.002))*(1.0-self.steam*0.999),dt)
        self.force=(self.steam*self.pressure*self.steam_temp)/400
        self.RPM=lerp(self.RPM,self.force,dt)
        self.generation=(self.RPM*self.force)
        self.total_generation+=self.generation*dt
        self.boiling_point=100*math.log10(9+abs(complex(self.pressure).real)**2.9)
light_1=LightSource(400,300,300,0.5,500)
light_2=LightSource(400,300,300,0.5,500)
PM=PlayerManager()
last_knob_name=None
juggle_history=[]
cell_temp_total=0
all_cell_temp=[]
selected_area=[]
AREA_BUTTON_NAMES = {"A", "B", "C", "D", "E", "F", "G", "H"}
current_control_panel=1
comparison_control_panel=1
grid=[]
water_grid=[]
grid_size=20
cell_size=15
grid_origin_x=225
grid_origin_y=-20
core_center=(grid_size-1)/2
core_radius=8
sector_names=["A","B","C","D","E","F","G","H"]
boiling_point_meter=Meter(60,100,150,80,50,0,200,40)
water_level_meter=Meter(60,10,150,80,50,0,7000,40)
void_meter=Meter(60,190,150,80,50,0,80,40)
reactor=Reactor("default")
sg=SteamGenerator(reactor,"default")
turbine=Turbine(sg)
for iy in range(grid_size):
    row=[]
    water_row=[]
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
        water_row.append(cell.w_cell)
        row.append(cell)
    grid.append(row)
    water_grid.append(water_row)
for row in grid:
    for cell in row:
        cell.get_neighbor()
        cell.w_cell.get_neighbor()
for row in grid:
    for cell in row:
        if cell.iy==10 and cell.ix==17:
            reactor.CircSys.entrance=cell
        if cell.iy==10 and cell.ix==2:
            reactor.CircSys.exit=cell
pygame.init()
screen = pygame.display.set_mode((800, 600),pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Knob Test")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
sm=StyleManager()
knobs=[
    Knob(300,400, "Heater",1,light_1,160,value=0, radius=40, _type=2),
    Knob(300,500, "Fine Control Heater",1,light_1,150, value=0, radius=40, _type=2),
    Knob(180,400, "Sprinkler",1,light_1,160, value=0,radius=40, _type=2),
    Knob(180,500, "Fine Control Sprinkler",1,light_1,150, value=0, radius=40, _type=2),
    Knob(420, 300, "Coolant Flow Rate",1,light_1,170, value=0, radius=40, _type=2),
    Knob(420, 400, "Boration",1,light_1,160, value=0, radius=40, _type=2),
    Knob(420, 500,"Demin. control",1,light_1,150, value=0, radius=40, _type=2),
    Knob(300, 300, "switch",1,light_1,170, vmin=0, vmax=100, value=0, radius=40, _type=1),
    Knob(60,400,"Makeup Valve",1,light_1,160,value=0,radius=40,_type=2),
    Knob(60,500,"Letdown Valve",1,light_1,150,value=0,radius=40,_type=2)
    ]
knobs_2=[
    Knob(420, 300, "Charging Pump",1,light_2,170, value=0, radius=40, _type=2)
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
pumps=[
    Pump("RCP",knobs[4]),
    Pump("CP",None)
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
        if current_control_panel==1:
            CR_throttle.handle_event(e)
        for button in buttons:
            if current_control_panel==1:
                button.handle_event(e)
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_RIGHT:
                current_control_panel+=1
            elif e.key==pygame.K_LEFT:
                current_control_panel-=1
        if e.type == pygame.MOUSEBUTTONDOWN:
            all_button = next((button for button in buttons if button.name == "ALL"), None)
            if all_button and all_button.toggle:
                for button in buttons:
                    if button.name in AREA_BUTTON_NAMES:
                        button.toggle = True
    current_control_panel=clamp(current_control_panel,1,4)
    comparison_control_panel=current_control_panel
    all_cell_temp.clear()
    for row in grid:
        for cell in row:
            cell.update()
            cell.w_cell.update()

    for button in buttons:
        if current_control_panel==1:
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
            if current_control_panel==1:
                cell.get_color()
                cell.draw(screen)
                cell.w_cell.draw(screen)
    reactor.avg_temp=cell_temp_total/208
    selected_area.clear()
    for button in buttons:
        if current_control_panel==1:
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
    pygame.draw.rect(screen,(100,100,100),(370,350,100,225))
    pygame.draw.rect(screen,(50,50,50),(375,550,90,20))
    screen.blit(CVCS_text,(397,547.5))
    amount=len(juggle_history)
    if amount<2:
        p=c=None
    else:
        p=juggle_history[amount-2]
        c=juggle_history[amount-1]
    if p is not None and c is not None:
        if c["time"]-p["time"]>=4000 or amount>=4:
            juggle_history.clear()
            if amount>=4:
                sm.add_style_log(sm.style[5])
    if current_control_panel==1:
        CR_throttle.draw(screen)
    for knob in knobs:
        knob.draw(screen)
    for pump in pumps:
        pump.update()
    reactor.update()
    reactor.CircSys.update()
    sg.update()
    turbine.update()
    sm.update()
    sm.draw(screen,500,40)
    plant_terminal.draw(screen)
    boiling_point_meter.value=reactor.boiling_point
    boiling_point_meter.update()
    water_level_meter.value=reactor.water_level
    water_level_meter.update()
    void_meter.value=reactor.void
    void_meter.update()
    PM.update(sm.rank_dur,900,0)
    PM.draw(screen,700,300)
    if current_control_panel==1:
        boiling_point_meter.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()
