import streamlit as st
import openai
import os
import numpy as np
import pandas as pd
import datetime as dt
import altair as alt

os.environ["OPENAI_API_KEY"] = "sk-proj-YVT5pzAi8XrVv8ZNwzLGT3BlbkFJ6MowIkREhrU6zphQ6DJO"
client = openai.OpenAI()


st.title('PAO Beauty Tone')
#Toneは情筋を鍛えることを示唆し、健康的で美しい表情を目指すことを表現している


#ここまで
import datetime as dt

st.write('#### 日付')

col1, col2, col3 = st.columns(3)

with col1:
    year = st.number_input('年', min_value=2022, step=1)
with col2:
    month = st.number_input('月', min_value=1, max_value=12, step=1)
with col3:
    day = st.number_input('日', min_value=1, max_value=31, step=1)

date = None
weekday = None

if year != '' and month != '' and day != '':
    date = dt.date(year, month, day)
    weekday = date.strftime('%a')
    

st.write('#### 憧れの人を選んでください')
person = st.selectbox('憧れの人を選んでください',["Marina Takewaki","xxxxx","xxxxx"])

st.write('#### Paoの活動')

if date is not None:
    weight = st.selectbox("重りを選択してください",["28g","23g","18g"])
    time = st.number_input('運動時間を入力してください(分)', min_value=1, max_value=10, step=1)

    if st.button('データを登録する'):
        _df = {
            '日付': date,
            '曜日': weekday, 
            '重り': weight, 
            '運動時間(分)': time
        }
        data = pd.DataFrame([_df])
        df = pd.concat([df, data])
        df.to_excel('Pao管理.xlsx', index=False)
        st.write('完了しました。画面を更新(Ctr+r)してください')

#ここから

df = pd.read_excel('Pao管理.xlsx')
df.columns = ['日付', '曜日', '重り', '運動時間(分)']
st.write('#### 直近5日間のデータ')
st.dataframe(df.tail())
#st.dataframe(df.tail())は、StreamlitでDataFrameを表示するためのコマンド。このコマンドは、DataFrameの末尾の行を表示

ymin_1 = 0.5
ymax_1 = 5

ymin_2 = 18
ymax_2 = 28

base = alt.Chart(df).encode(
    alt.X('日付:T', axis=alt.Axis(title=None))
)
line1 = base.mark_line(opacity=0.3, color='#57A44C').encode(
    alt.Y('運動時間(分)',
          axis=alt.Axis(title='運動の記録', titleColor='#57A44C'),
          scale=alt.Scale(domain=[ymin_1, ymax_1]))
)

line2 = base.mark_line(opacity=0.3, color='#57A44C').encode(
    alt.Y('重り',
          axis=alt.Axis(title='重さ', titleColor='#57A44C'),
          scale=alt.Scale(domain=[ymin_2, ymax_2]))
)

chart = alt.layer(line1, line2).resolve_scale(
    y='independent'
)
st.altair_chart(chart, use_container_width=True)



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

