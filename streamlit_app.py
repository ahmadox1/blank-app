import streamlit as st
import yfinance as yf
import google.generativeai as genai

st.set_page_config(page_title="مستشاري المالي الذكي", layout="wide")
st.title("🚀 منصة تحليل الأسهم والأخبار السعودية")

api_key = st.sidebar.text_input("أدخل مفتاح Gemini API:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # استخدام الموديل الأحدث المستقر لعام 2025
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
                if st.button(f"تحليل أخبار {name}", key=symbol):
                    with st.spinner(f"جاري جلب أخبار وتحليلات {name}..."):
                        ticker = yf.Ticker(symbol)
                        
                        # 1. جلب السعر
                        hist = ticker.history(period="5d")
                        current_price = hist['Close'].iloc[-1]
                        
                        # 2. جلب الأخبار (ميزة التحديث الجديد)
                        news_list = ticker.news
                        news_text = ""
                        for news in news_list[:5]: # نأخذ آخر 5 أخبار فقط
                            news_text += f"- {news['title']} (المصدر: {news['publisher']})\n"
                        
                        # 3. صياغة الأمر للذكاء الاصطناعي
                        prompt = f"""
                        أنت محلل مالي في السوق السعودي. سهم {name} سعره الحالي {current_price:.2f} ريال.
                        إليك آخر العناوين الإخبارية المرتبطة بالسهم:
                        {news_text if news_text else "لا توجد أخبار حديثة جداً."}
                        
                        بناءً على هذا الخبر وسعر السهم:
                        1- حلل تأثير هذه الأخبار على مستقبل السهم القريب.
                        2- هل الأخبار إيجابية أم سلبية؟
                        3- ما هو السعر المثالي للدخول بناءً على المعطيات الحالية؟
                        """
                        
                        response = model.generate_content(prompt)
                        
                        st.subheader(f"📊 تحليل {name}")
                        st.info(f"السعر الحالي: {current_price:.2f} ريال")
                        st.write("---")
                        st.markdown(response.text)
                        
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
else:
    st.warning("يرجى إدخال مفتاح الـ API للبدء.")
