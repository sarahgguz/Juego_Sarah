import pygame
import io
import base64

def create_svg_surface(svg_code, size):
    """Convierte código SVG a una superficie de pygame usando renderizado en memoria"""
    # Codificar SVG como data URI
    svg_uri = f"data:image/svg+xml;base64,{base64.b64encode(svg_code.encode('utf-8')).decode('ascii')}"
    
    # Crear superficie temporal
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    try:
        # Intentar usar pygame.image.load_extended para cargar el SVG
        temp_surface = pygame.image.load(svg_uri)
        # Escalar a tamaño deseado
        temp_surface = pygame.transform.scale(temp_surface, size)
        surface.blit(temp_surface, (0, 0))
    except:
        # Si falla, usar formas básicas como respaldo
        if "player" in svg_code.lower():
            create_player_basic(surface)
        elif "grunt" in svg_code.lower():
            create_grunt_basic(surface)
        elif "hulk" in svg_code.lower():
            create_hulk_basic(surface)
        elif "brain" in svg_code.lower():
            create_brain_basic(surface)
        elif "human" in svg_code.lower():
            create_human_basic(surface)
        else:
            # Forma genérica
            pygame.draw.circle(surface, (255, 255, 255), (size[0]//2, size[1]//2), size[0]//2)
    
    return surface

# Funciones de respaldo para crear sprites básicos
def create_player_basic(surface):
    size = surface.get_size()
    pygame.draw.circle(surface, (0, 255, 255), (size[0]//2, size[1]//2), size[0]//2)
    pygame.draw.circle(surface, (0, 136, 255), (size[0]//2, size[1]//2), size[0]//3)

def create_grunt_basic(surface):
    size = surface.get_size()
    pygame.draw.polygon(surface, (255, 0, 0), [
        (size[0]//2, 2),
        (size[0]-2, size[1]-2),
        (2, size[1]-2)
    ])

def create_hulk_basic(surface):
    size = surface.get_size()
    pygame.draw.rect(surface, (0, 255, 0), (2, 2, size[0]-4, size[1]-4))
    pygame.draw.rect(surface, (0, 180, 0), (size[0]//4, size[1]//4, size[0]//2, size[1]//2))

def create_brain_basic(surface):
    size = surface.get_size()
    pygame.draw.circle(surface, (255, 0, 255), (size[0]//2, size[1]//2), size[0]//2)
    pygame.draw.arc(surface, (180, 0, 180), (5, 5, size[0]-10, size[1]-10), 0, 3.14, 3)

def create_human_basic(surface):
    size = surface.get_size()
    pygame.draw.circle(surface, (255, 255, 0), (size[0]//2, size[1]//3), size[0]//3)
    pygame.draw.rect(surface, (255, 255, 0), 
                    (size[0]//3, size[1]//2, size[0]//3, size[1]//2))

# SVG detallados para cada sprite
PLAYER_SVG = '''
<svg width="30" height="30" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="playerGrad" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
      <stop offset="0%" style="stop-color:#00FFFF;stop-opacity:1" />
      <stop offset="70%" style="stop-color:#0088FF;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0055FF;stop-opacity:1" />
    </radialGradient>
  </defs>
  <circle cx="15" cy="15" r="14" fill="url(#playerGrad)" stroke="#FFFFFF" stroke-width="1"/>
  <circle cx="15" cy="15" r="8" fill="#0055FF" stroke="#00FFFF" stroke-width="1"/>
  <circle cx="10" cy="10" r="2" fill="#FFFFFF" opacity="0.7"/>
  <path d="M 8,18 Q 15,22 22,18" stroke="#FFFFFF" stroke-width="1.5" fill="none"/>
</svg>
'''

GRUNT_SVG = '''
<svg width="20" height="20" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gruntGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF8800;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FF0000;stop-opacity:1" />
    </linearGradient>
  </defs>
  <polygon points="10,2 18,18 2,18" fill="url(#gruntGrad)" stroke="#880000" stroke-width="1"/>
  <circle cx="10" cy="8" r="2" fill="#FFFF00"/>
  <circle cx="10" cy="8" r="1" fill="#FF0000"/>
  <path d="M 6,14 L 14,14" stroke="#880000" stroke-width="1.5"/>
</svg>
'''

HULK_SVG = '''
<svg width="40" height="40" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="hulkGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#00FF00;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#008800;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect x="5" y="5" width="30" height="30" rx="5" ry="5" fill="url(#hulkGrad)" stroke="#005500" stroke-width="2"/>
  <rect x="12" y="12" width="16" height="16" rx="2" ry="2" fill="#008800" stroke="#005500" stroke-width="1"/>
  <circle cx="15" cy="15" r="2" fill="#FFFFFF"/>
  <circle cx="25" cy="15" r="2" fill="#FFFFFF"/>
  <path d="M 15,25 Q 20,28 25,25" stroke="#005500" stroke-width="2" fill="none"/>
</svg>
'''

BRAIN_SVG = '''
<svg width="25" height="25" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="brainGrad" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
      <stop offset="0%" style="stop-color:#FF88FF;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#880088;stop-opacity:1" />
    </radialGradient>
  </defs>
  <circle cx="12.5" cy="12.5" r="11" fill="url(#brainGrad)" stroke="#550055" stroke-width="1"/>
  <path d="M 6,10 Q 12.5,5 19,10" stroke="#550055" stroke-width="1.5" fill="none"/>
  <path d="M 6,15 Q 12.5,20 19,15" stroke="#550055" stroke-width="1.5" fill="none"/>
  <path d="M 8,7 Q 12.5,12 17,7" stroke="#550055" stroke-width="1" fill="none"/>
  <path d="M 8,18 Q 12.5,13 17,18" stroke="#550055" stroke-width="1" fill="none"/>
</svg>
'''

HUMAN_SVG = '''
<svg width="15" height="15" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="humanGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FFFF88;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FFFF00;stop-opacity:1" />
    </linearGradient>
  </defs>
  <circle cx="7.5" cy="4" r="3.5" fill="url(#humanGrad)" stroke="#888800" stroke-width="0.5"/>
  <rect x="6" y="7" width="3" height="6" rx="1" ry="1" fill="url(#humanGrad)" stroke="#888800" stroke-width="0.5"/>
  <circle cx="6" cy="3.5" r="0.8" fill="#000000"/>
  <circle cx="9" cy="3.5" r="0.8" fill="#000000"/>
  <path d="M 6,5 Q 7.5,6 9,5" stroke="#888800" stroke-width="0.5" fill="none"/>
  <line x1="4.5" y1="9" x2="6" y2="8" stroke="#888800" stroke-width="1"/>
  <line x1="9" y1="8" x2="10.5" y2="9" stroke="#888800" stroke-width="1"/>
</svg>
'''

PROJECTILE_SVG = '''
<svg width="8" height="8" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="projGrad" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
      <stop offset="0%" style="stop-color:#FFFFFF;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#88FFFF;stop-opacity:1" />
    </radialGradient>
  </defs>
  <circle cx="4" cy="4" r="3" fill="url(#projGrad)" stroke="#FFFFFF" stroke-width="0.5"/>
  <circle cx="3" cy="3" r="1" fill="#FFFFFF" opacity="0.8"/>
</svg>
'''

POWERUP_HEALTH_SVG = '''
<svg width="20" height="20" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="healthGrad" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
      <stop offset="0%" style="stop-color:#FF8888;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FF0000;stop-opacity:1" />
    </radialGradient>
  </defs>
  <circle cx="10" cy="10" r="9" fill="url(#healthGrad)" stroke="#FFFFFF" stroke-width="1"/>
  <rect x="5" y="8" width="10" height="4" rx="1" ry="1" fill="#FFFFFF"/>
  <rect x="8" y="5" width="4" height="10" rx="1" ry="1" fill="#FFFFFF"/>
</svg>
'''

POWERUP_SPEED_SVG = '''
<svg width="20" height="20" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="speedGrad" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
      <stop offset="0%" style="stop-color:#88FFFF;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0088FF;stop-opacity:1" />
    </radialGradient>
  </defs>
  <circle cx="10" cy="10" r="9" fill="url(#speedGrad)" stroke="#FFFFFF" stroke-width="1"/>
  <path d="M 10,3 L 15,12 L 10,10 L 5,12 Z" fill="#FFFFFF"/>
</svg>
'''

POWERUP_SHIELD_SVG = '''
<svg width="20" height="20" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="shieldGrad" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
      <stop offset="0%" style="stop-color:#FFFF88;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FFFF00;stop-opacity:1" />
    </radialGradient>
  </defs>
  <circle cx="10" cy="10" r="9" fill="url(#shieldGrad)" stroke="#FFFFFF" stroke-width="1"/>
  <path d="M 10,4 Q 15,6 15,12 Q 10,15 5,12 Q 5,6 10,4 Z" fill="#FFFFFF" opacity="0.6" stroke="#888800" stroke-width="1"/>
</svg>
'''

POWERUP_RAPID_SVG = '''
<svg width="20" height="20" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="rapidGrad" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
      <stop offset="0%" style="stop-color:#FF88FF;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FF00FF;stop-opacity:1" />
    </radialGradient>
  </defs>
  <circle cx="10" cy="10" r="9" fill="url(#rapidGrad)" stroke="#FFFFFF" stroke-width="1"/>
  <circle cx="10" cy="10" r="5" fill="#FFFFFF" opacity="0.5"/>
  <path d="M 5,10 L 15,10 M 10,5 L 10,15" stroke="#FFFFFF" stroke-width="2"/>
</svg>
'''

def create_player_sprite(size=(30, 30)):
    return create_svg_surface(PLAYER_SVG, size)

def create_grunt_sprite(size=(20, 20)):
    return create_svg_surface(GRUNT_SVG, size)

def create_hulk_sprite(size=(40, 40)):
    return create_svg_surface(HULK_SVG, size)

def create_brain_sprite(size=(25, 25)):
    return create_svg_surface(BRAIN_SVG, size)

def create_human_sprite(size=(15, 15)):
    return create_svg_surface(HUMAN_SVG, size)

def create_projectile_sprite(size=(8, 8)):
    return create_svg_surface(PROJECTILE_SVG, size)

def create_powerup_sprite(type, size=(20, 20)):
    if type == "health":
        return create_svg_surface(POWERUP_HEALTH_SVG, size)
    elif type == "speed":
        return create_svg_surface(POWERUP_SPEED_SVG, size)
    elif type == "shield":
        return create_svg_surface(POWERUP_SHIELD_SVG, size)
    elif type == "rapid":
        return create_svg_surface(POWERUP_RAPID_SVG, size)
    else:
        # Powerup genérico
        surface = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255), (size[0]//2, size[1]//2), size[0]//2)
        return surface 