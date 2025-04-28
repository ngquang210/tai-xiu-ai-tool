import streamlit as st
import collections

st.set_page_config(page_title="Tool Tài Xỉu Bắt Cầu AI", layout="centered")

st.title("🎲 Tool Tài Xỉu Bắt Theo Cầu (AI Phân Tích)")
st.markdown("Nhập kết quả gần nhất (VD: `TXTTXXT...`). Dự đoán xác suất ra Tài/Xỉu tiếp theo.")

def predict_tai_xiu(history, max_pattern_len=4):
    history = history.strip().upper()
    if not all(c in "TX" for c in history):
        return {"T": 50.0, "X": 50.0}  # Nhập sai định dạng

    scores = {"T": 0, "X": 0}
    total_matches = 0

    for pattern_len in range(2, max_pattern_len + 1):
        if len(history) < pattern_len:
            continue
        pattern = history[-pattern_len:]
        matches = []

        for i in range(len(history) - pattern_len):
            if history[i:i+pattern_len] == pattern:
                if i + pattern_len < len(history):
                    next_char = history[i + pattern_len]
                    matches.append(next_char)

        if matches:
            counter = collections.Counter(matches)
            total = sum(counter.values())
            scores["T"] += (counter.get("T", 0) / total)
            scores["X"] += (counter.get("X", 0) / total)
            total_matches += 1

    if total_matches == 0:
        return {"T": 50.0, "X": 50.0}

    percent_t = round((scores["T"] / total_matches) * 100, 2)
    percent_x = round((scores["X"] / total_matches) * 100, 2)

    return {"T": percent_t, "X": percent_x}

# Giao diện nhập liệu
user_input = st.text_input("Nhập chuỗi Tài/Xỉu (T hoặc X):", "")

if user_input:
    result = predict_tai_xiu(user_input)
    st.subheader("📊 Kết quả dự đoán:")
    st.success(f"✅ Xác suất ra **Tài (T)**: `{result['T']}%`")
    st.success(f"✅ Xác suất ra **Xỉu (X)**: `{result['X']}%`")

    if result['T'] > result['X']:
        st.markdown("👉 Gợi ý: **TÀI** có khả năng cao hơn!")
    elif result['X'] > result['T']:
        st.markdown("👉 Gợi ý: **XỈU** có khả năng cao hơn!")
    else:
        st.markdown("👉 Không có cầu rõ ràng, tỉ lệ 50/50.")

