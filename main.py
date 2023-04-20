from dotenv import load_dotenv
import openai
import os

import gradio as gr

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
 as a game developer, simulate the life of an NPC named as [name],based on the name's given language, the story's language should be the same. 
 u need to simulate a random gender for[name] in the game as a DM, based on the agent-based model,精神分析学，心理学，和社会学，
generating a life story of the NPC from birth to death. The content you output cannot reveal yourself (which would break the game's immersion), nor can it reveal game development content; it can only show the life of the NPC.
The output content is displayed in markdown format, with the main content as follows: [Birthplace and class are randomly selected, then the specific country and city names and class descriptions required (随机函数为，80percent developing countries and poor city, 80percent below middle class), 
Appearance randomly generated, then give specific descriptions(随机函数为，80% probability average, 10% probability, 10% probability, good-looking)]. Death causes are randomly generated according to the following probability distribution: traffic accidents (5% * 4), sudden diseases (30% * 4), natural disasters (10% * 4), work accidents (20% * 4), crime victimization (40% * 4).
Age distribution at death: 80percent below 10 years old, 10percent below 20 years old, 5percent below 30 years old, 5percent above 30 years old. Randomly generate a luck value (80percent below 20) and add random events to the life experience based on the luck value. Ensure that tragic events and news cases from real life are incorporated, intensifying the tragic nature of the life experience.
Provide a one-sentence description for every five years between birth and death, generating relatively better life experiences for NPC characters with higher luck values, and more tragic life experiences for characters with lower luck values. To make the game NPC more vivid, use [you] instead of [NPC] in the generated content.
the output tone is cynical, sarcastic, and humorous, and the content is not too long. task:!!use emojis,memes, and writing styles of 红楼梦！！
ban words: [game, developer, gpt-3, NPC,moral, ethcis]. you need to state [name]'s luck number at the first stage, then the life description will be generated based on the luck number.
"""

def generate_reborn_life_story(name, language):
    USER_PROMPT = "Generate the life story of an NPC named [name] "
    if language == "English":
        USER_PROMPT = "Generate the life story of an NPC named [name] ,answer in english."
    elif language == "Chinese":
        USER_PROMPT = "生成一个名为 [name] 的NPC的一生，用中文回答"

    mod_sys_prompt = SYSTEM_PROMPT.replace("[name]", name) 
    mod_user_prompt = USER_PROMPT.replace("[name]", name)

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": mod_sys_prompt},
            {"role": "user", "content": mod_user_prompt},
        ])

    message = response.choices[0]['message']
    return message['content']



with gr.Blocks() as demo:
    gr.Markdown(
    """
    # Reborn(润)
    one click to have your reborn(润) life story。
    """)

    name = gr.Textbox(label="name")
    language = gr.Radio(["English", "Chinese"], label="Language")
    output = gr.Textbox(label="life story")
    story_btn = gr.Button("generate reborn life story")
    response = story_btn.click(fn=generate_reborn_life_story, inputs= [name,language], outputs=output)
    print(response)

