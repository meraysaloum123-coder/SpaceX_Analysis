import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# 1) تحميل البيانات
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("spacex_cleaned_data.csv")
    return df

df = load_data()

# =========================
# 2) عنوان التطبيق
# =========================
st.title("🚀 SpaceX Launch Dashboard")
st.markdown("تحليل بيانات إطلاقات SpaceX وعلاقة المتغيرات بنجاح الهبوط")

# =========================
# 3) عرض البيانات
# =========================
if st.checkbox("عرض البيانات الخام"):
    st.write(df)

# =========================
# 4) إحصائيات عامة
# =========================
st.subheader("📊 الإحصائيات العامة")

total_launches = len(df)
success_rate = df["success"].mean() * 100

col1, col2 = st.columns(2)
col1.metric("عدد الإطلاقات", total_launches)
col2.metric("نسبة النجاح %", f"{success_rate:.2f}")

# =========================
# 5) توزيع النجاح
# =========================
st.subheader("📈 توزيع النجاح")

fig1 = px.pie(df, names="success", title="Success vs Failure")
st.plotly_chart(fig1)

# =========================
# 6) تأثير الوزن على النجاح
# =========================
st.subheader("⚖️ تأثير وزن الحمولة على النجاح")

fig2 = px.scatter(
    df,
    x="payload_mass",
    y="success",
    color="success",
    title="Payload vs Success"
)

st.plotly_chart(fig2)

# =========================
# 7) تحليل المواقع
# =========================
st.subheader("📍 تأثير موقع الإطلاق")

site_success = df.groupby("launch_site")["success"].mean().reset_index()

fig3 = px.bar(
    site_success,
    x="launch_site",
    y="success",
    title="Success Rate by Launch Site"
)

st.plotly_chart(fig3)

# =========================
# 8) فلترة تفاعلية
# =========================
st.subheader("🔍 فلترة البيانات")

site = st.selectbox("اختر موقع الإطلاق", df["launch_site"].unique())

filtered_df = df[df["launch_site"] == site]

st.write(filtered_df)

st.subheader("📊 نجاح هذا الموقع")

fig4 = px.histogram(filtered_df, x="success")
st.plotly_chart(fig4)   