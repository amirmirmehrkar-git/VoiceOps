"""
Demo endpoint for viewing incident JSON output
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from api.incident import create_incident_from_transcript

router = APIRouter()

@router.get("/demo", response_class=HTMLResponse)
async def demo_page():
    """Demo page showing incident JSON output."""
    # Create a sample incident
    transcript = "از ساعت ۱۸:۰۵ بعد از دیپلوی جدید، checkout-api توی پروداکشن ۵۰۰ می‌دهد. مشتری‌ها نمی‌تونن پرداخت کنن."
    
    try:
        incident = create_incident_from_transcript(
            transcript=transcript,
            call_id="demo_001",
            timezone="Europe/Berlin"
        )
        
        import json
        json_output = json.dumps(incident, indent=2, ensure_ascii=False)
    except Exception as e:
        json_output = f"Error: {str(e)}"
    
    html = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VoiceOps MVP - Demo Output</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }}
            .container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #6366f1;
                border-bottom: 3px solid #6366f1;
                padding-bottom: 10px;
            }}
            .transcript {{
                background: #f9fafb;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
                border-right: 4px solid #6366f1;
            }}
            .json-output {{
                background: #1e293b;
                color: #e2e8f0;
                padding: 20px;
                border-radius: 5px;
                overflow-x: auto;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                line-height: 1.6;
            }}
            .key-fields {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }}
            .field-card {{
                background: #f0f9ff;
                padding: 15px;
                border-radius: 5px;
                border-right: 3px solid #6366f1;
            }}
            .field-label {{
                font-weight: bold;
                color: #64748b;
                font-size: 12px;
                text-transform: uppercase;
            }}
            .field-value {{
                color: #1e293b;
                font-size: 18px;
                margin-top: 5px;
            }}
            .status-badge {{
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
            }}
            .sev1 {{ background: #fee2e2; color: #991b1b; }}
            .sev2 {{ background: #fef3c7; color: #92400e; }}
            .sev3 {{ background: #dbeafe; color: #1e40af; }}
            .sev4 {{ background: #f3f4f6; color: #374151; }}
            .success {{
                background: #d1fae5;
                color: #065f46;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            a {{
                color: #6366f1;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎤 VoiceOps MVP - Demo Output</h1>
            
            <div class="success">
                ✅ Incident created successfully! Schema validation passed!
            </div>
            
            <h2>📝 Transcript (Input)</h2>
            <div class="transcript">
                {transcript}
            </div>
            
            <h2>📊 Key Fields</h2>
            <div class="key-fields">
                <div class="field-card">
                    <div class="field-label">Category</div>
                    <div class="field-value">{incident.get('category', 'N/A') if 'incident' in locals() else 'N/A'}</div>
                </div>
                <div class="field-card">
                    <div class="field-label">Severity</div>
                    <div class="field-value">
                        <span class="status-badge sev{incident.get('severity', 'sev3')[-1] if 'incident' in locals() else '3'}">
                            {incident.get('severity', 'N/A') if 'incident' in locals() else 'N/A'}
                        </span>
                    </div>
                </div>
                <div class="field-card">
                    <div class="field-label">Status</div>
                    <div class="field-value">{incident.get('status', 'N/A') if 'incident' in locals() else 'N/A'}</div>
                </div>
                <div class="field-card">
                    <div class="field-label">Confidence</div>
                    <div class="field-value">{incident.get('confidence', 'N/A') if 'incident' in locals() else 'N/A'}</div>
                </div>
            </div>
            
            <h2>📄 JSON Output</h2>
            <div class="json-output">
                <pre>{json_output}</pre>
            </div>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #e5e7eb;">
                <p>
                    <a href="/docs">📚 API Documentation (Swagger)</a> | 
                    <a href="/health">❤️ Health Check</a> |
                    <a href="/">🏠 Home</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

