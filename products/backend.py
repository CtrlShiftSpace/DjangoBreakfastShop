from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(object):
    """
    身份驗證後端，允許使用用戶名或電子郵件地址進行登入。
    """

    def authenticate(self, request, username=None, password=None):
        User = get_user_model()

        # 檢查用戶名或電子郵件地址是否為空
        if username is None or password is None:
            return None

        # 嘗試通過用戶名進行身份驗證
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 如果找不到用戶名，則嘗試通過電子郵件地址進行身份驗證
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None

        # 驗證用戶密碼
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None