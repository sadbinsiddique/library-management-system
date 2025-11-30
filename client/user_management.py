import requests

class UserManagementClient:
    def __init__(self, base_url, timeout=5):
        self.base_url = base_url
        self.timeout = timeout

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        kwargs.setdefault('timeout', self.timeout)
        
        try:
            resp = requests.request(method, url, **kwargs)
            resp.raise_for_status()
            return None if resp.status_code == 204 else resp.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")

    def add_user(self, username, full_name, email):
        return self._request(
            'POST',
            '/', 
            json={
                'username': username, 
                'full_name': full_name, 
                'email': email
        })

    def get_user(self, user_id):
        return self._request(
            'GET', 
            f'/{user_id}'
        )

    def update_user(self, user_id, **fields):
        update_data = {k: v for k, v in fields.items() if v is not None}
        
        return self._request(
            'PUT', 
            f'/{user_id}',
            json = update_data
        )

    def delete_user(self, user_id):
        self._request(
            'DELETE', 
            f'/{user_id}'
        )

    def list_users(self):
        return self._request(
            'GET',
            '/'
        )

def print_user(user, user_id=None):
    print("\n--- User Info ---")
    if user_id: 
        print(f"ID: {user_id}")

    print(f"Username: {user.get('username')}")
    print(f"Full Name: {user.get('full_name')}")
    print(f"Email: {user.get('email')}\n")