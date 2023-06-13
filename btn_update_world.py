from chatbot import chatbot
from datetime import datetime
import redis_cli

# 更新世界状态
def update_world(story_id):

    # 检查故事ID
    story_data = redis_cli.get_story(story_id)
    if story_data is None:
        return "故事不存在：" + story_id, "故事不存在：" + story_id
    
    # 检查模板ID
    temp_name = story_data['template_id']
    temp_data = redis_cli.get_template(temp_name)
    if temp_data is None:
        return "故事对应的模板不存在：" + story_id, "故事对应的模板不存在：" + story_id
    
    # 更新世界状态
    new_world_state = chatbot.ask(story_id, "system", temp_data['world_engine_update_template'])
    
    # 再次开始多轮对话
    new_dialog = chatbot.ask(story_id, "system", temp_data['dialog_engine_update_template'])

    # 追加到缓存
    current_date_and_time = str(datetime.now())
    story_data['world_record_txt'] += "\n\n------------" + current_date_and_time + "-----------\n" + new_world_state
    story_data['dialog_record_txt'] += "\n\n------------" + current_date_and_time + "-----------\n" + new_dialog
    redis_cli.set_story(story_id, story_data)

    # 返回缓存中的内容
    return story_data['world_record_txt'], story_data['dialog_record_txt']