import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة بمظهر فخم وعريض
st.set_page_config(page_title="شجرة عائلة الكردي", layout="wide", initial_sidebar_state="expanded")

# التنسيق الشامل الحاسم لتوحيد المسافات بالبكسل وإلغاء الهوامش الافتراضية المتفاوتة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;800;900&display=swap');

    .stApp {
        background-color: #f7f5f0;
    }
    body, .main, .block-container { 
        direction: rtl; 
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }
    /* هيدر تفصيلي علوي فخم في المنتصف تماماً */
    .header-container {
        background-color: #1b4332;
        padding: 25px;
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
        font-size: 40px;
        margin: 0 auto;
        text-align: center !important;
    }
    .subtitle {
        color: #b7e4c7;
        font-size: 18px;
        font-family: 'Cairo', sans-serif;
        font-weight: 600;
        margin-top: 8px;
        margin-bottom: 0;
        text-align: center !important;
    }
    
    /* توحيد التباعد الصارم والمطلق بوزن واحد لجميع الحاويات والصناديق */
    .stExpander {
        background-color: #ffffff !important;
        border: 1px solid #e9e5db !important;
        border-radius: 8px !important;
        padding: 0px !important;
        
        /* تصفير الهوامش العلوية وتثبيت هامش سفلي موحد تماماً بدقة 6 بكسل بين كل اسم والتالي له */
        margin-top: 0px !important;
        margin-bottom: 6px !important; 
        
        box-shadow: 0 2px 4px rgba(0,0,0,0.01) !important;
        text-align: right !important;
    }
    
    /* توحيد الهوامش الداخلية لبطاقات الأسماء */
    .stExpander [data-testid="stExpanderDetails"] {
        padding-top: 4px !important;
        padding-bottom: 4px !important;
        margin: 0px !important;
    }
    .stExpander p {
        font-family: 'Cairo', sans-serif !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        margin: 0px !important;
    }
    
    /* تطبيق نفس الارتفاع والهيكل لمن ليس لديهم أطفال لتوحيد الفراغات بشكل كامل */
    .leaf-node-container .stExpander {
        margin-top: 0px !important;
        margin-bottom: 6px !important; /* نفس التباعد تماماً */
    }
    
    /* إخفاء سهم الفتح للأعضاء بلا أطفال مع الحفاظ على نفس شكل البطاقة وحجمها */
    .leaf-node-container button [data-testid="stExpanderToggleIcon"] {
        display: none !important; 
    }
    .leaf-node-container button {
        pointer-events: none !important; 
        cursor: default !important;
    }
    
    /* تحسين القائمة الجانبية وتلوينها */
    [data-testid="stSidebar"] {
        background-color: #f0f4f1;
        border-left: 3px solid #b7e4c7;
    }
    .stTextInput input { 
        text-align: right; 
        direction: rtl; 
        border: 2px solid #b7e4c7;
        border-radius: 8px; 
        font-family: 'Cairo', sans-serif;
    }
    .stAlert p {
        text-align: right !important;
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

# القائمة الجانبية للبحث والبطاقات الذكية
st.sidebar.markdown("<h2 style='text-align:center; color:#1b4332; font-family:\"Cairo\", sans-serif; font-size:22px;'>🔍 البحث الذكي</h2>", unsafe_allow_html=True)
search_query = st.sidebar.text_input("ابحث عن اسم داخل العائلة:")

selected_member = None
if search_query:
    results = df[df['name'].str.contains(search_query, case=False, na=False)]
    if not results.empty:
        options = {row['ID']: f"{row['name']} ({get_full_name(row['ID'])})" for _, row in results.iterrows()}
        selected_id = st.sidebar.selectbox("اختر الشخص:", options=options.keys(), format_func=lambda x: options[x])
        selected_member = family_dict[selected_id]
        selected_member['ID'] = selected_id
    else:
        st.sidebar.warning("لم يتم العثور على هذا الاسم.")

if selected_member:
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='text-align:right; color:#1b4332; font-family:\"Cairo\", sans-serif; font-size:18px;'>🪪  البطاقة الشخصية</h3>", unsafe_allow_html=True)
    status_emoji = "🟢" if selected_member['Status'] == "حي" else "⚫ (رحمه الله)"
    st.sidebar.info(f"""
    **الاسم الكامل:** {get_full_name(selected_member['ID'])}
    **الجيل:** {selected_member['Generation']}
    **الحالة:** {selected_member['Status']} {status_emoji}
    **ملاحظات:** {selected_member['Notes'] if selected_member['Notes'] else 'لا توجد ملاحظات.'}
    """)

# 2. الدالة البرمجية المحدثة لتوحيد التباعد بالكامل أفقياً وعمودياً بالبكسل
def display_accordion_tree(parent_id, df_data):
    children = df_data[df_data['Parent_ID'] == parent_id]
    
    for _, row in children.iterrows():
        child_id = row['ID']
        name_str = row['name']
        status_str = " (رحمه الله)" if row['Status'] == "متوفى" else ""
        gen = row['Generation']
        
        # تحديد الإيموجي المناسب
        prefix_emoji = "👨" if gen == 2 else "👦" if gen == 3 else "👶"
        label_text = f"{prefix_emoji} {name_str}{status_str}"
        
        # فحص وجود الأطفال
        has_children = not df_data[df_data['Parent_ID'] == child_id].empty
        
        if has_children:
            # إذا كان لديه أولاد، يظهر كصندوق ممدد طبيعي
            with st.expander(label_text, expanded=False):
                display_accordion_tree(child_id, df_data)
        else:
            # إذا لم يكن لديه أولاد، يتم وضعه داخل حاوية مخصصة تصفر الفروقات وتجعل المسافة متطابقة 100% مع البقية وبدون أقفال أو أسهم
            st.markdown("<div class='leaf-node-container'>", unsafe_allow_html=True)
            with st.expander(label_text, expanded=False):
                pass 
            st.markdown("</div>", unsafe_allow_html=True)

# 3. عرض شجرة عائلة الكردي بالقائمة الملكية المتناسقة والموحدة بالبكسل
st.markdown("<h3 style='text-align: right; color: #1b4332; margin-top: 5px; margin-bottom: 10px; font-size: 20px;'>🌿 تصفح أفرع العائلة:</h3>", unsafe_allow_html=True)

root_row = df[df['Parent_ID'] == '']
if not root_row.empty:
    root_id = root_row['ID'].iloc[0]
    
    # بطاقة الجد الأكبر الرئيسية التي تحضن القائمة بالكامل بكفاءة وثبات
    with st.expander("👑 عبد العزيز نعمان الكردي رحمه الله", expanded=True):
        display_accordion_tree(root_id, df)
else:
    st.error("تأكد من وجود بيانات الجد الأكبر في ملف الإكسل.")