import json, os, time, hoshino
from hoshino.typing import CQEvent
from hoshino import Service

sv = Service('room', enable_on_default=False, help_='')

json_path = os.path.join(os.path.dirname(__file__), 'room.json')
room = {}
def load_room():
    global room
    with open(json_path, encoding='utf8') as f:
        room = json.load(f)
load_room()

def render_forward_msg(msg_list: list):
    forward_msg = []
    for msg in msg_list:
        forward_msg.append({
            "type": "node",
            "data": {
                "name": '某不愿透露姓名的小环奈', #修改这里可以让bot转发消息时显示其他人
                "uin": '2779874515',
                "content": msg
            }
        })
    return forward_msg

def check_time():
    now = int(time.time())
    if room:
        for uid in room:
            if room[uid]['close_time'] < now:
                close_room(uid)
    else:
        return

def close_room(uid):
    global room
    if uid in room:
        room.pop(uid)
    save_room()

def save_room(): #存到本地，防止bot重启后数据丢失
    with open(json_path, 'w', encoding='utf8') as f:
        json.dump(room, f, ensure_ascii=False, indent=2)

def search_member(member):
    for uid in room:
        if member in room[uid]['member_list']:
            return uid
    else:
        return 0

@sv.on_fullmatch('开车帮助')
async def help_info(bot, ev):
    msg = '''[@bot]开车 [房间名称] [房间密钥] [房间超时时间]
[房间名称]：任意字符，不限制长度
[房间密钥]：房间加入方法，比如雀魂车建议为雀魂6位房间号
[房间超时时间]：（可选）该房间超过多长时间后自动关闭，单位分钟，默认30
[@bot]查车 查看自己所在车的信息，如果没有上车则发送所有车信息
[@bot]上车[创建者qq号]或[@创建者] @的优先度更高 当上车后车上人数大于等于4人，会对所有车上人员发送@提醒
[@bot]跳车 从自己当前所在车上离开
[@bot]解散 创建者用此指令解散自己所创建的车队'''
    await bot.send(ev, msg)

@sv.on_prefix(('开车'), only_to_me = True)
async def create_room(bot, ev):
    global room
    args = ev.message.extract_plain_text().strip().split()
    game_name = args[0]
    room_num = str(args[1])
    room_time = int(args[2]) if len(args) >= 3 else 30
    uid = str(ev.user_id)
    gid = ev.group_id
    check_time()
    if uid in room:
        await bot.send(ev, '你已经发过车了哦')
        return
    if search_member(uid):
        await bot.send(ev, '你已经在别人车上了哦，不可以脚踏两条船哦')
        return
    close_time = int(time.time()) + room_time * 60
    room[uid] = {'id':uid, 'game_name':game_name, 'room_num':room_num, 'member_list':[uid], 'close_time':close_time}
    save_room()
    msg = f'''创建成功，房间id:{room[uid]['id']}
游戏名称:{room[uid]['game_name']}
超时时间：{room_time}'''
    await bot.send(ev, msg)

@sv.on_fullmatch('查车', only_to_me = True)
async def search_room(bot, ev):
    msg = ''
    check_time()
    uid = search_member(str(ev.user_id))
    room_nums = len(room)
    if uid:
        msg += '您当前所在房间id:' + str(room[uid]['id']) +'\n'
        msg += '游戏名称:' + str(room[uid]['game_name']) + '\n'
        msg += '房间号:' + str(room[uid]['room_num']) + '\n'
        msg += '房间内成员有:\n'
        for member in room[uid]['member_list']:
            msg += member + '\n'
        msg += '房间自动解散剩余时间:' + str((room[uid]['close_time'] - int(time.time())) // 60) + '分钟\n\n'
        await bot.send(ev, msg.strip())
    elif room_nums <= 5:
        for uid in room:
            msg += 'id:' + str(room[uid]['id']) +'\n'
            msg += '游戏名称:' + str(room[uid]['game_name']) + '\n'
            msg += '房间号:' + str(room[uid]['room_num']) + '\n'
            msg += '房间内成员有:\n'
            for member in room[uid]['member_list']:
                msg += member + '\n'
            msg += '房间自动解散剩余时间:' + str((room[uid]['close_time'] - int(time.time())) // 60) + '分钟\n\n'
        await bot.send(ev, msg.strip())
    else:
        msg_list = []
        for uid in room:
            msg = ''
            msg += 'id:' + str(room[uid]['id']) +'\n'
            msg += '游戏名称:' +str(room[uid]['game_name']) + '\n'
            msg += '房间号:' + str(room[uid]['room_num']) + '\n'
            msg += '房间内成员有:\n'
            for member in room[uid]['member_list']:
                msg += member + '\n'
            msg += '房间自动解散剩余时间:' + str((room[uid]['close_time'] - int(time.time())) // 60) + '分钟'
            msg_list.append(msg)
        forward_msg = render_forward_msg(msg_list)
        await hoshino.get_bot().send_group_forward_msg(group_id=ev.group_id, messages = forward_msg)

@sv.on_rex('上车', only_to_me = True)
async def join_room(bot, ev):
    check_time()
    for msg in ev.message:
        if msg.type == 'at':
            uid = str(msg.data['qq'])
            break
    else:
        uid = '' 
        m = msg.data['text'].strip()
        for i in m:
            if i.isdigit():
               uid += i
    new_member = str(ev.user_id)
    if uid not in room:
        await bot.send(ev, '没有这俩车哦')
        return
    if search_member(new_member):
        await bot.send(ev, '你已经在别人车上了哦，不可以脚踏两条船哦')
        return
    room[uid]['member_list'].append(new_member)
    save_room()
    if len(room[uid]['member_list']) >= 4:
        at_msg = ''
        for member in room[uid]['member_list']:
            at_msg += f'[CQ:at,qq={member}],'
        await bot.send(ev, f'''{at_msg} {new_member}已上车，当前车上已有{len(room[uid]['member_list'])}人''')
    else:
        await bot.send(ev, f'''{new_member}已上车，当前车上已有{len(room[uid]['member_list'])}人''')
        
@sv.on_fullmatch('跳车', only_to_me = True)
async def exit_room(bot, ev):
    check_time()
    global room
    if not room:
        return
    member = str(ev.user_id)
    uid = search_member(member)
    if not uid:
        await bot.send(ev, '车队中没有你哦')
    room[uid]['member_list'].remove(member)
    save_room()
    n = len(room[uid]['member_list'])
    if not n:
        close_room(uid)
        await bot.send(ev, f'''车{uid}已解散''')
        return
    await bot.send(ev, f'''{member}已下车，当前车上有{n}人''')

@sv.on_fullmatch('解散', only_to_me = True)
async def master_close_room(bot,ev):
    uid = str(ev.user_id)
    if uid in room:
        close_room(uid)
        await bot.send(ev, f'{uid}已解散')
    else:
        await bot.send(ev, '你还没有发车哦')
