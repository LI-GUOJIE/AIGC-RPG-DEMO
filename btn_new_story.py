from chatbot import chatbot
from datetime import datetime
import redis_cli

# 加载世界引擎初始模板，并初始化会话
def new_story(player_template_name):

    # 检查模板名是否为空
    if len(player_template_name) < 1:
        return "", "模板ID为空：" + player_template_name, "模板ID为空：" + player_template_name, \
            "", "模板ID为空：" + player_template_name, "模板ID为空：" + player_template_name, \
            "", "模板ID为空：" + player_template_name, "模板ID为空：" + player_template_name, \
            "", "模板ID为空：" + player_template_name, "模板ID为空：" + player_template_name

    # 获取模板
    temp_data = redis_cli.get_template(player_template_name)
    if temp_data is None:
        return "", "模板不存在：" + player_template_name, "模板不存在：" + player_template_name, \
            "", "模板不存在：" + player_template_name, "模板不存在：" + player_template_name, \
            "", "模板不存在：" + player_template_name, "模板不存在：" + player_template_name, \
            "", "模板不存在：" + player_template_name, "模板不存在：" + player_template_name

    # 获取新的故事ID
    story_id = redis_cli.get_new_story_id(player_template_name)

    # 初始化故事
    story_data = redis_cli.get_story(story_id)
    if story_data is not None:
        return story_id, "故事ID异常", "故事ID异常"
    
    story_data = {
        "template_id": player_template_name,  # 模板ID
        'world_record_txt': '',               # 世界记录
        'dialog_record_txt': '',              # 对话记录
        'conversation': [],                   # 和AI模型的对话 list[dict]
    }
    redis_cli.set_story(story_id, story_data)

    # 初始化世界状态
    current_date_and_time = str(datetime.now())
    worldRecordInit = "------------" + current_date_and_time + "-----------\n"
    worldRecordInit += chatbot.ask(story_id, "system", temp_data['world_engine_init_template'])

    # 初始对话
    dialogRecordInit = "------------" + current_date_and_time + "-----------\n"
    dialogRecordInit += chatbot.ask(story_id, "system", temp_data['dialog_engine_init_template'] )

    # 更新记录
    story_data = redis_cli.get_story(story_id)
    story_data['world_record_txt'] = worldRecordInit
    story_data['dialog_record_txt'] = dialogRecordInit
    redis_cli.set_story(story_id, story_data)
    
    print("create story_id: " + str(story_id))
    return story_id, worldRecordInit, dialogRecordInit