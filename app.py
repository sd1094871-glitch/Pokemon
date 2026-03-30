import streamlit as st

# 页面配置
st.set_page_config(page_title="宝可梦评级 ERP v1.3", layout="wide")

st.title("🛡️ 宝可梦评级 ERP (v1.3) - 资金杠杆分析")
st.caption("针对 2026 年 7 月新弹调价及能源附加费优化版")

# --- 侧边栏输入 ---
st.sidebar.header("核心参数输入")
mode = st.sidebar.selectbox("采购模式", ["1-线下现金 (便宜)", "2-线上分期 (杠杆)"])
total_count = st.sidebar.number_input("总送评张数", value=238, step=1)
raw_cost_base = st.sidebar.number_input("基础裸卡单价 (元)", value=30.0, step=1.0)
cycle_months = st.sidebar.slider("预期回款周期 (月)", 1, 12, 6)

# --- 逻辑计算 ---
price_gap = 0.10 if "2-" in mode else 0.00
interest_monthly = 58 / 41000 if "2-" in mode else 0

# 2026年7月调价修正 (180->200)
new_set_markup = 1.11 
actual_card_cost = raw_cost_base * (1 + price_gap) * new_set_markup

# 利息与评级费
total_interest_cost = (actual_card_cost * total_count) * interest_monthly * cycle_months
cgc_fee = 65
psa_fee = 190
# 假设 61 张转 PSA (你可以根据实际情况调整这个比例)
cash_needed_for_fees = (total_count * cgc_fee) + (61 * psa_fee) 

total_investment = (actual_card_cost * total_count) + cash_needed_for_fees + total_interest_cost

# --- 网页结果展示 ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("实际单张采购成本", f"{actual_card_cost:.2f} 元")
with col2:
    st.metric("现金流压力 (评级费)", f"¥{cash_needed_for_fees:,.2f}")
with col3:
    st.metric("项目总投入", f"¥{total_investment:,.2f}")

st.divider()

# 策略分析
st.subheader("💡 操盘策略建议")
if "2-" in mode and cycle_months >= 6:
    st.success("建议：PSA长线项目使用分期。每月 58 元的代价保住了 4.1 万现金流，这是防爆仓的核心。")
elif "1-" in mode:
    st.info("建议：短线项目坚持线下现金。11% 的涨价压力下，只有省下分期差价才是你的纯利润。")

if cash_needed_for_fees > 41000:
    st.error(f"⚠️ 警告：现金流赤字！评级费缺口为 ¥{cash_needed_for_fees - 41000:,.2f}。请减少 PSA 送评比例。")
