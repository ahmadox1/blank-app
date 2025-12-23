import streamlit as st
import yfinance as yf
import google.generativeai as genai

# إعدادات واجهة احترافية متقدمة
st.set_page_config(page_title="الرادار المالي السعودي v2", layout="wide")

# تصميم CSS لجعل الواجهة تبدو كمنصة احترافية
st.markdown("""
    <style>
    .report-card { background-color: #ffffff; border-radius: 15px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 5px solid #007bff; margin-bottom: 20px; }
    .news-section { background-color: #f8f9fa; border-right: 4px solid #ffc107; padding: 10px; margin: 10px 0; border-radius: 5px; }
    .analysis-section { background-color: #e8f5e9; border-right: 4px solid #28a745; padding: 10px; margin: 10px 0; border-radius: 5px; }
    .entry-price { font-size: 20px; color: #d32f2f; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 منصة تحليل الأسهم السعودية (أرقام & تداول)")
st.write("تحليل ذكي يعتمد على آخر الأخبار المحلية وتحركات السعر")

api_key = st.sidebar.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    stocks = {
        "أرامكو": "2222.SR",
        "اسمنت القصيم": "3020.SR",
        "مصرف الإنماء": "1150.SR",
        "اس تي سي": "7010.SR"
    }

    # توزيع الأزرار بشكل عرضي أنيق
    cols = st.columns(4)
    for i, (name, symbol) in enumerate(stocks.items()):
        with cols[i]:
            if st.button(f"📊 تحليل {name}", key=symbol):
                with st.spinner(f"جاري البحث في أرقام وتداول عن {name}..."):
                    # 1. جلب السعر اللحظي
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="5d")
                    current_price = hist['Close'].iloc[-1] if not hist.empty else 0
                    
                    # 2. أمر الذكاء الاصطناعي (البحث والتحليل)
                    prompt = f"""
                    أنت محلل مالي في السوق السعودي (تداول).
                    السهم: {name} (الرمز: {symbol}). السعر الحالي: {current_price:.2f} ريال.
                    المطلوب منك:
                    1. ابحث عن آخر أخبار هذا السهم في (موقع أرقام، موقع تداول، العربية بيزنس) لليوم وأمس.
                    2. لخص أهم خبر وجدته (العنوان والمحتوى باختصار).
                    3. اشرح تأثير هذا الخبر على السهم (إيجابي/سبي/محايد).
                    4. بناءً على السعر الحالي والأخبار، اقترح "أنسب سعر دخول" و "الهدف المتوقع".
                    رتب الإجابة بتنسيق Markdown مع عناوين واضحة.
                    """
                    
                    try:
                        response = model.generate_content(prompt)
                        
                        # 3. عرض النتائج بشكل "بطاقة" مرتبة
                        st.markdown(f"""
                        <div class="report-card">
                            <h2 style='color:#004a99;'>📝 تقرير {name}</h2>
                            <p style='font-size:18px;'><b>السعر الحالي:</b> {current_price:.2f} ريال</p>
                            <hr>
                            {response.text}
                        </div>
                        """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء التحليل: {e}")

else:
    st.info("💡 يرجى إدخال مفتاح الـ API في القائمة الجانبية لتفعيل المحلل الذكي.")
