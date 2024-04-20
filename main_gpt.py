import streamlit as st
import pandas as pd
import openai
import os


os.environ["OPENAI_API_KEY"] = "sk-proj-YVT5pzAi8XrVv8ZNwzLGT3BlbkFJ6MowIkREhrU6zphQ6DJO"
client = openai.OpenAI()



def run_gpt(content_text_to_gpt, content_kind_of_to_gpt):
    request_to_gpt = (
        content_text_to_gpt
        + "上記の内容はpaoという小顔になるための健康器具のトレーニング記録です。これについて、アドバイスを作成してください。"
        + "アドバイスは今日の頑張りをたたえつつ、結果のレビュー、今後のモチベーションアップのための提案の順番で出力してください。"
        + "内容は500文字程度で出力してください。"
        + "また、文章は"
        + content_kind_of_to_gpt
        + "がアドバイスしているような語り口調にしてください。"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": request_to_gpt}],
    )
    output_content = response.choices[0].message.content.strip()
    return output_content

def main():
    st.title('advice')

    df = pd.read_excel('Pao管理.xlsx')
    content_text_to_gpt = df.to_string()

    content_kind_of_to_gpt = st.selectbox('誰にadvice欲しい？:', ["Marina Takewaki","ホリエモン","さかなくん"])

    if st.button('get advice'):
        output_content_text = run_gpt(content_text_to_gpt, content_kind_of_to_gpt)
        st.write('advice:', output_content_text)

if __name__ == "__main__":
    main()

