# 🧞 Granter Genie - AI-Powered Grant and Funding Finder

An intelligent web application that helps startups and businesses discover grants, funding opportunities, and accelerator programs using IBM watsonx.ai Granite models.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![IBM watsonx.ai](https://img.shields.io/badge/IBM-watsonx.ai-purple.svg)

## ✨ Features

### 🤖 AI-Powered Features
- **Intelligent Chat Assistant**: Conversational AI powered by IBM Granite models
- **Personalized Recommendations**: Tailored grant suggestions based on startup profile
- **Eligibility Analysis**: AI-driven eligibility checking with detailed insights
- **Proposal Generation**: Automated grant proposal content generation
- **Document Analysis**: Smart analysis of grant requirements

### 📊 Core Features
- **Comprehensive Grant Database**: 150+ grants and funding opportunities
- **Advanced Search & Filters**: Search by type, industry, location, and stage
- **Application Tracker**: Track deadlines and application progress
- **Startup Profile Management**: Maintain detailed company information
- **Dark Mode**: Eye-friendly dark theme support
- **Mobile Responsive**: Works seamlessly on all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- IBM Cloud account with watsonx.ai access
- pip (Python package manager)

### Installation

1. **Navigate to project directory**
```bash
cd granter-genie
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
copy .env.template .env  # Windows
cp .env.template .env    # macOS/Linux
```

5. **Add IBM Cloud credentials to .env**
```env
IBM_CLOUD_API_KEY=your_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

Get credentials from:
- API Key: https://cloud.ibm.com/iam/apikeys
- Project ID: https://dataplatform.cloud.ibm.com/wx/home

6. **Run the application**
```bash
python app.py
```

7. **Open browser**
```
http://localhost:5000
```

## 📁 Project Structure

```
granter-genie/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.template              # Environment template
├── README.md                  # Documentation
├── data/
│   └── grants_database.json   # Grants database
├── templates/                 # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── chat.html
│   ├── search.html
│   ├── recommendations.html
│   ├── eligibility.html
│   ├── tracker.html
│   └── profile.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## 🎨 Customizing AI Agent

Edit `AGENT_INSTRUCTIONS` in `app.py`:

```python
AGENT_INSTRUCTIONS = {
    "system_role": "Your custom role...",
    "response_tone": "professional, encouraging",
    "funding_specialization": [...],
    "startup_domains": [...],
    "regional_preferences": {...}
}
```

## 🌐 API Endpoints

- `POST /api/chat` - Chat with AI assistant
- `POST /api/recommendations` - Get grant recommendations
- `POST /api/eligibility` - Check eligibility
- `POST /api/generate-proposal` - Generate proposal
- `POST /api/search-grants` - Search grants
- `POST /api/save-profile` - Save startup profile
- `GET /api/get-profile` - Get startup profile
- `GET /api/deadlines` - Get upcoming deadlines

## 🔧 Configuration

### Change AI Model
```python
MODEL_ID = "ibm/granite-13b-chat-v2"
```

### Adjust Parameters
```python
GENERATION_PARAMS = {
    GenParams.MAX_NEW_TOKENS: 1500,
    GenParams.TEMPERATURE: 0.7,
    GenParams.TOP_K: 50
}
```

## 📊 Sample Data

Includes 15 sample grants:
- Government Grants (India)
- Government Loans
- Accelerator Programs
- International Grants

Expand by editing `data/grants_database.json`

## 🎯 Usage Examples

### 1. Chat with AI
Navigate to `/chat` and ask questions like:
- "What grants are available for tech startups in India?"
- "Help me write a grant proposal"
- "What documents do I need for SISFS?"

### 2. Get Recommendations
1. Go to `/recommendations`
2. Fill in your startup profile
3. Click "Get AI Recommendations"
4. Review personalized suggestions

### 3. Check Eligibility
1. Visit `/eligibility`
2. Enter startup details
3. Select a grant
4. Get AI-powered eligibility analysis

### 4. Track Applications
1. Go to `/tracker`
2. Add grant applications
3. Monitor deadlines and status
4. Get reminders

## 🛠️ Troubleshooting

### API Key Issues
- Verify API key is correct in `.env`
- Check IBM Cloud account has watsonx.ai access
- Ensure Project ID is from correct workspace

### Module Import Errors
```bash
pip install --upgrade -r requirements.txt
```

### Port Already in Use
Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 📝 License

MIT License - feel free to use for your projects!

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues or questions:
- Check the troubleshooting section
- Review IBM watsonx.ai documentation
- Open an issue on GitHub

## 🙏 Acknowledgments

- Built with IBM watsonx.ai and Granite models
- Powered by Flask and Bootstrap
- Icons by Bootstrap Icons

---

**Made with ❤️ for startups seeking funding opportunities**