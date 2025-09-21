import streamlit as st
import pyrebase
from requests.exceptions import HTTPError
import json

@st.cache_resource
def initialize_firebase_app():
    """
    Khởi tạo và cache kết nối tới Firebase.
    """
    try:
        # Chuyển đổi secrets thành dict để tương thích với pyrebase
        firebase_config = dict(st.secrets.firebase)
        firebase = pyrebase.initialize_app(firebase_config)
        return firebase
    except Exception as e:
        st.error("Lỗi khi khởi tạo Firebase. Vui lòng kiểm tra lại file secrets.")
        st.exception(e)
        return None

def display_auth_forms(auth, db):
    """
    Hiển thị các form đăng nhập/đăng ký trong sidebar và xử lý lỗi chi tiết.
    Trả về True nếu người dùng đã đăng nhập.
    """
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None

    if st.session_state.user_info:
        user_email = st.session_state.user_info['email']
        st.success(f"Chào mừng, {user_email}")
        if st.button("Đăng xuất"):
            # Giữ lại các biến của firebase, xóa các biến người dùng
            for key in list(st.session_state.keys()):
                if key not in ['firebase_app', 'firebase_auth', 'firebase_db']:
                    del st.session_state[key]
            st.rerun()
    else:
        choice = st.selectbox("Đăng nhập / Đăng ký", ["Tiếp tục với tư cách khách", "Đăng nhập", "Đăng ký"])
        
        if choice == "Đăng nhập":
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Mật khẩu", type="password")
                if st.form_submit_button("Đăng nhập"):
                    try:
                        user = auth.sign_in_with_email_and_password(email, password)
                        st.session_state.user_info = user
                        st.rerun()
                    except HTTPError as e:
                        # Phân tích lỗi cụ thể hơn cho việc đăng nhập
                        error_json = e.response.json()
                        error_message = error_json.get("error", {}).get("message", "UNKNOWN_ERROR")
                        if "INVALID_LOGIN_CREDENTIALS" in error_message:
                            st.error("Email hoặc mật khẩu không chính xác.")
                        else:
                            st.error("Đã có lỗi xảy ra. Vui lòng thử lại.")

        elif choice == "Đăng ký":
            with st.form("register_form"):
                email = st.text_input("Email")
                password = st.text_input("Mật khẩu", type="password")
                if st.form_submit_button("Đăng ký"):
                    try:
                        user = auth.create_user_with_email_and_password(email, password)
                        st.sidebar.success("Đăng ký thành công! Đang khởi tạo dữ liệu...")
                        
                        user_id = user['localId']
                        token = user['idToken']
                        
                        # Dữ liệu mặc định cho người dùng mới
                        default_data = {
                            "history": [], 
                            "collections": {}, 
                            "is_pro": False, 
                            "usage_counters": {"prescription_analysis": 0}
                        }
                        db.child("user_data").child(user_id).set(default_data, token=token)
                        
                        st.info("Tuyệt vời! Vui lòng chuyển qua tab 'Đăng nhập' để bắt đầu.")
                        
                    except HTTPError as e:
                        # --- PHẦN NÂNG CẤP XỬ LÝ LỖI CHI TIẾT ---
                        try:
                            error_json = e.response.json()
                            error_message = error_json.get("error", {}).get("message", "UNKNOWN_ERROR")
                            
                            if "EMAIL_EXISTS" in error_message:
                                st.sidebar.error("Lỗi: Email này đã được đăng ký. Vui lòng sử dụng email khác hoặc đăng nhập.")
                            elif "WEAK_PASSWORD" in error_message:
                                st.sidebar.error("Lỗi: Mật khẩu phải có ít nhất 6 ký tự.")
                            elif "INVALID_EMAIL" in error_message:
                                st.sidebar.error("Lỗi: Định dạng email không hợp lệ.")
                            else:
                                # Lỗi chung khác từ Firebase
                                st.sidebar.error("Đã có lỗi xảy ra từ máy chủ. Vui lòng thử lại.")
                        except json.JSONDecodeError:
                            # Lỗi không thể phân tích phản hồi từ Firebase
                             st.sidebar.error("Lỗi kết nối. Vui lòng kiểm tra lại mạng và thử lại.")
                    except Exception as e:
                        # Các lỗi không mong muốn khác
                        st.sidebar.error(f"Đã xảy ra lỗi không xác định: {e}")

    return st.session_state.user_info is not None
