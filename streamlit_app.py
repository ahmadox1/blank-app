import streamlit as st
import yfinance as yf
import google.generativeai as genai

# 1. إعداد الصفحة لتكون بعرض كامل ومريح
st.set_page_config(page_title="رادار تداول الذكي", layout="wide")

st.markdown("""
    <style>
    .report-box { width: 100%; background-color: #ffffff; padding: 25px; border-radius: 15px; border-right: 10px solid #28a745; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-top: 20px; }
    .stButton>button { height: 3.5em; font-weight: bold; font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 منصة تحليل الأسهم السعودية v3 (أخبار + تحليل)")
st.write("الكود يجلب الأخبار المحلية والعالمية ويرسلها لنموذج Gemini 2.5 للتحليل")

# 2. إعداد مفتاح API في الجانب
api_key = st.sidebar.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # استخدام الإصدار الأحدث gemini-2.5-flash الذي طلبت
    model = genai.GenerativeModel('gemini-2.5-flash')

    stocks = {
        "أرامكو": "2222.SR",
        "اسمنت القصيم": "3020.SR",
        "مصرف الإنماء": "1150.SR",
        "اس تي سي": "7010.SR"
    }

    # 3. عرض الأزرار بشكل عرضي (4 أعمدة)
    cols = st.columns(4)
    for i, (name, symbol) in enumerate(stocks.items()):
        if cols[i].button(f"🔍 تحليل {name}", key=symbol):
            st.session_state.active_stock = (name, symbol)

    # 4. منطقة التحليل (تظهر بعرض الصفحة كاملة بالأسفل)
    if 'active_stock' in st.session_state:
        name, symbol = st.session_state.active_stock
        
        with st.spinner(f"جاري جلب أخبار {name} وتحليلها..."):
            # أ- جلب البيانات السعرية برمجياً
            ticker = yf.Ticker(symbol)
            current_price = ticker.history(period="1d")['Close'].iloc[-1]
            
            # ب- جلب الأخبار برمجياً (هنا الكود هو من يأتي بالأخبار)
            raw_news = ticker.news
            news_summary = ""
            if raw_news:
                for n in raw_news[:5]: # نأخذ آخر 5 أخبار
                    news_summary += f"- العنوان: {n.get('title')} (المصدر: {n.get('publisher')})\n"
            else:
                news_summary = "لم يتم العثور على أخبار عاجلة في الساعات الماضية."

            # ج- إرسال البيانات الجاهزة للموديل (Gemini 2.5)
            prompt = f"""
            أنت محلل مالي خبير. لقد قمت بجلب البيانات التالية لسهم {name} ({symbol}):
            1- السعر الحالي: {current_price:.2f} ريال.
            2- آخر الأخبار المتوفرة: 
            {news_summary}
            
            المطلوب منك (بناءً على هذه المعطيات تحديداً):
            - ترجم ولخص الأخبار إذا كانت بالإنجليزية واشرحها ببساطة.
            - وضح كيف سيؤثر هذا الخبر على سعر السهم في تداول (إيجابي/سلبي).
            - حدد "سعر الدخول المثالي" و "الهدف" بناءً على حركة السعر والخبر.
            رتب إجابتك في نقاط واضحة جداً.
            """
            
            try:
                response = model.generate_content(prompt)
                
                # د- عرض التقرير في مساحة عريضة جداً بالأسفل
                st.markdown(f"""
                <div class="report-box">
                    <h2 style='color:#0056b3;'>📝 التقرير التحليلي لـ {name}</h2>
                    <p style='font-size: 1.2em;'><b>السعر الحالي:</b> {current_price:.2f} ريال</p>
                    <hr>
                    <div style='font-size: 1.1em; color: #333;'>
                        {response.text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"حدث خطأ في التحليل: {e}")
else:
    st.info("💡 يرجى وضع مفتاح API لتفعيل الرصد والتحليل.")
