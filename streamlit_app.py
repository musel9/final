import streamlit as st
import pandas as pd
from datetime import time, datetime
import os
import pytz

# Set timezone (e.g., Riyadh)
TIMEZONE = pytz.timezone("Asia/Riyadh")

# Authentication dictionary
AUTH_USERS = {
    "Muse": "!Muse!",
    "Mohammed": "!Mohammed!",
    "Duha": "!Duha!",
    "Ziyad": "!Ziyad!",
    "Rawan": "!Rawan!",
    "Fahad": "!Fahad!",
}

# List of energy types in Arabic
type_of_energy = [
    "الطاقة", "الطاقة النظيفة", "الطاقة الشمسية", "الطاقة الرياحية", "الطاقة الكهربائية",
    "الطاقة النووية", "الطاقة الحرارية الأرضية", "الطاقة المائية",
    "الطاقة الكهروضوئية", "الطاقة الحيوية", "الطاقة الهيدروجينية",
    "الطاقة المدية", "الطاقة الحرارية", "الطاقة الكيميائية",
    "الطاقة الشمسية المركزة", "الطاقة المتجددة", "الطاقة غير المتجددة"
]

# Direction styling for Arabic
st.markdown("""
    <style>
    body { direction: rtl; text-align: right; }
    </style>
    """, unsafe_allow_html=True
)

# Authentication logic
def login():
    st.title("تسجيل دخول")
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        if username in AUTH_USERS and AUTH_USERS[username] == password:
            st.session_state["logged_in"] = True
            st.success("تم تسجيل الدخول بنجاح!")
        else:
            st.error("اسم المستخدم أو كلمة المرور غير صحيحة")

def logout():
    st.session_state["logged_in"] = False
    st.success("تم تسجيل الخروج")

# Load CSV data
def load_data(file_name, columns):
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        return pd.DataFrame(columns=columns)

# Save data to CSV
def save_data(df, file_name):
    df.to_csv(file_name, index=False)

# Check login state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    if st.button("تسجيل خروج"):
        logout()

    tabs = st.tabs(["رصد الأخبار", "تواصل إجتماعي"])

    def get_selected_time(key_prefix):
        col1, col2 = st.columns(2)
        with col1:
            hour = st.selectbox("الساعة", list(range(1, 25)), index=11, key=f"{key_prefix}_hour")
        with col2:
            minute = st.selectbox("الدقيقة", list(range(0, 60)), index=0, key=f"{key_prefix}_minute")
        return time(hour=hour, minute=minute)

    NEWS_CSV = "news_data.csv"
    TWITTER_CSV = "twitter_news_data.csv"

    with tabs[0]:
        st.session_state["news_data"] = load_data(NEWS_CSV, ["التاريخ", "الوقت", "نوع الخبر", "الخبر الرئيسي", "التصنيف", "المقدمة", "الرابط"])

        with st.form("news_form", clear_on_submit=True):
            col_left, col_right = st.columns([2, 1])
            with col_left:
                news_date = st.date_input("التاريخ")
                time_choice = st.selectbox("التوقيت", ["الآن", "اختر"], key="news_time_choice")
                if time_choice == 'الآن':
                    current_time = datetime.now(TIMEZONE)
                    news_time = time(hour=current_time.hour, minute=current_time.minute, second=current_time.second)
                else:
                    news_time = get_selected_time(key_prefix="news")
                
                st.write(f"الوقت المحدد: {news_time.strftime('%I:%M:%S %p')}")
                news_type = st.selectbox('نوع الخبر', ['خبر', 'مرئي', 'مقال'])
                news_main = st.text_input("الخبر الرئيسي")

            with col_right:
                news_class = st.selectbox('التصنيف', type_of_energy)
                news_intro = st.text_area("المقدمة")
                news_url = st.text_area("الرابط")

            submit_button = st.form_submit_button(label="إرسال الخبر")

        if submit_button:
            new_entry = pd.DataFrame({
                "التاريخ": [news_date],
                "الوقت": [news_time],
                "نوع الخبر": [news_type],
                "الخبر الرئيسي": [news_main],
                "التصنيف": [news_class],
                "المقدمة": [news_intro],
                "الرابط": [news_url]
            })
            st.session_state["news_data"] = pd.concat([st.session_state["news_data"], new_entry], ignore_index=True)
            save_data(st.session_state["news_data"], NEWS_CSV)
            st.success("تم إرسال الخبر بنجاح!")

        if not st.session_state["news_data"].empty:
            st.subheader("الأخبار العامة")
            edited_df = st.data_editor(st.session_state["news_data"])
            st.session_state["news_data"] = edited_df
            save_data(edited_df, NEWS_CSV)

    with tabs[1]:
        st.session_state["twitter_news_data"] = load_data(TWITTER_CSV, ["المنصة", "التاريخ", "الوقت", "المنطقة", "التصنيف", "المحتوى", "التقييم", "الرابط"])

        with st.form("social_media_form", clear_on_submit=True):
            col_right, col_left = st.columns(2)
            with col_right:
                social_media = st.selectbox('المنصة', ['Twitter X', 'YouTube', 'TikTok', 'Snapchat', 'Instagram', 'Facebook', 'Linkedin'])
                social_date = st.date_input("التاريخ", key="social_date")
                social_time_choice = st.selectbox("التوقيت", ["الآن", "اختر"], key="social_time_choice")
                if social_time_choice == 'الآن':
                    current_time_2 = datetime.now(TIMEZONE)
                    social_time = time(hour=current_time_2.hour, minute=current_time_2.minute, second=current_time_2.second)
                else:
                    social_time = get_selected_time(key_prefix="tweet")
                st.write(f"الوقت المحدد: {social_time.strftime('%I:%M:%S %p')}")  
                social_zone = st.selectbox("المنطقة", ['غير محدد', 'الرياض', 'مكة المكرمة', 'عسير', 'نجران', 'الباحة', 'تبوك', 'القصيم',
                                                        'جازان', 'المنطقة الشرقية', 'الجوف', 'حائل', 'الحدود الشمالية', 'المدينة المنورة'],
                                        key="social_zone")

            with col_left:
                social_content = st.text_area("المحتوى", key="social_content")
                social_class = st.selectbox('التصنيف', ["خبر", "انقطاع التيار", "شكوى", "فواتير", "مطالبة"], key="social_class")
                social_stage = st.selectbox('التقييم', ["إيجابي", 'سلبي', 'محايد'])
                social_url = st.text_area("الرابط", key="social_url")

            submit_social_button = st.form_submit_button(label="إرسال الخبر")

        if submit_social_button:
            new_tweet_entry = pd.DataFrame({
                "المنصة": [social_media],
                "التاريخ": [social_date],
                "الوقت": [social_time],
                "المنطقة": [social_zone],
                "التصنيف": [social_class],
                "المحتوى": [social_content],
                "التقييم": [social_stage],
                "الرابط": [social_url]
            })
            st.session_state["twitter_news_data"] = pd.concat([st.session_state["twitter_news_data"], new_tweet_entry], ignore_index=True)
            save_data(st.session_state["twitter_news_data"], TWITTER_CSV)
            st.success("تم إرسال الخبر بنجاح!")

        if not st.session_state["twitter_news_data"].empty:
            st.subheader("رصد التواصل الإجتماعي")
            edited_tweet_df = st.data_editor(st.session_state["twitter_news_data"])
            st.session_state["twitter_news_data"] = edited_tweet_df
            save_data(edited_tweet_df, TWITTER_CSV)
