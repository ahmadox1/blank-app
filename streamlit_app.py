import streamlit as st
import yfinance as yf
import google.generativeai as genai

# إعداد الصفحة لتكون بعرض كامل
st.set_page_config(page_title="رادار الأسهم السعودية", layout="wide")

# تصميم الواجهة للعرض العريض
st.markdown("""
    <style>
    .report-full { width: 100%; background: #ffffff; padding: 25px; border-radius: 12px; border: 1px solid #ddd; border-top: 6px solid #1a73e8; margin-top: 20px; }
    .stButton>button { height: 3.5em; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 نظام التحليل الذكي للأسهم (تداول & أرقام)")

api_key = st.sidebar.text_input("أدخل مفتاح Gemini API:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # تصحيح تعريف أداة البحث (Google Search Tool)
    # نستخدم الموديل المستقر المحدث لعام 2025
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        tools=[{"google_search": {}}] # هذا هو التعريف الصحيح للأداة
    )

    stocks = {
        "أرامكو": "2222.SR",
        "اسمنت القصيم": "3020.SR",
        "مصرف الإنماء": "1150.SR",
        "اس تي سي": "7010.SR"
    }

    # الأزرار في صف واحد
    cols = st.columns(4)
    for i, (name, symbol) in enumerate(stocks.items()):
        if cols[i].button(f"🔎 تحليل {name}", key=symbol):
            st.session_state.target = (name, symbol)

    # عرض التقرير في مساحة عريضة بالأسفل
    if 'target' in st.session_state:
        name, symbol = st.session_state.target
        with st.spinner(f"جاري جلب أحدث أخبار {name} من الإنترنت وتحليلها..."):
            ticker = yf.Ticker(symbol)
            price = ticker.history(period="1d")['Close'].iloc[-1]
            
            prompt = f"""
            ابحث الآن في الإنترنت عن آخر أخبار شركة {name} (الرمز {symbol}) في مواقع تداول وأرقام لليوم وأمس.
            ثم اكتب لي تقريراً مرتباً كالتالي:
            1. السعر الحالي: {price:.2f} ريال.
            2. أهم خبر محلي وجدته (بالتفصيل).
            3. تحليل الخبر: هل يدعم صعود السهم أم هبوطه؟
            4. التوصية: أفضل سعر للدخول والهدف المتوقع.
            """
            
            try:
                response = model.generate_content(prompt)
                
                # عرض النتيجة في حاوية عريضة تأخذ مساحة الصفحة كاملة
                st.markdown(f'<div class="report-full">', unsafe_allow_html=True)
                st.subheader(f"📝 التقرير الكامل لسهم {name}")
                st.write(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"تنبيه: {str(e)}")
else:
    st.info("💡 بانتظار إدخال مفتاح الـ API للبدء.")
