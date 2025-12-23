import streamlit as st
import yfinance as yf
import google.generativeai as genai

# --- إعدادات الواجهة ---
st.set_page_config(page_title="محلل الأسهم الخاص بي", layout="wide")
st.title("📊 منصة تحليل الأسهم السعودية الخاصة")
st.write("اختر السهم واضغط على الزر لتحليله فوراً")

# --- إعداد الذكاء الاصطناعي ---
api_key = st.sidebar.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # تم تحديث اسم الموديل هنا إلى الإصدار الأحدث والأسرع
        model = genai.GenerativeModel('gemini-2.5-flash')

        stocks = {
            "أرامكو": "2222.SR",
            "اسمنت القصيم": "3020.SR",
            "مصرف الإنماء": "1150.SR",
            "اس تي سي": "7010.SR"
        }

        cols = st.columns(4)

        for i, (name, symbol) in enumerate(stocks.items()):
            with cols[i]:
                if st.button(f"تحليل {name}"):
                    with st.spinner(f"جاري تحليل {name}..."):
                        ticker = yf.Ticker(symbol)
                        # جلب بيانات أكثر (آخر 3 أشهر) ليعطي الذكاء الاصطناعي رؤية أفضل
                        hist = ticker.history(period="3mo")
                        if not hist.empty:
                            current_price = hist['Close'].iloc[-1]
                            
                            prompt = f"""
                            أنت خبير مالي في السوق السعودي (تداول). 
                            حلل سهم {name} (الرمز: {symbol}). 
                            السعر الحالي: {current_price:.2f} ريال.
                            بناءً على تحركات السعر الأخيرة، أعطني باختصار:
                            1- هل السعر الحالي مناسب للدخول؟
                            2- ما هي نقاط الدعم والمقاومة القريبة؟
                            3- نصيحة سريعة للمتداول.
                            """
                            
                            response = model.generate_content(prompt)
                            
                            st.success(f"السعر الحالي لـ {name}: {current_price:.2f} ريال")
                            st.markdown(response.text)
                        else:
                            st.error("عذراً، تعذر جلب بيانات السهم حالياً.")
    except Exception as e:
        st.error(f"حدث خطأ في الاتصال بالذكاء الاصطناعي: {e}")
else:
    st.warning("يرجى إدخال مفتاح API في الشريط الجانبي لتفعيل المنصة.")
