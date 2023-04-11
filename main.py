import os, sys, traceback, requests, yaml
from modules import setup, gui, updater, manager

# import yaml files 
with open("configs/config.yml",'r') as cfg_file:
    cfg = yaml.safe_load(cfg_file)
with (
    open("configs/"+cfg["asset_list"],"r") as asset_file,
    open("configs/data.yml","a+") as data_file
):
    yml = yaml.safe_load(asset_file)
    data = yaml.safe_load(data_file) if data_file.read() else {}
    print(data_file)
    print(data)

def menu():
    print(f"elis mod & plugin updater indev")
    menu_opt = gui.options(["quit",f"download updates via {cfg['asset_list']}",f"manage {cfg['asset_list']} (WIP)"],"type your selection: ")
    if menu_opt == 0: exit()
    elif menu_opt == 1: updater.update(yml, data)
    elif menu_opt == 2: manager.manage(yml)

while True:
    menu()