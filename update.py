# -*- coding:utf8 -*-
"""每日运行，更新必要的数据"""
import os.path, time
import net

# get the game list from steamspy
# check for last run time, only run once a day
need_to_run = True
if os.path.isfile(net.SPY_JSON):
    now_time = time.time()
    file_change_time = os.path.getmtime(net.SPY_JSON)
    if now_time - file_change_time < 60 * 60 * 24:
        need_to_run = False

if need_to_run:
    steamspyjson = net.get_all_game()
    with open(net.SPY_JSON, 'w') as ft:
        ft.write(steamspyjson)
