# 🚀 Granter Genie - Deployment Guide

Complete step-by-step guide to deploy and run the Granter Genie application.

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [IBM Cloud Setup](#ibm-cloud-setup)
3. [Local Development Setup](#local-development-setup)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Testing](#testing)
7. [Production Deployment](#production-deployment)
8. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

### Required Software
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **pip** - Python package manager (included with Python)
- **Git** (optional) - For version control

### Required Accounts
- **IBM Cloud Account** - [Sign up](https://cloud.ibm.com/registration)
- **watsonx.ai Access** - Available through IBM Cloud

### System Requirements
- **RAM**: Minimum 4GB
- **Storage**: 500MB free space
- **OS**: Windows 10+, macOS 10.14+, or Linux

---

## 2. IBM Cloud Setup

### Step 1: Create IBM Cloud Account
1. Go to https://cloud.ibm.com/registration
2. Sign up with your email
3. Verify your email address
4. Complete account setup

### Step 2: Access watsonx.ai
1. Log in to IBM Cloud
2. Navigate to **Catalog** → **AI/Machine Learning**
3. Select **watsonx.ai**
4. Click **Launch watsonx.ai**

### Step 3: Create a Project
1. In watsonx.ai, click **Projects**
2. Click **New project**
3. Choose **Create an empty project**
4. Enter project name: "Granter Genie"
5. Click **Create**
6. **Copy the Project ID** from the project settings

### Step 4: Generate API Key
1. Go to https://cloud.ibm.com/iam/apikeys
2. Click **Create an IBM Cloud API key**
3. Enter name: "Granter Genie API Key"
4. Click **Create**
5. **Copy and save the API key** (you won't see it again!)

---

## 3. Local Development Setup

### Step 1: Navigate to Project Directory
```bash
cd C:\Users\Meghna\Desktop\granter-genie
```

### Step 2: Create Virtual Environment
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0
- python-dotenv 1.0.0
- ibm-watsonx-ai 0.2.6
- ibm-watson 8.0.0
- Werkzeug 3.0.1

### Step 4: Verify Installation
```bash
python -c "import flask; import ibm_watsonx_ai; print('All packages installed successfully!')"
```

---

## 4. Configuration

### Step 1: Create Environment File
**Windows:**
```bash
copy .env.template .env
```

**macOS/Linux:**
```bash
cp .env.template .env
```

### Step 2: Edit .env File
Open `.env` in a text editor and add your credentials:

```env
# IBM Cloud API Configuration
IBM_CLOUD_API_KEY=your_actual_api_key_here
IBM_WATSONX_PROJECT_ID=your_actual_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here
```

**Important:**
- Replace `your_actual_api_key_here` with your IBM Cloud API key
- Replace `your_actual_project_id_here` with your watsonx.ai Project ID
- Keep the URL as is (unless using a different region)

### Step 3: Verify Configuration
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key:', 'SET' if os.getenv('IBM_CLOUD_API_KEY') else 'NOT SET')"
```

---

## 5. Running the Application

### Start the Application
```bash
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Access the Application
Open your web browser and go to:
```
http://localhost:5000
```

### Stop the Application
Press `Ctrl+C` in the terminal

---

## 6. Testing

### Test the Dashboard
1. Open http://localhost:5000
2. Verify the dashboard loads
3. Check that stats and featured grants appear

### Test AI Chat
1. Navigate to http://localhost:5000/chat
2. Type a message: "What grants are available for tech startups?"
3. Verify AI responds (may take 5-10 seconds)

### Test Grant Search
1. Go to http://localhost:5000/search
2. Verify grants list loads
3. Try filtering by type or industry
4. Click on a grant to view details

### Test Recommendations
1. Navigate to http://localhost:5000/recommendations
2. Fill in the startup profile form
3. Click "Get AI Recommendations"
4. Verify personalized recommendations appear

### Test Eligibility Checker
1. Go to http://localhost:5000/eligibility
2. Fill in startup information
3. Select a grant
4. Click "Check Eligibility"
5. Verify analysis appears

### Test Profile Management
1. Navigate to http://localhost:5000/profile
2. Fill in company information
3. Click "Save Profile"
4. Verify success message appears

### Test Application Tracker
1. Go to http://localhost:5000/tracker
2. Click "Add Application"
3. Fill in application details
4. Click "Save Application"
5. Verify application appears in the list

---

## 7. Production Deployment

### Option 1: Local Production Server

#### Using Gunicorn (Recommended)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Using Waitress (Windows)
```bash
pip install waitress
waitress-serve --port=5000 app:app
```

### Option 2: Cloud Deployment

#### IBM Cloud Foundry
1. Install IBM Cloud CLI
2. Create `manifest.yml`:
```yaml
applications:
- name: granter-genie
  memory: 512M
  instances: 1
  buildpack: python_buildpack
  command: python app.py
```
3. Deploy:
```bash
ibmcloud cf push
```

#### Heroku
1. Install Heroku CLI
2. Create `Procfile`:
```
web: gunicorn app:app
```
3. Deploy:
```bash
heroku create granter-genie
git push heroku main
```

#### Docker
1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```
2. Build and run:
```bash
docker build -t granter-genie .
docker run -p 5000:5000 --env-file .env granter-genie
```

---

## 8. Troubleshooting

### Issue: "Module not found" Error
**Solution:**
```bash
pip install --upgrade -r requirements.txt
```

### Issue: "API Key Invalid" Error
**Solution:**
1. Verify API key in `.env` file
2. Check for extra spaces or quotes
3. Generate a new API key if needed
4. Ensure watsonx.ai access is enabled

### Issue: "Project ID Not Found"
**Solution:**
1. Log in to watsonx.ai
2. Open your project
3. Go to **Manage** → **General**
4. Copy the correct Project ID

### Issue: Port 5000 Already in Use
**Solution:**
Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: AI Responses Not Working
**Solution:**
1. Check internet connection
2. Verify IBM Cloud API key is valid
3. Check watsonx.ai service status
4. Review console for error messages
5. Ensure Project ID is correct

### Issue: Slow AI Responses
**Solution:**
- Normal response time: 5-15 seconds
- Reduce `MAX_NEW_TOKENS` in `app.py` for faster responses
- Check IBM Cloud service region (use closest region)

### Issue: Database Not Loading
**Solution:**
1. Verify `data/grants_database.json` exists
2. Check JSON syntax is valid
3. Ensure file permissions are correct

### Issue: Static Files Not Loading
**Solution:**
1. Clear browser cache
2. Verify `static/` folder structure
3. Check file paths in templates

---

## 📝 Additional Notes

### Customizing the Agent
Edit `AGENT_INSTRUCTIONS` in `app.py` to customize:
- Response tone and style
- Funding specializations
- Regional preferences
- Eligibility rules

### Adding More Grants
Edit `data/grants_database.json` to add new grants:
```json
{
  "id": "grant_016",
  "name": "Your Grant Name",
  "type": "Government Grant",
  "provider": "Provider Name",
  "location": "India",
  "amount": "₹10 lakhs",
  "focus_area": "Technology",
  "stage": ["MVP", "Early Revenue"],
  "eligibility": "Eligibility criteria...",
  "deadline": "2026-12-31",
  "description": "Grant description..."
}
```

### Security Best Practices
1. Never commit `.env` file to version control
2. Use strong SECRET_KEY in production
3. Enable HTTPS in production
4. Regularly rotate API keys
5. Implement rate limiting for production

### Performance Optimization
1. Use caching for grant data
2. Implement pagination for large datasets
3. Optimize database queries
4. Use CDN for static assets
5. Enable gzip compression

---

## 🎉 Success!

Your Granter Genie application should now be running successfully!

For support or questions:
- Check the README.md file
- Review IBM watsonx.ai documentation
- Check application logs for errors

**Happy grant hunting! 🧞✨**