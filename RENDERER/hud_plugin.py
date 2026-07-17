import pygame
import moderngl
import numpy as np
import time
from SYSTEM.events import bus
from SYSTEM.plugin_manager import Plugin

class HUDPlugin(Plugin):
    def __init__(self):
        super().__init__("HUDPlugin")
        self.screen = None
        self.ctx = None
        
        self.jarvis_state = "Sleeping"
        self.power_mode = "normal"
        self.cpu = 0
        self.ram = 0
        self.weather = "Tidak tersedia"
        
        self.plugin_statuses = {}
        
        self.prog = None
        self.vbo = None
        self.vao = None
        
    def start(self):
        print("[HUD] Initializing Premium HUD Interface...")
        pygame.init()
        # Setup for ModernGL
        pygame.display.set_mode((1280, 720), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
        pygame.display.set_caption("JARVIS OS 4.0")
        
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        
        bus.subscribe("jarvis_state", self._on_jarvis_state)
        bus.subscribe("power_state_changed", self._on_power_state)
        bus.subscribe("system_stats_update", self._on_stats)
        bus.subscribe("weather_update", self._on_weather)
        bus.subscribe("plugin_status_change", self._on_plugin_status)
        
        self._init_shaders()
        
    def _init_shaders(self):
        vertex_shader = '''
            #version 330 core
            in vec2 in_vert;
            in vec2 in_texcoord;
            out vec2 v_texcoord;
            void main() {
                gl_Position = vec4(in_vert, 0.0, 1.0);
                v_texcoord = in_texcoord;
            }
        '''
        
        fragment_shader = '''
            #version 330 core
            uniform sampler2D texture0;
            uniform float time;
            in vec2 v_texcoord;
            out vec4 f_color;
            void main() {
                vec4 tex_color = texture(texture0, v_texcoord);
                // Premium holographic glow effect
                float pulse = 0.9 + 0.1 * sin(time * 2.0);
                f_color = vec4(tex_color.rgb * pulse, tex_color.a);
            }
        '''
        
        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        
        vertices = np.array([
            -1.0,  1.0, 0.0, 1.0,
            -1.0, -1.0, 0.0, 0.0,
             1.0,  1.0, 1.0, 1.0,
             1.0, -1.0, 1.0, 0.0,
        ], dtype='f4')
        
        self.vbo = self.ctx.buffer(vertices)
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert', 'in_texcoord')

    def _on_jarvis_state(self, state):
        self.jarvis_state = state
        
    def _on_power_state(self, state):
        self.power_mode = state
        
    def _on_stats(self, stats):
        self.cpu = stats.get("cpu", 0)
        self.ram = stats.get("ram", 0)
        
    def _on_weather(self, w):
        self.weather = w
        
    def _on_plugin_status(self, data):
        self.plugin_statuses[data["name"]] = data["status"]

    def stop(self):
        pygame.quit()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bus.publish("tts_speak", "Mematikan sistem.")
                import sys
                sys.exit(0)
                
        # 1. Render UI to surface
        surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        
        font = pygame.font.SysFont("courier new", 20)
        title_font = pygame.font.SysFont("courier new", 36, bold=True)
        
        # Title
        title = title_font.render("JARVIS OS 4.0", True, (150, 220, 255))
        surface.blit(title, (40, 40))
        
        # State
        state_color = (0, 255, 255) if self.jarvis_state != "Sleeping" else (100, 100, 100)
        state_text = font.render(f"STATUS : {self.jarvis_state.upper()}", True, state_color)
        surface.blit(state_text, (40, 100))
        
        # Power Mode
        mode_text = font.render(f"POWER  : {self.power_mode.upper()} MODE", True, (150, 220, 255))
        surface.blit(mode_text, (40, 140))
        
        # Stats
        cpu_text = font.render(f"CPU USG: {self.cpu}%", True, (150, 220, 255))
        ram_text = font.render(f"RAM USG: {self.ram}%", True, (150, 220, 255))
        surface.blit(cpu_text, (40, 200))
        surface.blit(ram_text, (40, 230))
        
        # Weather
        weather_text = font.render(f"WEATHER: {self.weather}", True, (150, 220, 255))
        surface.blit(weather_text, (40, 280))
        
        # AI Animations (Center)
        center = (640, 360)
        base_radius = 180
        t = time.time()
        
        if self.jarvis_state in ["Listening", "Understanding"]:
            radius = base_radius + int(20 * np.sin(t * 5))
            pygame.draw.circle(surface, (0, 255, 255, 150), center, radius, 3)
            pygame.draw.circle(surface, (0, 100, 255, 80), center, radius + 20, 1)
        elif self.jarvis_state in ["Processing", "Thinking"]:
            radius = base_radius + int(30 * np.sin(t * 10))
            pygame.draw.circle(surface, (255, 150, 0, 150), center, radius, 5)
            pygame.draw.circle(surface, (255, 50, 0, 80), center, radius + 15, 2)
        elif self.jarvis_state == "Generating Response":
            radius = base_radius + int(20 * np.sin(t * 15))
            pygame.draw.circle(surface, (255, 200, 0, 150), center, radius, 4)
        elif self.jarvis_state == "Speaking":
            radius = base_radius + int(40 * np.sin(t * 12))
            pygame.draw.circle(surface, (0, 255, 100, 180), center, radius, 4)
            pygame.draw.circle(surface, (0, 150, 255, 100), center, base_radius, 2)
        else:
            pygame.draw.circle(surface, (50, 100, 150, 80), center, base_radius, 1)
            pygame.draw.circle(surface, (50, 100, 150, 40), center, base_radius + 10, 1)
            
        # Draw tech rings
        for i in range(3):
            r = base_radius + 40 + i*20
            pygame.draw.arc(surface, (100, 200, 255, 100), 
                            (center[0]-r, center[1]-r, r*2, r*2), 
                            t + i, t + i + 2, 2)
                            
        # Plugin Statuses (Right Panel)
        y_offset = 40
        status_font = pygame.font.SysFont("courier new", 16)
        header = font.render("SYSTEM MODULES", True, (150, 220, 255))
        surface.blit(header, (1000, y_offset))
        y_offset += 40
        
        for name, status in self.plugin_statuses.items():
            if status == "ACTIVE":
                color = (0, 255, 100)
            elif status == "FAILED":
                color = (255, 50, 50)
            elif status == "SLEEPING":
                color = (150, 150, 150)
            else:
                color = (200, 200, 200)
            
            # Format name
            display_name = name.replace("Plugin", "").replace("System", "").replace("Management", "").replace("Core", "").upper()
            text_str = f"{display_name.ljust(15, '.')} {status}"
            text = status_font.render(text_str, True, color)
            surface.blit(text, (1000, y_offset))
            y_offset += 25
        
        # 2. ModernGL pass
        texture_data = pygame.image.tostring(surface, "RGBA", True)
        texture = self.ctx.texture(surface.get_size(), 4, texture_data)
        texture.use(0)
        
        if 'time' in self.prog:
            self.prog['time'].value = t
            
        self.ctx.clear(0.01, 0.02, 0.04, 1.0)
        self.vao.render(moderngl.TRIANGLE_STRIP)
        
        texture.release()
        pygame.display.flip()
