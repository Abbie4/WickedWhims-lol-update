from Utilities import extract_folder, decompile_dir
from settings import *

ea_folder = 'EA'
if not os.path.exists(ea_folder):
    os.mkdir(ea_folder)

gameplay_folder_data = os.path.join(game_folder, 'Data', 'Simulation', 'Gameplay')
gameplay_folder_game = os.path.join(game_folder, 'Game', 'Bin', 'Python')

decompile_dir('./decompiled')
