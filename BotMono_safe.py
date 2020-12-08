#!/usr/bin/python3
# -*-coding:utf-8-*-
"""
Created on 2020/12/3
「君は道具ではなく、その名が似合う人になろんだ」
@author: Jerry_FaGe
"""
import json
import time
from utils import rtext as r
from imp import load_source

PlayerInfoAPI = load_source('PlayerInfoAPI', './plugins/PlayerInfoAPI.py')
config_path = './config/BotMono.json'
prefix_short = '!!bm'
prefix = '!!botmono'
bot_dic = {}
bot_list = []
help_msg = '''
================== §bBotMono §r==================
§6欢迎使用由@Jerry-FaGe开发的假人全物品（暂时并不全）插件！
§6你可以在Github搜索MCDR-BotMono找到本项目！
「君は道具ではなく、その名が似合う人になろんだ」
本插件中§d{prefix_short}§r与§d{prefix}§r效果相同，两者可以互相替换
§b{prefix_short} §r显示本帮助信息
§b{prefix_short} list §r显示由本插件召唤出的假人列表
§b{prefix_short} reload §r重载插件配置
§b{prefix_short} <mono> §r输出一个可点击的界面，自动根据假人是否在线改变选项
§b{prefix_short} <mono> spawn §r召唤一个用于存储<mono>的假人
§b{prefix_short} <mono> kill §r干掉用于存储<mono>的假人
§b{prefix_short} <mono> here §r将用于存储<mono>的假人传送到自己身边
§b{prefix_short} <mono> one §r假人扔出一个手中物品（执行此条前无需执行spawn，如假人不存在会自动创建）
§b{prefix_short} <mono> all §r假人扔出身上所有物品（执行此条前无需执行spawn，如假人不存在会自动创建）
§b{prefix_short} <mono> handall §r假人扔出手中所有物品（执行此条前无需执行spawn，如假人不存在会自动创建）
'''.format(prefix=prefix, prefix_short=prefix_short)
help_head = """
================== §bBotMono §r==================
§6欢迎使用由@Jerry-FaGe开发的假人全物品（暂时并不全）插件！
§6你可以在Github搜索MCDR-BotMono找到本项目！
「君は道具ではなく、その名が似合う人になろんだ」
本插件中§d{prefix_short}§r与§d{prefix}§r效果相同，两者可以互相替换
""".format(prefix=prefix, prefix_short=prefix_short)
help_body = {
    f"§b{prefix_short}": "§r显示本帮助信息",
    f"§b{prefix_short} list": "§r显示由本插件召唤出的假人列表",
    f"§b{prefix_short} reload": "§r重载插件配置",
    f"§b{prefix_short} <mono>": "§r输出一个可点击的界面，自动根据假人是否在线改变选项",
    f"§b{prefix_short} <mono> spawn": "§r召唤一个用于存储<mono>的假人",
    f"§b{prefix_short} <mono> kill": "§r干掉用于存储<mono>的假人",
    # f"§b{prefix_short} <mono> here": "§r将用于存储<mono>的假人传送到自己身边",
    f"§b{prefix_short} <mono> one": "§r假人扔出一个手中物品（执行此条前无需执行spawn，如假人不存在会自动创建）",
    f"§b{prefix_short} <mono> all": "§r假人扔出身上所有物品（执行此条前无需执行spawn，如假人不存在会自动创建）",
    f"§b{prefix_short} <mono> handall": "§r假人扔出手中所有物品（执行此条前无需执行spawn，如假人不存在会自动创建）"
}


class Info:
    def __init__(self, content):
        self.content = content
        self.is_user = True
        self.is_player = False
        self.player = "Jerry_FaGe"


class Server:
    def reply(self, info, msg, encoding=None):
        print("发送消息: " + msg)

    def execute(self, name):
        print("执行命令: " + name)


def on_load(server, old):
    global bot_list
    server.add_help_message(prefix_short, f'假人物品映射(和谐版)，输入§6{prefix_short}查看帮助')
    if old is not None and old.bot_list is not None:
        bot_list = old.bot_list
    else:
        bot_list = []
    try:
        read()
    except Exception as e:
        server.say('§b[BotMono]§4配置加载失败，请确认配置路径是否正确：{}'.format(e))


def get_pos(server, info):
    PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
    pos = PlayerInfoAPI.getPlayerInfo(server, info.player, 'Pos')
    dim = PlayerInfoAPI.getPlayerInfo(server, info.player, 'Dimension')
    facing = PlayerInfoAPI.getPlayerInfo(server, info.player, 'Rotation')
    return pos, dim, facing


def spawn_cmd(server, info, name):
    if info.is_player:
        pos, dim, facing = get_pos(server, info)
        return f'/player {name} spawn at {pos[0]} {pos[1]} {pos[2]} facing {facing[0]} {facing[1]} in {dim}'
    else:
        return f'/player {name} spawn'


def read():
    global bot_dic
    with open(config_path, encoding='utf8') as f:
        bot_dic = json.load(f)


def save():
    with open(config_path, 'w', encoding='utf8') as f:
        json.dump(bot_dic, f, indent=4, ensure_ascii=False)


def search(mono):
    for k, v in bot_dic.items():
        if mono in v:
            return k


def spawn(server, info, name):
    return spawn_cmd(server, info, name)


def kill(name):
    return f'/player {name} kill'


def drop_one(name):
    return f'/player {name} drop once'


def drop_all(name):
    return f'/player {name} dropStack all'


def drop_handall(name):
    return f'/player {name} dropStack once'


def on_info(server, info):
    if info.is_user:
        if info.content.startswith(prefix) or info.content.startswith(prefix_short):
            global bot_dic, bot_list
            read()
            args = info.content.split(' ')

            if len(args) == 1:
                # server.reply(info, help_msg)
                head = [help_head]
                body = [r.RText(f'{k} {v}\n').c(
                    r.RAction.suggest_command, k.replace('§b', '')).h(v)
                        for k, v in help_body.items()]
                server.reply(info, r.RTextList(*(head + body)))

            elif len(args) == 2:
                if args[1] == "list":
                    msg = ['\n', f'当前共有{len(bot_list)}个假人在线']
                    for name in bot_list:
                        bot_info = r.RTextList(
                            '\n'
                            f'§7----------- §6{name}§7 -----------\n',
                            f'§7此假人存放:§6 {bot_dic.get(name, "没有索引")}\n',
                            # r.RText('§d[传送]  ').c(
                            #     r.RAction.run_command, f'{prefix_short} {name} here').h(f'§7将§6{name}§7传送至身边'),
                            r.RText('§d[罪人按钮]  ').c(
                                r.RAction.run_command, f'{prefix_short} {name} here').h('§4使用此功能你就会变成罪人'),
                            r.RText('§d[扔出所有]  ').c(
                                r.RAction.run_command, f'{prefix_short} {name} all').h(f'§6{name}§7扔出身上所有物品'),
                            r.RText('§d[扔出一个]  ').c(
                                r.RAction.run_command, f'{prefix_short} {name} one').h(f'§6{name}§7扔出一个物品'),
                            r.RText('§d[扔出手中]  ').c(
                                r.RAction.run_command, f'{prefix_short} {name} handall').h(f'§6{name}§7扔出手中物品'),
                            r.RText('§d[下线]  ').c(
                                r.RAction.run_command, f'{prefix_short} {name} kill').h(f'§7干掉§6{name}')
                        )
                        msg.append(bot_info)
                    server.reply(info, r.RTextList(*msg))

                elif args[1] == "reload":
                    try:
                        read()
                        server.say('§b[BotMono]§a由玩家§d{}§a发起的BotMono重载成功'.format(info.player))
                    except Exception as e:
                        server.say('§b[BotMono]§4由玩家§d{}§4发起的BotMono重载失败：{}'.format(info.player, e))

                elif search(args[1]):
                    name = search(args[1])
                    if name not in bot_list:
                        # server.execute(spawn(server, info, search(args[1])))
                        # bot_list.append(search(args[1]))
                        msg = r.RTextList(
                            '\n'
                            f'§7----------- §6{name}§7 -----------\n',
                            f'§7此假人存放:§6 {bot_dic.get(search(args[1]), "没有索引")}\n',
                            r.RText('§d[召唤]  ').c(
                                r.RAction.run_command, f'{prefix_short} {name} spawn').h(f'§7召唤§6{name}'),
                            r.RText('§d[扔出所有]  ').c(
                                r.RAction.run_command, f'{prefix_short} {name} all').h(f'§6{name}§7扔出身上所有物品'),
                            r.RText('§d[扔出一个]  ').c(
                                r.RAction.run_command, f'{prefix_short} {name} one').h(f'§6{name}§7扔出一个物品'),
                            r.RText('§d[扔出手中]  ').c(
                                r.RAction.run_command, f'{prefix_short} {name} handall').h(f'§6{name}§7扔出手中物品')
                        )
                        server.reply(info, msg)
                    else:
                        # server.reply(info, f"§b[BotMono]§4假人§d{search(args[1])}§6（{args[1]}）§4已经在线")
                        msg = r.RTextList(
                            '\n'
                            f'§7----------- §6{name}§7 -----------\n',
                            f'§7此假人存放:§6 {bot_dic.get(search(args[1]), "没有索引")}\n',
                            r.RText('§d[罪人按钮]  ').c(
                                r.RAction.run_command, f'{prefix_short} {name} here').h('§4使用此功能你就会变成罪人'),
                            r.RText('§d[扔出所有]  ').c(
                                r.RAction.run_command, f'{prefix_short} {name} all').h(f'§6{name}§7扔出身上所有物品'),
                            r.RText('§d[扔出一个]  ').c(
                                r.RAction.run_command, f'{prefix_short} {name} one').h(f'§6{name}§7扔出一个物品'),
                            r.RText('§d[扔出手中]  ').c(
                                r.RAction.run_command, f'{prefix_short} {name} handall').h(f'§6{name}§7扔出手中物品'),
                            r.RText('§d[下线]  ').c(
                                r.RAction.run_command, f'{prefix_short} {name} kill').h(f'§7干掉§6{name}')
                        )
                        server.reply(info, msg)

                else:
                    server.reply(info, f"§b[BotMono]§4未查询到§d{args[1]}§4对应的假人")
            elif len(args) == 3:
                name = search(args[1])
                if name:
                    if args[2] == "spawn":
                        if name not in bot_list:
                            server.execute(spawn(server, info, name))
                            bot_list.append(name)
                        else:
                            server.reply(info, f"§b[Botmono]§4假人§d{name}§6（{args[1]}）§4已经在线")

                    elif args[2] == "kill":
                        if name in bot_list:
                            server.execute(kill(name))
                            bot_list.remove(name)
                            server.reply(info, f"§b[BotMono]§a假人§d{name}§6（{args[1]}）§a已被下线")

                    elif args[2] == "here":
                        if name in bot_list:
                            # server.execute(f"/tp {name} {info.player}")
                            server.reply(info, f"§b[BotMono]§4停用了，我可不想当罪人")
                        else:
                            server.reply(info, f"§b[BotMono]§4假人§d{name}§6（{args[1]}）§4不在线")

                    elif args[2] == "one":
                        if name not in bot_list:
                            server.execute(spawn(server, info, name))
                            bot_list.append(name)
                            server.reply(info, f"§b[BotMono]§a已自动创建假人§d{name}§6（{args[1]}）")
                            time.sleep(1)
                        server.execute(drop_one(name))
                        server.reply(info, f"§b[BotMono]§a假人§d{name}§6（{args[1]}）§a扔出1个物品")

                    elif args[2] == "all":
                        if name not in bot_list:
                            server.execute(spawn(server, info, name))
                            bot_list.append(name)
                            server.reply(info, f"§b[BotMono]§a已自动创建假人§d{name}§6（{args[1]}）")
                            time.sleep(1)
                        server.execute(drop_all(name))
                        server.reply(info, f"§b[BotMono]§a假人§d{name}§6（{args[1]}）§a扔出身上所有物品")

                    elif args[2] == "handall":
                        if name not in bot_list:
                            server.execute(spawn(server, info, name))
                            bot_list.append(name)
                            server.reply(info, f"§b[BotMono]§a已自动创建假人§d{name}§6（{args[1]}）")
                            time.sleep(1)
                        server.execute(drop_handall(name))
                        server.reply(info, f"§b[BotMono]§a假人§d{name}§6（{args[1]}）§a扔出手中所有物品")

                    else:
                        server.reply(info, f"§b[BotMono]§4参数输入错误，输入§6{prefix_short}§4查看帮助信息")

                else:
                    server.reply(info, f"§b[BotMono]§4未查询到§d{args[1]}§4对应的假人")


def on_server_stop(server, return_code):
    global bot_list
    bot_list = []


if __name__ == '__main__':
    a = Info("!!bm 发哥 here")
    s = Server()
    on_info(s, a)
