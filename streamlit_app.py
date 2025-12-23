import streamlit as st
import yfinance as yf
from google import genai # المكتبة الجديدة لعام 2025
import pandas as pd

# 1. إعداد الصفحة للعرض العريض والاحترافي
st.set_page_config(page_title="رادار تداول 2026", layout="wide")

st.markdown("""
    <style>
    .report-card { width: 100%; background: white; padding: 25px; border-radius: 15px; border-right: 12px solid #00a651; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-top: 20px; }
    .stButton>button { width: 100%; height: 3.8em; font-weight: bold; border-radius: 12px; transition: 0.3s; }
    .stButton>button:hover { background-color: #00a651; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 منصة تحليل الأسهم السعودية (الجيل الجديد)")
st.write("تم التحديث للمكتبة الجديدة لضمان دقة البحث في أرقام وتداول")

# 2. إعداد المفتاح الجديد
api_key = st.sidebar.text_input("أدخل مفتاح Gemini API:", type="password")

if api_key:
    try:
        # الربط باستخدام المكتبة الجديدة google-genai
        client = genai.Client(api_key=api_key)
        
        stocks = {
            "أرامكو": "2222.SR",
            "اسمنت القصيم": "3020.SR",
            "مصرف الإنماء": "1150.SR",
            "اس تي سي": "7010.SR"
        }

        # عرض الأزرار بشكل عرضي أنيق
        cols = st.columns(4)
        for i, (name, symbol) in enumerate(stocks.items()):
            if cols[i].button(f"🔎 تحليل {name}", key=symbol):
                st.session_state.active_stock = (name, symbol)

        # منطقة التحليل بعرض الصفحة الكاملة
        if 'active_stock' in st.session_state:
            name, symbol = st.session_state.active_stock
            
            with st.spinner(f"جاري البحث والتحليل المتقدم لسهم {name}..."):
                # جلب البيانات الفنية المباشرة
                ticker = yf.Ticker(symbol)
                df = ticker.history(period="1mo")
                curr_p = df['Close'].iloc[-1]
                
                # استخدام ميزة البحث المباشر في المكتبة الجديدة
                prompt = f"""
                ابحث في الإنترنت (موقع أرقام وتداول السعودية) عن آخر أخبار {name} ({symbol}) لليوم.
                بناءً على السعر الحالي {curr_p:.2f} ريال والأخبار المكتشفة:
                1. ما هو الخبر الأهم والمصدر؟
                2. كيف سيؤثر الخبر على السهم (إيجابي/سلبي)؟
                3. التوصية الفنية: سعر الدخول المناسب والهدف.
                رتب التقرير بشكل احترافي.
                """
                
                # تنفيذ الطلب باستخدام الموديل الأحدث Gemini 2.0 Flash
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt,
                    config={
                        'tools': [{'google_search': {}}] # تفعيل البحث بجوجل
                    }
                )
                
                # عرض النتيجة في حاوية عريضة جداً
                st.markdown(f"""
                <div class="report-card">
                    <h2 style='color:#0056b3;'>📝 التقرير الذكي لسهم {name}</h2>
                    <hr>
                    <div style='font-size: 1.15em; line-height: 1.9;'>
                        {response.text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
    except Exception as e:
        st.error(f"حدث خطأ في المكتبة الجديدة: {e}")
else:
    st.info("💡 يرجى إدخال مفتاح API لتشغيل الرادار المالي.")
