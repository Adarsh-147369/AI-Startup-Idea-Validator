import json
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


PROMPT_TEMPLATE = """You are an expert startup validator and business analyst. Analyze the following startup idea and provide a comprehensive validation report.

Startup Idea:
- Name: {idea_name}
- Description: {idea_description}

Based on this startup idea, provide a detailed analysis in the following JSON format exactly:
{{
    "problem": "<Clear problem statement this startup solves>",
    "customer": "<Target customer segment and demographics>",
    "market": "<Market size, opportunity, and growth potential>",
    "competitors": ["<competitor 1>", "<competitor 2>", "<competitor 3>"],
    "tech_stack": ["<technology 1>", "<technology 2>", "<technology 3>"],
    "risk_level": "<Low/Medium/High>",
    "profitability_score": <score between 0-100>,
    "strengths": ["<strength 1>", "<strength 2>"],
    "weaknesses": ["<weakness 1>", "<weakness 2>"],
    "recommendations": ["<recommendation 1>", "<recommendation 2>"],
    "overall_analysis": "<2-3 sentence comprehensive analysis>"
}}

Important:
- Be specific and realistic in your analysis
- Provide actual competitor names if they exist
- Suggest appropriate modern tech stack
- Risk level should be Low, Medium, or High
- Profitability score should reflect realistic market potential

Provide only the JSON output, no additional text."""


def validate_idea(idea_data: dict) -> dict:
    """
    Validate a startup idea using OpenRouter API.
    
    Args:
        idea_data: Dictionary containing idea_name and idea_description
        
    Returns:
        Dictionary containing all analysis fields
    """
    prompt = PROMPT_TEMPLATE.format(
        idea_name=idea_data.get("idea_name", ""),
        idea_description=idea_data.get("idea_description", "")
    )
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://startup-idea-validator.example.com",
        "X-Title": "AI Startup Idea Validator"
    }
    
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                OPENROUTER_API_URL,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Parse JSON from the response
            analysis = json.loads(content)
            
            return {
                "problem": analysis.get("problem", ""),
                "customer": analysis.get("customer", ""),
                "market": analysis.get("market", ""),
                "competitors": analysis.get("competitors", []),
                "tech_stack": analysis.get("tech_stack", []),
                "risk_level": analysis.get("risk_level", "Medium"),
                "profitability_score": analysis.get("profitability_score", 0),
                "ai_analysis": json.dumps({
                    "strengths": analysis.get("strengths", []),
                    "weaknesses": analysis.get("weaknesses", []),
                    "recommendations": analysis.get("recommendations", []),
                    "overall_analysis": analysis.get("overall_analysis", "")
                }, indent=2)
            }
    except Exception as e:
        print(f"Error validating idea: {str(e)}")
        return {
            "problem": "Unable to analyze",
            "customer": "Unable to analyze",
            "market": "Unable to analyze",
            "competitors": [],
            "tech_stack": [],
            "risk_level": "Unknown",
            "profitability_score": 0,
            "ai_analysis": json.dumps({
                "error": str(e),
                "strengths": [],
                "weaknesses": [],
                "recommendations": [],
                "overall_analysis": "Unable to generate analysis due to API error."
            }, indent=2)
        }
