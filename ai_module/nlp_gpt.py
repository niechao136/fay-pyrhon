from revChatGPT.V3 import Chatbot
from openai import OpenAI
from utils import config_util as cfg
import time 

count = 0
def question(cont):
    global count
    try:
        client = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            api_key=cfg.key_chatgpt_api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        completion = client.chat.completions.create(
            # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            model="qwen-max",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": cont},
            ],
            # Qwen3模型通过enable_thinking参数控制思考过程（开源版默认True，商业版默认False）
            # 使用Qwen3开源版模型时，若未启用流式输出，请将下行取消注释，否则会报错
            # extra_body={"enable_thinking": False},
        )
        # 提取最终的返回内容
        response_content = completion.choices[0].message.content
        count = 0
        return response_content
    except Exception as e:
        count += 1
        if count < 3:
            time.sleep(15)
            return question(cont)
        return 'gpt当前繁忙，请稍后重试' + e
