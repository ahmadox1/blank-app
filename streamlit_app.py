import streamlit as st
import yfinance as yf
import google.generativeai as genai
import pandas_ta as ta # لحساب المؤشرات الفنية

st.set_page_config(page_title="محلل تداول الذكي", layout="wide")

st.markdown("""
    <style>
    .report-full { width: 100%; background: #ffffff; padding: 30px; border-radius: 15px; border: 1px solid #e0e0e0; border-top: 8px solid #00a651; margin-top: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .stButton>button { height: 3.5em; border-radius: 8px; font-weight: bold; background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 نظام تحليل الأسهم السعودية (أرقام & تداول)")

api_key = st.sidebar.text_input("أدخل مفتاح Gemini API:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # تفعيل أداة البحث google_search كما طلبت الصورة الأخيرة
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash', # الإصدار الأحدث والأذكى لعام 2025
        tools=[{"google_search": {}}] 
    )

    stocks = {
        "أرامكو": "2222.SR",
        "اسمنت القصيم": "3020.SR",
        "مصرف الإنماء": "1150.SR",
        "اس تي سي": "7010.SR"
    }

    cols = st.columns(4)
    for i, (name, symbol) in enumerate(stocks.items()):
        if cols[i].button(f"🔎 تحليل {name}", key=symbol):
            st.session_state.active = (name, symbol)

    if 'active' in st.session_state:
        name, symbol = st.session_state.active
        with st.spinner(f"جاري البحث في أرقام وتداول عن أحدث أخبار {name}..."):
            # 1. جلب بيانات فنية متقدمة (لمنع اعتذار الموديل)
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="3mo")
            
            # حساب مؤشرات (RSI والمتوسطات)
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['SMA_20'] = ta.sma(df['Close'], length=20)
            
            current_price = df['Close'].iloc[-1]
            last_rsi = df['RSI'].iloc[-1]
            last_volume = df['Volume'].iloc[-1]

            # 2. الأمر الصارم للبحث في المواقع السعودية
            prompt = f"""
            أنت محلل مالي في السوق السعودي. السهم: {name} ({symbol}). السعر الحالي: {current_price:.2f}.
            المؤشرات الفنية الحالية: RSI هو {last_rsi:.2f}، وحجم التداول الأخير هو {last_volume}.
            
            المطلوب منك الآن وبشكل إلزامي:
            1. ابحث باستخدام جوجل في موقع (أرقام Argaam) وموقع (تداول Tadawul) عن آخر إعلانات وأخبار الشركة لليوم وأمس.
            2. لخص أهم خبر وجدته واشرح تأثيره المباشر على السعر.
            3. قدم تحليلاً فنياً يدمج بين (السعر، RSI، والأخبار).
            4. التوصية: هل السعر الحالي فرصة دخول؟ وما هي الأهداف القادمة؟
            
            اجعل التقرير مرتباً جداً بعناوين عريضة.
            """
            
            try:
                response = model.generate_content(prompt)
                
                # 3. عرض التقرير في مساحة عريضة
                st.markdown(f'<div class="report-full">', unsafe_allow_html=True)
                st.subheader(f"📝 التقرير الشامل لسهم {name}")
                st.write(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"تنبيه: {str(e)}")
else:
    st.info("💡 يرجى إدخال مفتاح الـ API لتفعيل ميزة البحث في أرقام وتداول.")
