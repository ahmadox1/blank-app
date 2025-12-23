import streamlit as st
import yfinance as yf
import google.generativeai as genai

# إعدادات واجهة احترافية
st.set_page_config(page_title="الرادار المالي السعودي", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .news-box { padding: 15px; border-radius: 10px; border-left: 5px solid #007bff; background-color: white; margin-bottom: 10px; }
    .analysis-box { background-color: #e9ecef; padding: 15px; border-radius: 10px; border-right: 5px solid #28a745; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 منصة التحليل الإخباري والفني للأسهم السعودية")
st.write("---")

api_key = st.sidebar.text_input("أدخل مفتاح Gemini API:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # استخدام الإصدار الأحدث المستقر لعام 2025
        model = genai.GenerativeModel('gemini-2.5-flash')

        stocks = {
            "أرامكو": "2222.SR",
            "اسمنت القصيم": "3020.SR",
            "مصرف الإنماء": "1150.SR",
            "اس تي سي": "7010.SR"
        }

        # عرض الأزرار بشكل مرتب
        cols = st.columns(4)
        for i, (name, symbol) in enumerate(stocks.items()):
            with cols[i]:
                if st.button(f"🔍 تحليل {name}", key=symbol):
                    with st.spinner(f"جاري معالجة بيانات {name}..."):
                        stock_obj = yf.Ticker(symbol)
                        
                        # جلب السعر مع معالجة الأخطاء
                        hist = stock_obj.history(period="5d")
                        if hist.empty:
                            st.error(f"عذراً، تعذر سحب سعر {name}")
                            continue
                        current_price = hist['Close'].iloc[-1]
                        
                        # جلب الأخبار بشكل آمن لتجنب خطأ الـ title
                        raw_news = stock_obj.news
                        
                        st.markdown(f"### 📊 تقرير سهم {name} ({symbol})")
                        st.metric("السعر الحالي", f"{current_price:.2f} ريال")
                        
                        if not raw_news:
                            st.info("لا توجد أخبار عالمية حديثة لهذا السهم حالياً.")
                        else:
                            for news_item in raw_news[:3]: # سنأخذ أهم 3 أخبار فقط للترتيب
                                title = news_item.get('title', 'عنوان غير متوفر')
                                publisher = news_item.get('publisher', 'مصدر مجهول')
                                
                                # عرض الخبر بشكل مرتب
                                st.markdown(f"""
                                <div class="news-box">
                                    <strong>الخبر:</strong> {title}<br>
                                    <small>المصدر: {publisher}</small>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # طلب تحليل الخبر من الذكاء الاصطناعي بشكل مخصص
                                prompt = f"""
                                حلل هذا الخبر المتعلق بسهم {name} في السوق السعودي:
                                الخبر: {title}
                                السعر الحالي: {current_price:.2f}
                                المطلوب (بشكل مختصر جداً ومرتب):
                                1- شرح مبسط للخبر.
                                2- تأثير الخبر على السعر (إيجابي/سبي/محايد).
                                3- نصيحة دخول/انتظار بناءً على هذا المعطى.
                                """
                                
                                analysis = model.generate_content(prompt)
                                
                                st.markdown(f"""
                                <div class="analysis-box">
                                    <strong>💡 تحليل المستشار الذكي:</strong><br>
                                    {analysis.text}
                                </div>
                                """, unsafe_allow_html=True)
                                st.write("---")

    except Exception as e:
        st.error(f"حدث خطأ في النظام: {e}")
else:
    st.warning("⚠️ يرجى إدخال مفتاح الـ API في القائمة الجانبية لتفعيل المحلل.")
