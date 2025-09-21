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
                        try:
                            error_data = json.loads(e.args[1])
                            if isinstance(error_data, dict):
                                error_message = error_data.get("error", {}).get("message", "UNKNOWN_ERROR")
                                if "INVALID_LOGIN_CREDENTIALS" in error_message or "INVALID_EMAIL" in error_message or "INVALID_PASSWORD" in error_message:
                                    st.error("Email hoặc mật khẩu không chính xác.")
                                else:
                                    st.error("Đã có lỗi xảy ra. Vui lòng thử lại.")
                            else:
                                st.error("Lỗi không xác định từ máy chủ. Vui lòng thử lại.")
                        except (json.JSONDecodeError, IndexError):
                            st.error("Lỗi kết nối. Vui lòng kiểm tra mạng và thử lại.")

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
                        
                        default_data = {
                            "history": [], "collections": {}, "is_pro": False, 
                            "usage_counters": {"prescription_analysis": 0}
                        }
                        # Thao tác ghi dữ liệu có thể gây lỗi nếu Rules sai
                        db.child("user_data").child(user_id).set(default_data, token=token)
                        
                        st.info("Tuyệt vời! Vui lòng chuyển qua tab 'Đăng nhập' để bắt đầu.")
                        
                    except HTTPError as e:
                        # --- PHẦN NÂNG CẤP CUỐI CÙNG ---
                        try:
                            error_data = json.loads(e.args[1])
                            
                            # KIỂM TRA XEM LỖI LÀ DICT HAY STRING
                            if isinstance(error_data, dict):
                                error_message = error_data.get("error", {}).get("message", "UNKNOWN_ERROR")
                                
                                if "EMAIL_EXISTS" in error_message:
                                    st.sidebar.error("Lỗi: Email này đã được đăng ký. Vui lòng sử dụng email khác hoặc đăng nhập.")
                                elif "WEAK_PASSWORD" in error_message:
                                    st.sidebar.error("Lỗi: Mật khẩu phải có ít nhất 6 ký tự.")
                                elif "INVALID_EMAIL" in error_message:
                                    st.sidebar.error("Lỗi: Định dạng email không hợp lệ.")
                                else:
                                    st.sidebar.error("Đã có lỗi xảy ra từ máy chủ. Vui lòng thử lại.")
                            
                            elif isinstance(error_data, str):
                                if "Permission denied" in error_data:
                                     st.sidebar.error("Lỗi: Không có quyền ghi dữ liệu. Vui lòng kiểm tra lại Security Rules trên Firebase.")
                                else:
                                     st.sidebar.error(f"Lỗi từ máy chủ: {error_data}")
                            else:
                                st.sidebar.error("Lỗi không xác định từ máy chủ.")

                        except (json.JSONDecodeError, IndexError):
                             st.sidebar.error("Lỗi kết nối. Vui lòng kiểm tra lại mạng và thử lại.")
                    except Exception as e:
                        st.sidebar.error(f"Đã xảy ra lỗi không xác định: {e}")

    return st.session_state.user_info is not None

