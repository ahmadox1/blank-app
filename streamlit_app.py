import streamlit as st
import yfinance as yf
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="مستشارك المالي الذكي", layout="wide")

# تصميم الواجهة وتوسيع الحاويات
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .report-container { 
        width: 100%; 
        background-color: white; 
        padding: 30px; 
        border-radius: 15px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-top: 20px;
        border-right: 8px solid #0056b3;
    }
    .stButton>button { width: 100%; height: 3.5em; font-weight: bold; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 نظام الرصد والتحليل الذكي للأسهم السعودية")
st.write("يتم الآن البحث في المصادر المحلية (أرقام، تداول، واس) وتحليلها فوراً")

api_key = st.sidebar.text_input("أدخل مفتاح Gemini API:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # تفعيل موديل Gemini مع خاصية البحث في جوجل
    # ملاحظة: نستخدم gemini-1.5-flash أو gemini-2.0-flash مع تفعيل التصفح
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        tools=[{"google_search_retrieval": {}}] 
    )

    stocks = {
        "أرامكو": "2222.SR",
        "اسمنت القصيم": "3020.SR",
        "مصرف الإنماء": "1150.SR",
        "اس تي سي": "7010.SR"
    }

    # إنشاء الأزرار
    cols = st.columns(4)
    selected_stock = None

    for i, (name, symbol) in enumerate(stocks.items()):
        if cols[i].button(f"🔍 تحليل {name}"):
            st.session_state.selected_stock = (name, symbol)

    # عرض التحليل في المساحة العريضة أسفل الأزرار
    if 'selected_stock' in st.session_state:
        name, symbol = st.session_state.selected_stock
        
        with st.spinner(f"جاري البحث في الإنترنت وتحليل سهم {name}..."):
            # جلب السعر الحالي
            ticker = yf.Ticker(symbol)
            current_price = ticker.history(period="1d")['Close'].iloc[-1]
            
            # أمر الذكاء الاصطناعي مع تفعيل البحث
            prompt = f"""
            استخدم ميزة البحث في جوجل للعثور على آخر أخبار سهم {name} (الرمز {symbol}) 
            في مواقع (أرقام، تداول، العربية نت) لآخر 48 ساعة.
            ثم قدم لي تقريراً احترافياً باللغة العربية كالتالي:
            1. السعر الحالي: {current_price:.2f} ريال.
            2. ملخص لأهم الأخبار المكتشفة وتواريخها.
            3. شرح مختصر لتأثير الخبر (هل هو إيجابي أم سلبي للنمو؟).
            4. التوقع الفني: هل السعر الحالي مناسب للدخول؟ وما هو الهدف القريب؟
            
            اجعل العرض مرتباً جداً باستخدام النقاط.
            """
            
            try:
                response = model.generate_content(prompt)
                
                # عرض النتيجة في حاوية عريضة (Full Width)
                st.markdown(f"""
                <div class="report-container">
                    <h2 style='color:#0056b3;'>📝 تقرير تحليل سهم {name}</h2>
                    <hr>
                    <div style='font-size: 1.1em; line-height: 1.8;'>
                        {response.text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")

else:
    st.info("💡 يرجى وضع مفتاح الـ API في اليسار لتفعيل خاصية البحث والتحليل.")
