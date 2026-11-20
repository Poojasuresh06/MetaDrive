import numpy as np

# 1. Legacy NumPy compatibility patches
np.float = float
np.int = int
np.bool = bool
np.typeDict = np.sctypeDict

# 2. Panda3D input handling
from panda3d.core import KeyboardButton

import metadrive
from metadrive import MetaDriveEnv

if __name__ == "__main__":
    config = {
        "use_render": True,
        "manual_control": False,  # Managed directly via custom loop
    }
    
    env = MetaDriveEnv(config=config)
    try:
        env.reset()
        
        # Target keys explicitly using Panda3D string characters
        key_w = KeyboardButton.ascii_key('w')
        key_s = KeyboardButton.ascii_key('s')
        key_a = KeyboardButton.ascii_key('a')
        key_d = KeyboardButton.ascii_key('d')
        
        while True:
            steering = 0.0
            throttle_brake = 0.0
            
            # Read input directly from the active Panda3D mouse/keyboard watcher
            mw = env.engine.mouseWatcherNode
            
            if mw.is_button_down(key_a):
                steering += 1.0     # Steer Left
            if mw.is_button_down(key_d):
                steering -= 1.0     # Steer Right
            if mw.is_button_down(key_w):
                throttle_brake += 1.0  # Accelerate
            if mw.is_button_down(key_s):
                throttle_brake -= 1.0  # Brake / Reverse
            
            # Step the simulation with real-time keyboard inputs
            action = [steering, throttle_brake]
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            
            if done:
                env.reset()
    finally:
        env.close()