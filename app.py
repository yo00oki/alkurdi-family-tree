import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة بمظهر عريض وتثبيت القائمة الجانبية مغلقة تماماً
st.set_page_config(page_title="شجرة عائلة الكردي", layout="wide", initial_sidebar_state="collapsed")

# هندسة الـ CSS الحاسمة: توحيد المسافات تماماً وإجبار اللون الأسود الصريح ومنع الرموز المتداخلة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;800;900&display=swap');

    .stApp {
        background-color: #f7f5f0;
    }
    body, .main, .block-container { 
        direction: rtl; 
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }
    
    /* حظر القائمة الجانبية المزعجة في الجوال والخطوط الفاصلة */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* هيدر علوي متموضع في المنتصف */
    .header-container {
        background-color: #1b4332;
        padding: 20px 15px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
    }
    .main-title {
        color: #fcfbf7;
        font-family: 'Cairo', sans-serif; 
        font-weight: 900;
        font-size: 32px;
        margin: 0 auto;
    }
    .subtitle {
        color: #b7e4c7;
        font-size: 15px;
        font-weight: 600;
        margin-top: 8px;
        text-align: center !important;
    }
    
    /* توحيد صناديق الأسماء تماماً وتثبيت التباعد كالمسطرة */
    .stExpander {
        background-color: #ffffff !important;
        border: 1px solid #e9e5db !important;
        border-radius: 8px !important;
        padding: 0px !important;
        
        /* تصفير الهوامش العلوية وجعل التباعد السفلي 6 بكسل ثابتاً بين كل الإطارات دون مليمتر واحد تفاوت */
        margin-top: 0px !important;
        margin-bottom: 6px !important; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.01) !important;
    }
    
    /* إجبار محرك الـ Expander على جعل كافة العناوين والنصوص سوداء داكنة جداً وحادة في الجوال */
    .stExpander p, .stExpander span, .stExpander text, .stExpander summary, .stMarkdown p {
        font-family: 'Cairo', sans-serif !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        color: #111111 !important; /* أسود ناصع وصريح 100% */
        text-align: right !important;
    }
    
    /* إخفاء سهم الفتح للأعضاء بلا أطفال مع بقاء نفس أبعاد وتنسيق الصندوق الموحد */
    .leaf-node-container button [data-testid="stExpanderToggleIcon"] {
        display: none !important; 
    }
    .leaf-node-container button {
        pointer-events: none !important; 
        cursor: default !important;
    }
    
    /* تنسيق صندوق البحث الذكي الموحد */
    .search-box-holder {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e9e5db;
        margin-bottom: 25px;
    }
    .stTextInput input { 
        text-align: right; 
        direction: rtl; 
        border: 2px solid #b7e4c7;
        border-radius: 8px; 
        color: #111111 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 1. تحميل قراءة ملف الإكسل تلقائياً
@st.cache_data
def load_data():
    excel_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls'))]
    if not excel_files:
        raise FileNotFoundError("لم يتم العثور على ملف الإكسل.")
    df = pd.read_excel(excel_files[0])
    df['ID'] = df['ID'].astype(str).str.replace('.0', '', regex=False)
    df['Parent_ID'] = df['Parent_ID'].fillna('').astype(str).str.replace('.0', '', regex=False)
    df['Generation'] = df['Generation'].astype(int)
    df['Status'] = df['Status'].fillna('حي')
    df['Notes'] = df['Notes'].fillna('')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"خطأ في قراءة ملف الإكسل: {e}")
    st.stop()

family_dict = df.set_index('ID').to_dict('index')

def get_full_name(node_id):
    if node_id not in family_dict or not node_id:
        return ""
    current = family_dict[node_id]
    parent_id = current['Parent_ID']
    if parent_id and parent_id in family_dict:
        return f"{current['name']} بن {get_full_name(parent_id)}"
    return current['name']

# الهيدر العلوي في المنتصف
st.markdown("""
    <div class='header-container'>
        <div class='main-title'>🌳 شجرة عائلة الكردي</div>
        <div class='subtitle'>شجرة عائلة الكردي بدء من الجد عبد العزيز بن نعمان الكردي رحمه الله</div>
    </div>
""", unsafe_allow_html=True)

# 2. صندوق البحث الذكي الموحد والنظيف
st.markdown("<div class='search-box-holder'>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 16px; font-weight: bold; color: #1b4332; margin-bottom: 6px !important;'>🔍 البحث الذكي في العائلة:</p>", unsafe_allow_html=True)
search_query = st.text_input("البحث", label_visibility="collapsed", placeholder="اكتب الاسم هنا للبحث الفوري...")

selected_member = None
if search_query:
    results = df[df['name'].str.contains(search_query, case=False, na=False)]
    if not results.empty:
        options = {row['ID']: f"{row['name']} ({get_full_name(row['ID'])})" for _, row in results.iterrows()}
        selected_id = st.selectbox("اختر الشخص لمعاينة تفاصيله:", options=options.keys(), format_func=lambda x: options[x])
        selected_member = family_dict[selected_id]
        selected_member['ID'] = selected_id
    else:
        st.warning("لم يتم العثور على هذا الاسم.")

if selected_member:
    status_emoji = "🟢" if selected_member['Status'] == "حي" else "⚫ (رحمه الله)"
    st.info(f"""
    🪪 **البطاقة الشخصية للمعاينة:**
    * **الاسم الكامل:** {get_full_name(selected_member['ID'])}
    * **الجيل:** {selected_member['Generation']}
    * **الحالة:** {selected_member['Status']} {status_emoji}
    * **ملاحظات:** {selected_member['Notes'] if selected_member['Notes'] else 'لا توجد ملاحظات.'}
    """)
st.markdown("</div>", unsafe_allow_html=True)

# 3. الدالة البرمجية النظيفة تماماً من أي رموز مع توحيد المسافات المطلقة
def display_accordion_tree(parent_id, df_data):
    children = df_data[df_data['Parent_ID'] == parent_id]
    
    for _, row in children.iterrows():
        child_id = row['ID']
        name_str = row['name']
        status_str = " (رحمه الله)" if row['Status'] == "متوفى" else ""
        gen = row['Generation']
        
        prefix_emoji = "👨" if gen == 2 else "👦" if gen == 3 else "👶"
        
        # نصوص نقية صريحة بدون أي وسوم HTML لمنع التشوه
        label_text = f"{prefix_emoji} {name_str}{status_str}"
        
        has_children = not df_data[df_data['Parent_ID'] == child_id].empty
        
        if has_children:
            with st.expander(label_text, expanded=False):
                display_accordion_tree(child_id, df_data)
        else:
            st.markdown("<div class='leaf-node-container'>", unsafe_allow_html=True)
            with st.expander(label_text, expanded=False):
                pass 
            st.markdown("</div>", unsafe_allow_html=True)

# عرض الشجرة الشاملة والنظيفة
st.markdown("<h3 style='text-align: right; color: #1b4332; margin-top: 5px; margin-bottom: 10px; font-size: 20px;'>🌿 تصفح أفرع العائلة:</h3>", unsafe_allow_html=True)

root_row = df[df['Parent_ID'] == '']
if not root_row.empty:
    root_id = root_row['ID'].iloc[0]
    
    with st.expander("👑 عبد العزيز نعمان الكردي رحمه الله", expanded=True):
        display_accordion_tree(root_id, df)
else:
    st.error("تأكد من وجود بيانات الجد الأكبر في ملف الإكسل.")
