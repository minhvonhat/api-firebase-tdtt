import streamlit as st
import api_client

st.set_page_config(page_title="Minke - Gợi ý quán ăn", layout="wide")

st.title("🍴 Minke Chatbot")

# Khởi tạo các biến session state cần thiết
if "id_token" not in st.session_state:
    st.session_state.id_token = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Màn hình đăng nhập / đăng ký
if not st.session_state.id_token:
    st.subheader("Vui lòng đăng nhập để sử dụng Chatbot")
    tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký"])
    
    with tab1:
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Mật khẩu", type="password", key="login_pass")
        if st.button("Đăng nhập"):
            try:
                # Gọi API backend để đăng nhập
                res = api_client.login(login_email, login_password)
                st.session_state.id_token = res.get("id_token") # Lưu token lại
                st.success("Đăng nhập thành công!")
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi đăng nhập: {e}")

    with tab2:
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Mật khẩu", type="password", key="signup_pass")
        if st.button("Đăng ký"):
            try:
                res = api_client.signup(signup_email, signup_password)
                st.success("Đăng ký thành công! Vui lòng chuyển sang tab Đăng nhập.")
            except Exception as e:
                st.error(f"Lỗi đăng ký: {e}")

# Màn hình Chat chính
else:
    st.sidebar.write("Đã đăng nhập")
    if st.sidebar.button("Đăng xuất"):
        st.session_state.id_token = None
        st.session_state.messages = []
        st.rerun()

    st.sidebar.divider()
    st.sidebar.subheader("Lịch sử trò chuyện")

    # Tải lịch sử chat từ Backend
    try:
        res_history = api_client.get_chat_history(st.session_state.id_token)
        db_history = res_history.get("data", [])

        # Đồng bộ lịch sử vào màn hình chính nếu session đang trống (vừa đăng nhập)
        if not st.session_state.messages and db_history:
            # DB đang trả về tin mới nhất trước (desc), cần đảo ngược lại để hiển thị đúng thứ tự thời gian
            for item in reversed(db_history):
                st.session_state.messages.append({"role": "user", "content": item["message"]})
                st.session_state.messages.append({"role": "assistant", "content": item["response"]})
        
        # Hiển thị tóm tắt lịch sử bên thanh sidebar
        if db_history:
            for item in db_history:
                short_msg = item["message"][:25] + "..." if len(item["message"]) > 25 else item["message"]
                st.sidebar.caption(f"👤 {short_msg}")
        else:
            st.sidebar.info("Chưa có trò chuyện nào.")
    except Exception as e:
        st.sidebar.error("Không thể tải lịch sử chat.")
    
    # Hiển thị lịch sử chat từ session
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Khung nhập tin nhắn mới
    if prompt := st.chat_input("Bạn muốn ăn gì hôm nay?"):
        # 1. Hiển thị tin nhắn người dùng ngay lập tức
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # 2. Hiển thị phản hồi từ Bot
        with st.chat_message("assistant"):
            with st.spinner("Minke đang suy nghĩ..."):
                try:
                    # Gọi API backend để lấy câu trả lời từ AI
                    res = api_client.send_chat(st.session_state.id_token, prompt)
                    reply = res.get("reply", "Lỗi: Không nhận được phản hồi hợp lệ.")
                except Exception as e:
                    reply = f"Rất tiếc, đã có lỗi xảy ra khi kết nối tới Minke. Chi tiết: {e}"
            
            # Hiển thị và lưu lại câu trả lời của bot
            st.markdown(reply, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": reply})