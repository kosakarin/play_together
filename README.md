# play_together
适用于HoshinoBot的快速组队插件

感谢[@soap_spree](https://github.com/soapspree)协助完善本插件

# 本插件有什么用处？

你在群中想要和群友一起快乐雀魂，然而一直三缺一······ 你在群中想要加入刚刚群友开的黑车，然而他死活没回复你······不要担心！万能群聊bot来帮忙了！

安装本插件后，如果你想上车，bot会帮助你盯着群友，当他们发车时，记下相关信息，这样你随时随地可以向bot询问有没有去幼儿园的车！

如果你想开车，bot会帮你一直盯着群友谁想加入你的车队，当人数足够时自动提醒你！免去你需要一直全神贯注的观察群聊的困恼！

（草，好怪）

反正总而言之就是写了个组队辅助插件

# 安装说明

1. 在`HoshinoBot/hoshino/modules`目录下克隆本仓库：`git clone https://github.com/kosakarin/play_together`

2. 修改`HoshinoBot/hoshino/config/__bot__.py`，在`MODULES_ON`中加入`play_together`

3. 重启HoshinoBot

4. 在需要开启插件的群中发送`启用 play_together`

# 使用说明

[@bot]开车 [房间名称] [房间密钥] [房间人数] [房间超时时间]

--[房间名称]：任意字符，不限制长度

--[房间密钥]：房间加入方法，比如雀魂车建议为雀魂6位房间号，也可以是其他你需要补充的信息

--[房间人数]：房间的最大成员数，设置为0则不限制，满员将自动发送@提醒

--[房间超时时间]：（可选）该房间超过多长时间后自动关闭，单位分钟，默认30

[@bot]查车 查看自己所在车的信息，如果没有上车则发送所有车信息

[@bot]上车 [房间编号]或[@创建者]，@的优先度更高

[@bot]跳车 从自己当前所在车队中离开

[@bot]发车 创建者用此指令一键@当前在车队中的全部成员

[@bot]解散 创建者用此指令解散自己所创建的车队

[@bot]添加备注 给自己在车队里添加一段个性化备注(请勿使用奇怪字段，我们是去幼儿园的车

# 参考用法

[@bot开车 雀魂🤺1=3 114514 4]创建一个1=3的雀魂车 房间号114514

[@bot开车 人民广场风云再起 舞萌地插排队用 0 1000]创建一个排卡车

[@bot开车 征婚 本人男 2]？？？？？？？？？？？

# 其他

数据保存方式：缓存+本地json保存备份，不用担心重启bot后数据丢失

是否支持群隔离：暂不支持，实现方法不难，在room中声明每个id下的新的映射关系‘group_id’,在使用时加上‘group_id’的判断即可
