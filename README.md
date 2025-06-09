# AVI Load Balancer Controller - Tenant Creation Script

This project demonstrates two ways to interact with the VMware AVI Load Balancer Controller API:
1. Using Python script (automated approach)
2. Using Postman (manual testing approach)

## Prerequisites

- Python 3.x
- Required Python packages:
  - requests
  - urllib3
- Postman (for manual API testing)

## Installation

1. Clone this repository or download the script

```
2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Install Postman:
   - Download from: https://www.postman.com/downloads/
   - Create a free account if you don't have one

## Configuration

The script uses the following configuration:
- AVI Controller URL: https://35.200.176.139
- Username: hiring-2
- Password: hiring-2
- Available Time Window: 7 PM to 11 PM

## Using Postman

1. **Create a new request in Postman:**
   - Method: POST
   - URL: https://35.200.176.139/api/tenant
   - Headers:
     ```
     Content-Type: application/json
     X-Avi-Version: 20.1.1
     ```

2. **Authentication:**
   - First, make a POST request to: https://35.200.176.139/login
   - Body (raw JSON):
     ```json
     {
         "username": "hiring-2",
         "password": "hiring-2"
     }
     ```
   - Save the session cookie from the response

3. **Create Tenant:**
   - Use the saved session cookie
   - Body (raw JSON):
     ```json
     {
         "name": "Your_Tenant_Name",
         "description": "Tenant created via Postman",
         "local": true
     }
     ```

## Using Python Script

The Python script automates the same process that you can do manually in Postman.

### Code Structure

### 1. Imports and Setup
```python
import requests
import json
import urllib3
from datetime import datetime
```
- `requests`: For making HTTP requests (equivalent to Postman requests)
- `json`: For handling JSON data
- `urllib3`: For SSL warning suppression
- `datetime`: For time window checking

### 2. Constants
```python
AVI_CONTROLLER = "https://35.200.176.139"
USERNAME = "hiring-2"
PASSWORD = "hiring-2"
```

### 3. Main Function: create_tenant(tenant_name)
The main function handles:
- Time window validation
- Authentication (equivalent to Postman login)
- Tenant existence check
- Tenant creation (equivalent to Postman POST request)

## How It Works

1. **Time Check**
   - Verifies if current time is between 7 PM and 11 PM
   - Exits if outside the allowed time window

2. **Authentication**
   - Logs in to the AVI Controller (same as Postman login)
   - Obtains session cookie and CSRF token
   - Handles authentication errors

3. **Tenant Check**
   - Checks if tenant already exists
   - Shows UUID if tenant exists
   - Proceeds with creation if tenant doesn't exist

4. **Tenant Creation**
   - Creates new tenant with specified name
   - Includes description and configuration
   - Handles creation errors

## Usage

### Using Postman
1. Open Postman
2. Create the login request
3. Create the tenant creation request
4. Execute the requests in sequence

### Using Python Script
1. Make sure your virtual environment is activated:
```bash
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

2. Open the script and modify the tenant name:
```python
if __name__ == "__main__":
    tenant_name = "Your_Tenant_Name"  # Change this to your desired tenant name
    create_tenant(tenant_name)
```

3. Run the script:
```bash
python3 create_tenant.py
```

4. When done, you can deactivate the virtual environment:
```bash
deactivate
```

## Expected Outputs

### Successful Creation
```
Successfully created tenant: Your_Tenant_Name
Response: {
    '_last_modified': '...',
    'config_settings': {...},
    'description': '...',
    'name': 'Your_Tenant_Name',
    'url': '...',
    'uuid': '...'
}
```

### Existing Tenant
```
Tenant 'Your_Tenant_Name' already exists with UUID: tenant-xxxx-xxxx-xxxx-xxxx
```

### Time Window Error
```
Error: The AVI Load Balancer Controller is only available between 7 PM and 11 PM.
```

## Error Handling

The script handles various error scenarios:
- Connection timeouts
- Authentication failures
- Network issues
- API errors
- Time window violations

## Security Features

1. SSL verification disabled for self-signed certificates
2. Session-based authentication
3. CSRF token protection
4. Proper error handling and logging

## Best Practices

1. Always use a virtual environment for Python projects
2. Always check the time window before running
3. Use meaningful tenant names
4. Handle the script's output appropriately
5. Keep credentials secure
6. Test API endpoints in Postman before implementing in Python

## Limitations

1. Only works between 7 PM and 11 PM
2. Requires Python 3.x
3. Needs internet connectivity to the AVI Controller
4. Requires valid credentials

## Contributing

Feel free to submit issues and enhancement requests!

## Author

Arbaaz Khan

## License

This project is licensed under the MIT License - see the LICENSE file for details. 