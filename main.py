import streamlit as st
import anthropic
import json
import re

st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍽️", layout="centered")

st.title("🍽️ 오늘 뭐 먹지?")
st.caption("기분, 음식 종류, 상황을 선택하면 Claude AI가 딱 맞는 음식을 추천해드려요.")

st.divider()

def remove_emoji(text):
    return re.sub(r'[^\w\s,.!?/]', '', text).strip()

def radio_with_other(label, options, key):
    choice = st.radio(label, options + ["기타"], horizontal=True, key=key)
    if choice == "기타":
        custom = st.text_input("직접 입력해주세요", key=f"{key}_custom")
        return custom if custom else None
    return choice

mood = radio_with_other(
    "지금 기분이 어때요?",
    ["기분 좋음", "피곤함", "스트레스", "몸이 안 좋음", "무난함", "신남"],
    "mood",
)

cuisine = radio_with_other(
    "어떤 종류가 끌려요?",
    ["한식", "중식", "일식", "양식", "분식/패스트푸드", "아시안", "상관없음"],
    "cuisine",
)

situation = radio_with_other(
    "어떤 상황인가요?",
    ["혼밥", "데이트", "회식/단체", "배달", "간단히", "배부르게"],
    "situation",
)

diet = radio_with_other(
    "특별한 선호/제한이 있나요?",
    ["없음", "채식 선호", "매운 거 좋아요", "짠 거 싫어요", "달달한 거", "해산물 싫어요"],
    "diet",
)

price = radio_with_other(
    "예산은 어느 정도예요?",
    ["5000원 이하", "5000~10000원", "10000~20000원", "20000원 이상", "상관없음"],
    "price",
)

fullness = radio_with_other(
    "얼마나 배부르게 먹고 싶어요?",
    ["가볍게", "적당히", "든든하게", "최대한 많이"],
    "fullness",
)

st.divider()

if st.button("음식 추천받기", use_container_width=True, type="primary"):
    if not all([mood, cuisine, situation, diet, price, fullness]):
        st.warning("모든 항목을 입력해주세요!")
    else:
        prompt = (
            "You are a Korean food recommendation expert. "
            "Recommend 3 foods based on the conditions below. "
            "Respond ONLY in JSON format with no other text.\n\n"
            f"Mood: {remove_emoji(mood)}\n"
            f"Cuisine: {remove_emoji(cuisine)}\n"
            f"Situation: {remove_emoji(situation)}\n"
            f"Dietary: {remove_emoji(diet)}\n"
            f"Budget: {remove_emoji(price)}\n"
            f"Fullness: {remove_emoji(fullness)}\n\n"
            'Respond in this exact JSON:\n'
            '{"recommendations": ['
            '{"name": "food name in Korean", "emoji": "1 emoji", "reason": "1-2 sentences in Korean", "price": "approximate price range in Korean won", "fullness": "fullness level in Korean (e.g. 가벼움/보통/든든함)"},'
            '{"name": "food name in Korean", "emoji": "1 emoji", "reason": "1-2 sentences in Korean", "price": "approximate price range in Korean won", "fullness": "fullness level in Korean"},'
            '{"name": "food name in Korean", "emoji": "1 emoji", "reason": "1-2 sentences in Korean", "price": "approximate price range in Korean won", "fullness": "fullness level in Korean"}'
            '], "summary": "one friendly line in Korean"}'
        )

        with st.spinner("Claude가 딱 맞는 음식을 고르고 있어요..."):
            try:
                client = anthropic.Anthropic()
                message = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}],
                )
                raw = message.content[0].text.strip().replace("```json", "").replace("```", "").strip()
                data = json.loads(raw)

                st.success(f"{data.get('summary', '')}")
                for item in data.get("recommendations", []):
                    with st.container(border=True):
                        st.subheader(f"{item.get('emoji', '')} {item.get('name', '')}")
                        col1, col2 = st.columns(2)
                        col1.metric("가격", item.get("price", ""))
                        col2.metric("포만도", item.get("fullness", ""))
                        st.write(item.get("reason", ""))

            except Exception as e:
                st.error(f"오류가 발생했어요: {e}")
