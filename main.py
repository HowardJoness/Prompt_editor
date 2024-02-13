import streamlit as st
import tiktoken
import json
from openai import OpenAI
import openai

API_KEY = "YOUR_API_KEY"

# 设置设置tiktoken计算的encoding
encoding = tiktoken.get_encoding("cl100k_base")

# 计算token数量
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    '''返回token信息'''
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# 设置title
st.title("PROMPT编辑器")
modelchoice = ["gpt-3.5-turbo", "gpt-3.5-turbo-0125", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-1106", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613", "gpt-4", "gpt-4-0125-preview", "gpt-4-0314", "gpt-4-0613", "gpt-4-1106-preview", "gpt-4-1106-vision-preview", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-0613", "gpt-4-turbo-preview", "gpt-4-vision-preview"]
modelprice = {
    "gpt-3.5-turbo": {"official_ask_price": 0.0000015, "official_answer_price": 0.000002},
    "gpt-3.5-turbo-0125": {"official_ask_price": 0.0000005, "official_answer_price": 0.0000015},
    "gpt-3.5-turbo-0301": {"official_ask_price": 0.0000015, "official_answer_price": 0.000002},
    "gpt-3.5-turbo-0613": {"official_ask_price": 0.0000015, "official_answer_price": 0.000002},
    "gpt-3.5-turbo-1106": {"official_ask_price": 0.000001, "official_answer_price": 0.000002},
    "gpt-3.5-turbo-16k": {"official_ask_price": 0.000003, "official_answer_price": 0.000004},
    "gpt-3.5-turbo-16k-0613": {"official_ask_price": 0.000003, "official_answer_price": 0.000004},
    "gpt-4": {"official_ask_price": 0.0003, "official_answer_price": 0.00006},
    "gpt-4-0125-preview": {"official_ask_price": 0.00001, "official_answer_price": 0.00003},
    "gpt-4-0314": {"official_ask_price": 0.00003, "official_answer_price": 0.00006},
    "gpt-4-0613": {"official_ask_price": 0.00003, "official_answer_price": 0.00006},
    "gpt-4-1106-preview": {"official_ask_price": 0.00001, "official_answer_price": 0.00003},
    "gpt-4-1106-vision-preview": {"official_ask_price": 0.00001, "official_answer_price": 0.00003},
    "gpt-4-32k": {"official_ask_price": 0.00006, "official_answer_price": 0.00012},
    "gpt-4-32k-0314": {"official_ask_price": 0.00006, "official_answer_price": 0.00012},
    "gpt-4-32k-0613": {"official_ask_price": 0.00006, "official_answer_price": 0.00012},
    "gpt-4-turbo-preview": {"official_ask_price": 0.00001, "official_answer_price": 0.00003},
    "gpt-4-vision-preview": {"official_ask_price": 0.00001, "official_answer_price": 0.00003}
}
modelchoices = st.selectbox("使用的模型", modelchoice)
# 编辑文本用的富文本框
text = st.text_area("请键入prompt", "你是一个智能AI助手，会解答由我提出的任何问题", height=300)

# 获取文本相关信息
total_characters = len(text)
total_chinese_characters = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
total_tokens = num_tokens_from_string(text, modelchoices)
tempprice = modelprice[modelchoices]['official_ask_price']
cost = total_tokens * tempprice
costr = cost*7.19

# 显示文本相关信息
st.write(f"总字符数: {total_characters}")
st.write(f"总汉字数: {total_chinese_characters}")
st.write(f"总token数: {total_tokens}")
st.write(f"耗费资金: ${cost:.4f} ￥{costr:.4f}")

# 对话框用于输入对话
st.subheader("对话测试")
say = st.chat_input("啵哔啵哔？")
if say:
    # 显示用户输入
    umessage = st.chat_message("user")
    umessage.write(say)
    client = OpenAI(
        api_key=API_KEY,
    )
    try:
        # 发起请求
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": text,
                },{
                    "role": "user",
                    "content": say,
                }

            ],
            model=modelchoices,
        )
        # 显示回答
        amessage = st.chat_message("assistant")
        r = json.loads(chat_completion.json())['choices'][0]['message']['content']
        amessage.write(r)

    except openai.PermissionDeniedError as err:
        # 捕捉到openai.PermissionDeniedError错误
        error_message = err.message
        amessage = st.chat_message("assistant")
        amessage.write(f'捕捉到openai.PermissionDeniedError异常：{error_message}')
