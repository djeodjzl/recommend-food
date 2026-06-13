import streamlit as st
import random

st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍽️", layout="centered")

st.title("🍽️ 오늘 뭐 먹지?")
st.caption("기분, 음식 종류, 상황을 선택하면 딱 맞는 음식을 추천해드려요.")

st.divider()

# ── 음식 데이터베이스 ──────────────────────────────────────────
FOODS = [
    {"name": "김치찌개", "cuisine": "한식", "price": "6000~9000원", "fullness": "든든함", "mood": ["스트레스", "피곤함", "무난함"], "situation": ["혼밥", "배달"], "diet": ["매운 거 좋아요"], "min_price": 6000, "max_price": 9000, "fullness_level": 3},
    {"name": "된장찌개", "cuisine": "한식", "price": "6000~8000원", "fullness": "든든함", "mood": ["몸이 안 좋음", "피곤함", "무난함"], "situation": ["혼밥", "간단히"], "diet": ["없음"], "min_price": 6000, "max_price": 8000, "fullness_level": 3},
    {"name": "비빔밥", "cuisine": "한식", "price": "7000~10000원", "fullness": "보통", "mood": ["기분 좋음", "무난함", "신남"], "situation": ["혼밥", "간단히"], "diet": ["채식 선호"], "min_price": 7000, "max_price": 10000, "fullness_level": 2},
    {"name": "삼겹살", "cuisine": "한식", "price": "13000~20000원", "fullness": "매우 든든함", "mood": ["기분 좋음", "스트레스", "신남"], "situation": ["회식/단체", "데이트"], "diet": ["매운 거 좋아요", "없음"], "min_price": 13000, "max_price": 20000, "fullness_level": 4},
    {"name": "냉면", "cuisine": "한식", "price": "8000~12000원", "fullness": "보통", "mood": ["기분 좋음", "무난함"], "situation": ["혼밥", "데이트"], "diet": ["없음"], "min_price": 8000, "max_price": 12000, "fullness_level": 2},
    {"name": "순두부찌개", "cuisine": "한식", "price": "7000~9000원", "fullness": "든든함", "mood": ["몸이 안 좋음", "피곤함"], "situation": ["혼밥", "간단히"], "diet": ["채식 선호", "없음"], "min_price": 7000, "max_price": 9000, "fullness_level": 3},
    {"name": "불고기", "cuisine": "한식", "price": "10000~18000원", "fullness": "든든함", "mood": ["기분 좋음", "신남"], "situation": ["데이트", "회식/단체"], "diet": ["없음"], "min_price": 10000, "max_price": 18000, "fullness_level": 3},
    {"name": "잡채", "cuisine": "한식", "price": "8000~12000원", "fullness": "보통", "mood": ["기분 좋음", "무난함"], "situation": ["회식/단체", "데이트"], "diet": ["채식 선호"], "min_price": 8000, "max_price": 12000, "fullness_level": 2},

    {"name": "짜장면", "cuisine": "중식", "price": "5000~7000원", "fullness": "든든함", "mood": ["스트레스", "피곤함", "무난함"], "situation": ["혼밥", "배달"], "diet": ["없음"], "min_price": 5000, "max_price": 7000, "fullness_level": 3},
    {"name": "짬뽕", "cuisine": "중식", "price": "6000~9000원", "fullness": "든든함", "mood": ["스트레스", "피곤함"], "situation": ["혼밥", "배달"], "diet": ["매운 거 좋아요", "해산물 싫어요"], "min_price": 6000, "max_price": 9000, "fullness_level": 3},
    {"name": "탕수육", "cuisine": "중식", "price": "15000~25000원", "fullness": "매우 든든함", "mood": ["기분 좋음", "신남"], "situation": ["회식/단체", "배달"], "diet": ["달달한 거"], "min_price": 15000, "max_price": 25000, "fullness_level": 4},
    {"name": "마라탕", "cuisine": "중식", "price": "10000~15000원", "fullness": "든든함", "mood": ["스트레스", "신남"], "situation": ["혼밥", "데이트"], "diet": ["매운 거 좋아요"], "min_price": 10000, "max_price": 15000, "fullness_level": 3},

    {"name": "라멘", "cuisine": "일식", "price": "9000~14000원", "fullness": "든든함", "mood": ["피곤함", "무난함", "스트레스"], "situation": ["혼밥", "데이트"], "diet": ["없음"], "min_price": 9000, "max_price": 14000, "fullness_level": 3},
    {"name": "초밥", "cuisine": "일식", "price": "15000~30000원", "fullness": "보통", "mood": ["기분 좋음", "신남"], "situation": ["데이트", "회식/단체"], "diet": ["해산물 싫어요"], "min_price": 15000, "max_price": 30000, "fullness_level": 2},
    {"name": "돈카츠", "cuisine": "일식", "price": "9000~13000원", "fullness": "든든함", "mood": ["기분 좋음", "무난함"], "situation": ["혼밥", "간단히"], "diet": ["없음"], "min_price": 9000, "max_price": 13000, "fullness_level": 3},
    {"name": "우동", "cuisine": "일식", "price": "7000~10000원", "fullness": "보통", "mood": ["몸이 안 좋음", "피곤함", "무난함"], "situation": ["혼밥", "간단히"], "diet": ["없음"], "min_price": 7000, "max_price": 10000, "fullness_level": 2},

    {"name": "파스타", "cuisine": "양식", "price": "10000~18000원", "fullness": "보통", "mood": ["기분 좋음", "신남"], "situation": ["데이트", "혼밥"], "diet": ["채식 선호"], "min_price": 10000, "max_price": 18000, "fullness_level": 2},
    {"name": "스테이크", "cuisine": "양식", "price": "25000원 이상", "fullness": "매우 든든함", "mood": ["기분 좋음", "신남"], "situation": ["데이트", "회식/단체"], "diet": ["없음"], "min_price": 25000, "max_price": 99999, "fullness_level": 4},
    {"name": "피자", "cuisine": "양식", "price": "15000~25000원", "fullness": "든든함", "mood": ["기분 좋음", "스트레스", "신남"], "situation": ["배달", "회식/단체"], "diet": ["없음"], "min_price": 15000, "max_price": 25000, "fullness_level": 3},
    {"name": "버거", "cuisine": "양식", "price": "6000~12000원", "fullness": "보통", "mood": ["무난함", "신남"], "situation": ["혼밥", "간단히", "배달"], "diet": ["없음"], "min_price": 6000, "max_price": 12000, "fullness_level": 2},

    {"name": "떡볶이", "cuisine": "분식/패스트푸드", "price": "3000~6000원", "fullness": "가벼움", "mood": ["스트레스", "신남", "무난함"], "situation": ["혼밥", "간단히"], "diet": ["매운 거 좋아요", "달달한 거"], "min_price": 3000, "max_price": 6000, "fullness_level": 1},
    {"name": "순대국밥", "cuisine": "분식/패스트푸드", "price": "7000~9000원", "fullness": "매우 든든함", "mood": ["피곤함", "스트레스"], "situation": ["혼밥", "간단히"], "diet": ["없음"], "min_price": 7000, "max_price": 9000, "fullness_level": 4},
    {"name": "김밥", "cuisine": "분식/패스트푸드", "price": "3000~5000원", "fullness": "가벼움", "mood": ["무난함", "피곤함"], "situation": ["혼밥", "간단히"], "diet": ["채식 선호"], "min_price": 3000, "max_price": 5000, "fullness_level": 1},

    {"name": "쌀국수", "cuisine": "아시안", "price": "8000~12000원", "fullness": "보통", "mood": ["몸이 안 좋음", "무난함", "피곤함"], "situation": ["혼밥", "데이트"], "diet": ["없음"], "min_price": 8000, "max_price": 12000, "fullness_level": 2},
    {"name": "팟타이", "cuisine": "아시안", "price": "9000~13000원", "fullness": "보통", "mood": ["기분 좋음", "신남"], "situation": ["혼밥", "데이트"], "diet": ["달달한 거"], "min_price": 9000, "max_price": 13000, "fullness_level": 2},
    {"name": "커리", "cuisine": "아시안", "price": "9000~14000원", "fullness": "든든함", "mood": ["기분 좋음", "무난함"], "situation": ["혼밥", "데이트", "배달"], "diet": ["채식 선호", "매운 거 좋아요"], "min_price": 9000, "max_price": 14000, "fullness_level": 3},
]

EMOJI_MAP = {
    "김치찌개": "🍲", "된장찌개": "🥘", "비빔밥": "🍚", "삼겹살": "🥓", "냉면": "🍜",
    "순두부찌개": "🥣", "불고기": "🥩", "잡채": "🍝", "짜장면": "🍜", "짬뽕": "🍜",
    "탕수육": "🍖", "마라탕": "🌶️", "라멘": "🍜", "초밥": "🍣", "돈카츠": "🍱",
    "우동": "🍜", "파스타": "🍝", "스테이크": "🥩", "피자": "🍕", "버거": "🍔",
    "떡볶이": "🌶️", "순대국밥": "🍲", "김밥": "🍙", "쌀국수": "🍜", "팟타이": "🍜", "커리": "🍛",
}

REASON_MAP = {
    "김치찌개": "얼큰하고 따뜻해서 스트레스 해소에 딱이에요.",
    "된장찌개": "구수하고 건강한 맛으로 몸을 따뜻하게 해줘요.",
    "비빔밥": "영양 균형이 좋고 든든하게 한 끼 해결할 수 있어요.",
    "삼겹살": "기분 좋은 날 고기 구워 먹으면 최고죠!",
    "냉면": "시원하고 담백해서 깔끔하게 먹기 좋아요.",
    "순두부찌개": "부드럽고 따뜻해서 몸이 안 좋을 때 딱이에요.",
    "불고기": "달콤짭짤한 맛으로 누구나 좋아하는 메뉴예요.",
    "잡채": "부드럽고 달콤해서 여럿이 먹기 좋아요.",
    "짜장면": "스트레스 받을 때 한 그릇이면 기분이 풀려요.",
    "짬뽕": "칼칼한 국물이 속을 시원하게 해줘요.",
    "탕수육": "바삭하고 달콤해서 모임 자리에 인기 만점이에요.",
    "마라탕": "얼얼한 매운맛이 스트레스를 날려줘요.",
    "라멘": "진한 국물이 피곤한 몸을 녹여줘요.",
    "초밥": "신선한 재료로 특별한 날을 더 빛내줘요.",
    "돈카츠": "바삭한 튀김옷이 기분을 업시켜줘요.",
    "우동": "따뜻하고 부드러워 몸이 힘들 때 먹기 좋아요.",
    "파스타": "분위기 있는 식사로 데이트에 잘 어울려요.",
    "스테이크": "특별한 날 고급스러운 식사로 완벽해요.",
    "피자": "다 같이 나눠 먹기 좋고 배달도 편해요.",
    "버거": "간단하고 빠르게 한 끼 해결하기 딱이에요.",
    "떡볶이": "달콤 매콤해서 기분 전환에 최고예요.",
    "순대국밥": "든든하고 따뜻해서 피곤할 때 힘이 나요.",
    "김밥": "간편하게 먹을 수 있어서 바쁠 때 좋아요.",
    "쌀국수": "깔끔하고 담백해서 속이 편해요.",
    "팟타이": "달콤하고 고소한 맛이 입맛을 돋워요.",
    "커리": "향긋하고 깊은 맛이 특별한 한 끼를 만들어줘요.",
}

PRICE_RANGE = {
    "5000원 이하": (0, 5000),
    "5000~10000원": (5000, 10000),
    "10000~20000원": (10000, 20000),
    "20000원 이상": (20000, 99999),
    "상관없음": (0, 99999),
}

FULLNESS_LEVEL = {
    "가볍게": [1],
    "적당히": [2],
    "든든하게": [3],
    "최대한 많이": [4],
}

def radio_with_other(label, options, key):
    choice = st.radio(label, options + ["기타"], horizontal=True, key=key)
    if choice == "기타":
        custom = st.text_input("직접 입력해주세요", key=f"{key}_custom")
        return custom if custom else None
    return choice

mood = radio_with_other("지금 기분이 어때요?",
    ["기분 좋음", "피곤함", "스트레스", "몸이 안 좋음", "무난함", "신남"], "mood")
cuisine = radio_with_other("어떤 종류가 끌려요?",
    ["한식", "중식", "일식", "양식", "분식/패스트푸드", "아시안", "상관없음"], "cuisine")
situation = radio_with_other("어떤 상황인가요?",
    ["혼밥", "데이트", "회식/단체", "배달", "간단히", "배부르게"], "situation")
diet = radio_with_other("특별한 선호/제한이 있나요?",
    ["없음", "채식 선호", "매운 거 좋아요", "짠 거 싫어요", "달달한 거", "해산물 싫어요"], "diet")
price = radio_with_other("예산은 어느 정도예요?",
    ["5000원 이하", "5000~10000원", "10000~20000원", "20000원 이상", "상관없음"], "price")
fullness = radio_with_other("얼마나 배부르게 먹고 싶어요?",
    ["가볍게", "적당히", "든든하게", "최대한 많이"], "fullness")

st.divider()

if st.button("음식 추천받기", use_container_width=True, type="primary"):
    if not all([mood, cuisine, situation, diet, price, fullness]):
        st.warning("모든 항목을 입력해주세요!")
    else:
        candidates = FOODS.copy()

        # 가격 필터
        if price in PRICE_RANGE:
            pmin, pmax = PRICE_RANGE[price]
            candidates = [f for f in candidates if f["min_price"] <= pmax and f["max_price"] >= pmin]

        # 포만도 필터
        if fullness in FULLNESS_LEVEL:
            levels = FULLNESS_LEVEL[fullness]
            candidates = [f for f in candidates if f["fullness_level"] in levels]

        # 음식 종류 필터
        if cuisine != "상관없음" and cuisine not in ["기타"]:
            filtered = [f for f in candidates if f["cuisine"] == cuisine]
            if filtered:
                candidates = filtered

        # 점수 계산
        def score(food):
            s = 0
            if mood in food["mood"]:
                s += 3
            if situation in food["situation"]:
                s += 2
            if diet != "없음" and diet in food["diet"]:
                s += 2
            return s

        candidates.sort(key=score, reverse=True)

        if len(candidates) == 0:
            st.warning("조건에 맞는 음식이 없어요. 조건을 조금 바꿔보세요!")
        else:
            top = candidates[:min(6, len(candidates))]
            picks = random.sample(top, min(3, len(top)))

            st.success("오늘의 추천 메뉴예요!")
            for food in picks:
                with st.container(border=True):
                    emoji = EMOJI_MAP.get(food["name"], "🍽️")
                    st.subheader(f"{emoji} {food['name']}")
                    col1, col2 = st.columns(2)
                    col1.metric("가격", food["price"])
                    col2.metric("포만도", food["fullness"])
                    st.write(REASON_MAP.get(food["name"], "맛있는 메뉴예요!"))
