"""
Granter Genie - AI-Powered Grant and Funding Finder
Built with Flask and IBM watsonx.ai Granite Models
"""

import os
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
import secrets

# Load environment variables
load_dotenv()

print("API KEY:", os.getenv("IBM_CLOUD_API_KEY"))
print("PROJECT ID:", os.getenv("IBM_WATSONX_PROJECT_ID"))
print("URL:", os.getenv("IBM_WATSONX_URL"))

# ============================================================================
# AGENT_INSTRUCTIONS - Customize the AI Agent's Behavior
# ============================================================================
AGENT_INSTRUCTIONS = {
    "system_role": """You are Granter Genie, an expert AI assistant specializing in grant and funding discovery 
    for startups and businesses. You have deep knowledge of government grants, venture capital, angel investors, 
    accelerator programs, and various funding opportunities across India and globally.""",
    
    "response_tone": "professional, encouraging, and actionable",
    
    "funding_specialization": [
        "Government grants (India - DPIIT, MSME, State schemes)",
        "Venture Capital and Angel Investment",
        "Accelerator and Incubator programs",
        "International grants (EU Horizon, US SBIR/STTR)",
        "Corporate innovation challenges",
        "Crowdfunding platforms",
        "Bank loans and financial schemes"
    ],
    
    "startup_domains": [
        "Technology and Software",
        "Healthcare and Biotech",
        "Agriculture and AgriTech",
        "Clean Energy and Sustainability",
        "Education and EdTech",
        "FinTech and Financial Services",
        "E-commerce and Retail",
        "Manufacturing and Industry 4.0",
        "Social Impact and NGOs"
    ],
    
    "eligibility_rules": {
        "startup_stage": {
            "idea": "Pre-seed grants, incubators, government startup schemes",
            "mvp": "Seed funding, accelerators, angel investors",
            "early_revenue": "Series A, venture capital, growth grants",
            "scaling": "Series B+, expansion grants, strategic investors"
        },
        "location_priority": ["India", "Asia-Pacific", "Global"],
        "funding_range": {
            "micro": "< ₹10 lakhs",
            "small": "₹10 lakhs - ₹1 crore",
            "medium": "₹1 crore - ₹10 crores",
            "large": "> ₹10 crores"
        }
    },
    
    "regional_preferences": {
        "primary": "India",
        "secondary": ["Singapore", "UAE", "USA", "UK", "EU"],
        "focus_states_india": ["All Indian States", "Special focus on startup hubs"]
    },
    
    "response_guidelines": [
        "Always provide specific, actionable recommendations",
        "Include eligibility criteria and deadlines",
        "Mention required documents and application process",
        "Suggest 3-5 most relevant opportunities per query",
        "Provide links or contact information when available",
        "Highlight any special advantages or unique features",
        "Warn about common pitfalls or challenges"
    ],
    
    "proposal_generation": {
        "sections": [
            "Executive Summary",
            "Problem Statement",
            "Solution and Innovation",
            "Market Opportunity",
            "Business Model",
            "Team and Expertise",
            "Financial Projections",
            "Use of Funds",
            "Impact and Outcomes"
        ],
        "tone": "compelling, data-driven, and professional",
        "length": "concise but comprehensive"
    }
}

# ============================================================================
# Flask App Configuration
# ============================================================================
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['JSON_SORT_KEYS'] = False

# ============================================================================
# IBM watsonx.ai Configuration
# ============================================================================
IBM_CLOUD_API_KEY = os.getenv('IBM_CLOUD_API_KEY')
IBM_WATSONX_PROJECT_ID = os.getenv('IBM_WATSONX_PROJECT_ID', '')
IBM_WATSONX_URL = os.getenv('IBM_WATSONX_URL', 'https://au-syd.ml.cloud.ibm.com')

# Model parameters
MODEL_ID = "meta-llama/llama-3-3-70b-instruct"

GENERATION_PARAMS = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 1500,
    GenParams.MIN_NEW_TOKENS: 50,
    GenParams.TEMPERATURE: 0.7,
    GenParams.TOP_K: 50,
    GenParams.TOP_P: 1
}

# Initialize watsonx.ai model
def get_watsonx_model():
    """Initialize and return IBM watsonx.ai model"""
    try:
        model = ModelInference(
            model_id=MODEL_ID,
            params=GENERATION_PARAMS,
            credentials={
                "apikey": IBM_CLOUD_API_KEY,
                "url": IBM_WATSONX_URL
            },
            project_id=IBM_WATSONX_PROJECT_ID
        )
        return model
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e
# ============================================================================
# Load Sample Grant Data
# ============================================================================
def load_grants_data():
    """Load grants data from JSON file"""
    try:
        with open('data/grants_database.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"grants": []}

# ============================================================================
# AI Helper Functions
# ============================================================================
def generate_ai_response(prompt, context=""):
    """Generate AI response using IBM watsonx.ai Granite model"""
    model = get_watsonx_model()
    if not model:
        return "AI service is currently unavailable. Please check your IBM Cloud API configuration."
    
    system_prompt = f"""{AGENT_INSTRUCTIONS['system_role']}

Response Guidelines:
{chr(10).join('- ' + guideline for guideline in AGENT_INSTRUCTIONS['response_guidelines'])}

Tone: {AGENT_INSTRUCTIONS['response_tone']}

Context: {context}
"""
    
    full_prompt = f"{system_prompt}\n\nUser Query: {prompt}\n\nResponse:"
    
    try:
        response = model.generate_text(prompt=full_prompt)
        return response
    except Exception as e:
        return f"Error generating response: {str(e)}"

def analyze_eligibility(startup_profile, grant_info):
    """Analyze startup eligibility for a specific grant"""
    prompt = f"""Analyze the eligibility of this startup for the given grant opportunity.

Startup Profile:
- Stage: {startup_profile.get('stage', 'N/A')}
- Industry: {startup_profile.get('industry', 'N/A')}
- Location: {startup_profile.get('location', 'N/A')}
- Funding Needed: {startup_profile.get('funding_needed', 'N/A')}
- Team Size: {startup_profile.get('team_size', 'N/A')}

Grant Information:
- Name: {grant_info.get('name', 'N/A')}
- Type: {grant_info.get('type', 'N/A')}
- Eligibility: {grant_info.get('eligibility', 'N/A')}
- Amount: {grant_info.get('amount', 'N/A')}

Provide:
1. Eligibility Score (0-100)
2. Matching Criteria
3. Missing Requirements
4. Recommendations to improve eligibility
"""
    return generate_ai_response(prompt)

def generate_proposal_draft(startup_profile, grant_info):
    """Generate a proposal draft for a grant application"""
    sections = AGENT_INSTRUCTIONS['proposal_generation']['sections']
    
    prompt = f"""Generate a comprehensive grant proposal draft with the following sections:
{chr(10).join('- ' + section for section in sections)}

Startup Information:
- Name: {startup_profile.get('name', 'N/A')}
- Industry: {startup_profile.get('industry', 'N/A')}
- Stage: {startup_profile.get('stage', 'N/A')}
- Description: {startup_profile.get('description', 'N/A')}

Grant Details:
- Name: {grant_info.get('name', 'N/A')}
- Focus Area: {grant_info.get('focus_area', 'N/A')}
- Amount: {grant_info.get('amount', 'N/A')}

Tone: {AGENT_INSTRUCTIONS['proposal_generation']['tone']}
"""
    return generate_ai_response(prompt)

def get_funding_recommendations(startup_profile):
    """Get personalized funding recommendations"""
    grants_data = load_grants_data()
    
    prompt = f"""Based on this startup profile, recommend the top 5 most suitable funding opportunities from the available grants.

Startup Profile:
- Stage: {startup_profile.get('stage', 'N/A')}
- Industry: {startup_profile.get('industry', 'N/A')}
- Location: {startup_profile.get('location', 'N/A')}
- Funding Needed: {startup_profile.get('funding_needed', 'N/A')}
- Goals: {startup_profile.get('goals', 'N/A')}

Available Grants: {len(grants_data.get('grants', []))} opportunities

For each recommendation, provide:
1. Grant name and type
2. Why it's a good match
3. Eligibility highlights
4. Application deadline
5. Next steps
"""
    return generate_ai_response(prompt, context=json.dumps(grants_data.get('grants', [])[:10]))

# ============================================================================
# Routes
# ============================================================================
@app.route('/')
def index():
    """Home page with dashboard"""
    return render_template('index.html')

@app.route('/chat')
def chat():
    """Chat interface"""
    return render_template('chat.html')

@app.route('/search')
def search():
    """Funding search page"""
    grants_data = load_grants_data()
    return render_template('search.html', grants=grants_data.get('grants', []))

@app.route('/recommendations')
def recommendations():
    """Grant recommendations page"""
    return render_template('recommendations.html')

@app.route('/eligibility')
def eligibility():
    """Eligibility checker page"""
    return render_template('eligibility.html')

@app.route('/tracker')
def tracker():
    """Application tracker page"""
    return render_template('tracker.html')

@app.route('/profile')
def profile():
    """Startup profile management"""
    return render_template('profile.html')

# ============================================================================
# API Endpoints
# ============================================================================
@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Handle chat messages"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = generate_ai_response(user_message)
    
    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/recommendations', methods=['POST'])
def api_recommendations():
    """Get funding recommendations"""
    startup_profile = request.json
    
    recommendations = get_funding_recommendations(startup_profile)
    
    return jsonify({
        'recommendations': recommendations,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/eligibility', methods=['POST'])
def api_eligibility():
    """Check eligibility for a grant"""
    data = request.json
    startup_profile = data.get('startup_profile', {})
    grant_info = data.get('grant_info', {})
    
    analysis = analyze_eligibility(startup_profile, grant_info)
    
    return jsonify({
        'analysis': analysis,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/generate-proposal', methods=['POST'])
def api_generate_proposal():
    """Generate proposal draft"""
    data = request.json
    startup_profile = data.get('startup_profile', {})
    grant_info = data.get('grant_info', {})
    
    proposal = generate_proposal_draft(startup_profile, grant_info)
    
    return jsonify({
        'proposal': proposal,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/search-grants', methods=['POST'])
def api_search_grants():
    """Search grants based on filters"""
    filters = request.json
    grants_data = load_grants_data()
    all_grants = grants_data.get('grants', [])
    
    # Apply filters
    filtered_grants = all_grants
    
    if filters.get('type'):
        filtered_grants = [g for g in filtered_grants if g.get('type') == filters['type']]
    
    if filters.get('industry'):
        filtered_grants = [g for g in filtered_grants if filters['industry'].lower() in g.get('focus_area', '').lower()]
    
    if filters.get('location'):
        filtered_grants = [g for g in filtered_grants if filters['location'].lower() in g.get('location', '').lower()]
    
    return jsonify({
        'grants': filtered_grants,
        'count': len(filtered_grants)
    })

@app.route('/api/save-profile', methods=['POST'])
def api_save_profile():
    """Save startup profile"""
    profile_data = request.json
    session['startup_profile'] = profile_data
    
    return jsonify({
        'success': True,
        'message': 'Profile saved successfully'
    })

@app.route('/api/get-profile', methods=['GET'])
def api_get_profile():
    """Get saved startup profile"""
    profile = session.get('startup_profile', {})
    return jsonify(profile)

@app.route('/api/save-application', methods=['POST'])
def api_save_application():
    """Save grant application tracking"""
    application_data = request.json
    
    if 'applications' not in session:
        session['applications'] = []
    
    session['applications'].append(application_data)
    session.modified = True
    
    return jsonify({
        'success': True,
        'message': 'Application saved successfully'
    })

@app.route('/api/get-applications', methods=['GET'])
def api_get_applications():
    """Get all tracked applications"""
    applications = session.get('applications', [])
    return jsonify({'applications': applications})

@app.route('/api/deadlines', methods=['GET'])
def api_deadlines():
    """Get upcoming deadlines"""
    grants_data = load_grants_data()
    all_grants = grants_data.get('grants', [])
    
    # Filter grants with upcoming deadlines (next 30 days)
    today = datetime.now()
    upcoming = []
    
    for grant in all_grants:
        if grant.get('deadline'):
            try:
                deadline = datetime.strptime(grant['deadline'], '%Y-%m-%d')
                days_left = (deadline - today).days
                if 0 <= days_left <= 30:
                    grant['days_left'] = days_left
                    upcoming.append(grant)
            except:
                pass
    
    upcoming.sort(key=lambda x: x.get('days_left', 999))
    
    return jsonify({'deadlines': upcoming})

# ============================================================================
# Error Handlers
# ============================================================================
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# ============================================================================
# Main
# ============================================================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
