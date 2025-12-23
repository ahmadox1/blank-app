import streamlit as st
import yfinance as yf
import google.generativeai as genai

# --- إعدادات الواجهة ---
st.set_page_config(page_title="محلل الأسهم الخاص بي", layout="wide")
st.title("📊 منصة تحليل الأسهم السعودية الخاصة")
st.write("اختر السهم واضغط على الزر لتحليله فوراً")

# --- إعداد الذكاء الاصطناعي ---
# ضع مفتاحك هنا أو سنطلبه منك في الواجهة
api_key = st.sidebar.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    # الأسهم الأربعة التي اخترتها
    stocks = {
        "أرامكو": "2222.SR",
        "اسمنت القصيم": "3020.SR",
        "مصرف الإنماء": "1150.SR",
        "اس تي سي": "7010.SR"
    }

    # إنشاء 4 أعمدة للأزرار
    cols = st.columns(4)

    for i, (name, symbol) in enumerate(stocks.items()):
        with cols[i]:
            if st.button(f"تحليل {name}"):
                with st.spinner(f"جاري تحليل {name}..."):
                    # سحب بيانات السهم
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="1mo")
                    current_price = hist['Close'][-1]
                    
                    # طلب التحليل من الذكاء الاصطناعي
                    prompt = f"أنت خبير في سوق الأسهم السعودي. سهم {name} (رمزه: {symbol}) سعره الحالي هو {current_price:.2f}. بناءً على حركة السعر في الشهر الأخير، أعطني: 1- تحليل فني مختصر 2- أفضل سعر للدخول 3- توقعك للسعر."
                    response = model.generate_content(prompt)
                    
                    st.success(f"السعر الحالي لـ {name}: {current_price:.2f} ريال")
                    st.markdown(response.text)
else:
    st.warning("يرجى إدخال مفتاح API في الشريط الجانبي لتفعيل المنصة.")
