import requests
import json
import urllib3
from datetime import datetime

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# AVI Load Balancer Controller details
AVI_CONTROLLER = "https://35.200.176.139"
USERNAME = "hiring-2"
PASSWORD = "hiring-2"

def create_tenant(tenant_name):
    """Create a new tenant with the given name"""
    # Check time window
    current_hour = datetime.now().hour
    if not (19 <= current_hour < 23):
        print("Error: The AVI Load Balancer Controller is only available between 7 PM and 11 PM.")
        return

    # Login to get session cookie and CSRF token
    login_url = f"{AVI_CONTROLLER}/login"
    login_data = {"username": USERNAME, "password": PASSWORD}
    headers = {"Content-Type": "application/json", "X-Avi-Version": "20.1.1"}
    
    try:
        # Get session cookie and CSRF token
        response = requests.post(login_url, headers=headers, json=login_data, verify=False, timeout=10)
        if response.status_code != 200:
            print(f"Login failed. Status code: {response.status_code}")
            return
        
        cookies = response.cookies.get_dict()
        csrf_token = cookies.get('csrftoken')
        
        # Check if tenant exists
        tenant_url = f"{AVI_CONTROLLER}/api/tenant"
        headers.update({
            "Referer": AVI_CONTROLLER,
            "X-CSRFToken": csrf_token
        })
        
        # Get list of tenants
        response = requests.get(tenant_url, headers=headers, cookies=cookies, verify=False, timeout=10)
        if response.status_code == 200:
            tenants = response.json().get('results', [])
            for tenant in tenants:
                if tenant.get('name') == tenant_name:
                    print(f"Tenant '{tenant_name}' already exists with UUID: {tenant.get('uuid')}")
                    return
        
        # Create tenant if it doesn't exist
        tenant_data = {
            "name": tenant_name,
            "description": f"Tenant created for {tenant_name}",
            "local": True
        }
        
        response = requests.post(
            tenant_url,
            headers=headers,
            cookies=cookies,
            json=tenant_data,
            verify=False,
            timeout=10
        )
        
        if response.status_code == 201:
            print(f"Successfully created tenant: {tenant_name}")
            print("Response:", response.json())
        else:
            print(f"Failed to create tenant. Status code: {response.status_code}")
            print("Response:", response.text)
            
    except requests.exceptions.Timeout:
        print("Error: Connection timed out. Please check if the AVI Load Balancer Controller is accessible.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the AVI Load Balancer Controller. Please check your network connection.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_tenant_uuid(tenant_name, session_cookie, csrf_token):
    """Get the UUID of a tenant by name"""
    url = f"{AVI_CONTROLLER}/api/tenant"
    headers = {
        "Content-Type": "application/json",
        "X-Avi-Version": "20.1.1",
        "Referer": AVI_CONTROLLER
    }
    if csrf_token:
        headers['X-CSRFToken'] = csrf_token
    
    try:
        response = requests.get(
            url,
            headers=headers,
            cookies=session_cookie,
            verify=False,
            timeout=10
        )
        if response.status_code == 200:
            tenants = response.json().get('results', [])
            for tenant in tenants:
                if tenant.get('name') == tenant_name:
                    return tenant.get('uuid')
        print(f"Tenant '{tenant_name}' not found.")
        return None
    except Exception as e:
        print(f"Error retrieving tenant UUID: {str(e)}")
        return None

def update_tenant(tenant_name, new_description):
    if not check_time():
        return

    # Authenticate and get session cookie and CSRF token
    session_cookie, csrf_token = get_session_cookie_and_csrf()
    if not session_cookie:
        print("Could not authenticate. Exiting.")
        return

    # Get tenant UUID
    tenant_uuid = get_tenant_uuid(tenant_name, session_cookie, csrf_token)
    if not tenant_uuid:
        return

    # API endpoint for tenant update
    url = f"{AVI_CONTROLLER}/api/tenant/{tenant_uuid}"
    
    # Tenant update data
    tenant_data = {
        "name": tenant_name,
        "description": new_description
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "X-Avi-Version": "20.1.1",
        "Referer": AVI_CONTROLLER
    }
    if csrf_token:
        headers['X-CSRFToken'] = csrf_token
    
    try:
        # Make the PUT request with a timeout of 10 seconds and session cookie
        response = requests.put(
            url,
            headers=headers,
            cookies=session_cookie,
            data=json.dumps(tenant_data),
            verify=False,
            timeout=10
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            print(f"Successfully updated tenant: {tenant_name}")
            print("Response:", response.json())
        else:
            print(f"Failed to update tenant. Status code: {response.status_code}")
            print("Response:", response.text)
            
    except requests.exceptions.Timeout:
        print("Error: Connection timed out. Please check if the AVI Load Balancer Controller is accessible.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the AVI Load Balancer Controller. Please check your network connection.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def delete_tenant(tenant_name):
    """Delete an existing tenant"""
    if not check_time():
        return

    # Authenticate and get session cookie and CSRF token
    session_cookie, csrf_token = get_session_cookie_and_csrf()
    if not session_cookie:
        print("Could not authenticate. Exiting.")
        return

    # Get tenant UUID
    tenant_uuid = get_tenant_uuid(tenant_name, session_cookie, csrf_token)
    if not tenant_uuid:
        return

    # API endpoint for tenant deletion
    url = f"{AVI_CONTROLLER}/api/tenant/{tenant_uuid}"
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "X-Avi-Version": "20.1.1",
        "Referer": AVI_CONTROLLER
    }
    if csrf_token:
        headers['X-CSRFToken'] = csrf_token
    
    try:
        # Make the DELETE request
        response = requests.delete(
            url,
            headers=headers,
            cookies=session_cookie,
            verify=False,
            timeout=10
        )
        
        # Check if the request was successful
        if response.status_code == 204:
            print(f"Successfully deleted tenant: {tenant_name}")
        else:
            print(f"Failed to delete tenant. Status code: {response.status_code}")
            print("Response:", response.text)
            
    except requests.exceptions.Timeout:
        print("Error: Connection timed out. Please check if the AVI Load Balancer Controller is accessible.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the AVI Load Balancer Controller. Please check your network connection.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # You can change this name to any name you want
    tenant_name = "Arbaaz_king"  # Change this to any name you want
    create_tenant(tenant_name) 