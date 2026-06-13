import streamlit as st
import httpx
import json

st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍽️", layout="centered")

st.title("🍽️ 오늘 뭐 먹지?")
st.caption("기분, 음식 종류, 상황을 선택하면 Claude AI가 딱 맞는 음식을 추천해드려요.")

st.divider()

# 한글 → 영어 매핑
MOOD_MAP = {"기분 좋음":"good","피곤함":"tired","스트레스":"stressed","몸이 안 좋음":"sick","무난함":"neutral","신남":"excited","기타":"other"}
CUISINE_MAP = {"한식":"Korean","중식":"Chinese","일식":"Japanese","양식":"Western","분식/패스트푸드":"street food","아시안":"Asian","상관없음":"any","기타":"other"}
SITUATION_MAP = {"혼밥":"eating alone","데이트":"date","회식/단체":"group","배달":"delivery","간단히":"quick meal","배부르게":"filling meal","기타":"other"}
DIET_MAP = {"없음":"none","채식 선호":"vegetarian","매운 거 좋아요":"spicy","짠 거 싫어요":"low sodium","달달한 거":"sweet","해산물 싫어요":"no seafood","기타":"other"}
PRICE_MAP = {"5000원 이하":"under 5000 KRW","5000~10000원":"5000-10000 KRW","10000~20000원":"10000-20000 KRW","20000원 이상":"over 20000 KRW","상관없음":"any","기타":"other"}
FULLNESS_MAP = {"가볍게":"light","적당히":"moderate","든든하게":"filling","최대한 많이":"very filling","기타":"other"}

def radio_with_other(label, options, key):
    choice = st.radio(label, options + ["기타"], horizontal=True, key=key)
    if choice == "기타":
        custom = st.text_input("직접 입력해주세요", key=f"{key}_custom")
        return custom if custom else None
    return choice

mood = radio_with_other("지금 기분이 어때요?", list(MOOD_MAP.keys())[:-1], "mood")
cuisine = radio_with_other("어떤 종류가 끌려요?", list(CUISINE_MAP.keys())[:-1], "cuisine")
situation = radio_with_other("어떤 상황인가요?", list(SITUATION_MAP.keys())[:-1], "situation")
diet = radio_with_other("특별한 선호/제한이 있나요?", list(DIET_MAP.keys())[:-1], "diet")
price = radio_with_other("예산은 어느 정도예요?", list(PRICE_MAP.keys())[:-1], "price")
fullness = radio_with_other("얼마나 배부르게 먹고 싶어요?", list(FULLNESS_MAP.keys())[:-1], "fullness")

st.divider()

if st.button("음식 추천받기", use_container_width=True, type="primary"):
    if not all([mood, cuisine, situation, diet, price, fullness]):
        st.warning("모든 항목을 입력해주세요!")
    else:
        mood_en = MOOD_MAP.get(mood, mood)
        cuisine_en = CUISINE_MAP.get(cuisine, cuisine)
        situation_en = SITUATION_MAP.get(situation, situation)
        diet_en = DIET_MAP.get(diet, diet)
        price_en = PRICE_MAP.get(price, price)
        fullness_en = FULLNESS_MAP.get(fullness, fullness)

        prompt = (
            "You are a Korean food recommendation expert. "
            "Recommend 3 Korean foods and respond ONLY in JSON.\n"
            "mood: " + mood_en + "\n"
            "cuisine: " + cuisine_en + "\n"
            "situation: " + situation_en + "\n"
            "dietary: " + diet_en + "\n"
            "budget: " + price_en + "\n"
            "fullness: " + fullness_en + "\n\n"
            'JSON format: {"recommendations": ['
            '{"name": "Korean food name in Korean", "emoji": "1 emoji", "reason": "in Korean", "price": "price in Korean", "fullness": "level in Korean"},'
            '{"name": "Korean food name in Korean", "emoji": "1 emoji", "reason": "in Korean", "price": "price in Korean", "fullness": "level in Korean"},'
            '{"name": "Korean food name in Korean", "emoji": "1 emoji", "reason": "in Korean", "price": "price in Korean", "fullness": "level in Korean"}'
            '], "summary": "in Korean"}'
        )

        with st.spinner("Claude가 딱 맞는 음식을 고르고 있어요..."):
            try:
                api_key = st.secrets["ANTHROPIC_API_KEY"]
                payload = {
                    "model": "claude-sonnet-4-6",
                    "max_tokens": 1000,
                    "messages": [{"role": "user", "content": prompt}]
                }
                headers = {
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                }
                response = httpx.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=payload,
                    timeout=30,
                )
                result = response.json()
                raw = result["content"][0]["text"].strip().replace("```json", "").replace("```", "").strip()
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
                st.error(f"오류: {str(e)}")
