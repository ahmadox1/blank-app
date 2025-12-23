import streamlit as st
import yfinance as yf
import google.generativeai as genai

# 1. إعداد الصفحة لتكون بعرض كامل (Wide Layout)
st.set_page_config(page_title="محلل تداول الاحترافي", layout="wide")

st.markdown("""
    <style>
    .full-width-report { width: 100%; background: #ffffff; padding: 30px; border-radius: 15px; border-right: 10px solid #0056b3; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 20px; }
    .stButton>button { width: 100%; height: 3.5em; font-weight: bold; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 رادار الأسهم السعودية الذكي (تداول & أرقام)")
st.write("بحث مباشر في المصادر المحلية وتحليل فني متكامل")

api_key = st.sidebar.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # تفعيل أداة البحث الصحيحة لعام 2025
        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash', 
            tools=[{"google_search": {}}] 
        )

        stocks = {
            "أرامكو": "2222.SR",
            "اسمنت القصيم": "3020.SR",
            "مصرف الإنماء": "1150.SR",
            "اس تي سي": "7010.SR"
        }

        # عرض الأزرار بشكل عرضي
        cols = st.columns(4)
        for i, (name, symbol) in enumerate(stocks.items()):
            if cols[i].button(f"🔍 تحليل {name}", key=symbol):
                st.session_state.selected = (name, symbol)

        # منطقة التحليل بعرض الصفحة كاملة (تحت الأزرار)
        if 'selected' in st.session_state:
            name, symbol = st.session_state.selected
            
            with st.spinner(f"جاري جلب بيانات {name} والبحث في أرقام وتداول..."):
                ticker = yf.Ticker(symbol)
                # جلب بيانات شهر كامل ليعرف الموديل حركة السهم (يمنع الاعتذار)
                df = ticker.history(period="1mo")
                current_price = df['Close'].iloc[-1]
                avg_price = df['Close'].mean()
                volume = df['Volume'].iloc[-1]
                
                # أمر البحث الصارم
                prompt = f"""
                مهم جداً: استخدم أداة البحث للوصول لموقعي (أرقام Argaam) و (تداول Tadawul) حصراً.
                ابحث عن آخر أخبار سهم {name} ({symbol}) لليوم وأمس.
                
                بناءً على الأخبار الحقيقية التي ستجدها وبيانات السهم (السعر الحالي: {current_price:.2f}، المتوسط: {avg_price:.2f}، الحجم: {volume}):
                1. ما هو الخبر المحلي الجديد؟ (اذكر المصدر والوقت).
                2. شرح تأثير الخبر (إيجابي أم سلبي للنمو؟).
                3. تحليل فني: هل السهم في منطقة شراء؟ وما هي الأهداف القادمة؟
                
                اجعل التقرير مرتباً جداً بعناوين عريضة وواضحة.
                """
                
                response = model.generate_content(prompt)
                
                # عرض التقرير في حاوية عريضة بالأسفل
                st.markdown(f"""
                <div class="full-width-report">
                    <h2 style='color:#0056b3;'>📝 التقرير التحليلي الكامل لسهم {name}</h2>
                    <hr>
                    <div style='font-size: 1.1em; line-height: 1.8;'>
                        {response.text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
else:
    st.info("💡 بانتظار إدخال مفتاح API في الشريط الجانبي لتفعيل البحث الذكي.")
