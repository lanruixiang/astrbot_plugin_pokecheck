from astrbot.api.all import *
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.event.filter import event_message_type, EventMessageType
import astrbot.api.message_components as Comp

@register("戳！", "huanyan434", "一个检测“戳”关键词的插件", "1.1", "https://github.com/huanyan434/astrbot_plugin_pokecheck")
class PokeCheckPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent) -> MessageEventResult:
        msg_obj = event.message_obj
        raw_message = msg_obj.raw_message
        text = msg_obj.message_str or ""
        if "戳" in text:
            messages = event.get_messages()
            target_user_id = next((str(seg.qq) for seg in messages if (isinstance(seg, Comp.At))), None)

            # 检查是否有 @ 的用户
            if target_user_id is not None:
                return
            # 发送戳一戳
            if event.get_platform_name() == "aiocqhttp":
                from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
                assert isinstance(event, AiocqhttpMessageEvent)
                client = event.bot
                sender_id = raw_message.get('user_id')
                group_id = raw_message.get('group_id')
                payloads = {"user_id": sender_id}
                if group_id:
                    payloads["group_id"] = group_id
                    try:
                        await client.api.call_action('send_poke', **payloads)
                    except Exception as e:
                        pass
