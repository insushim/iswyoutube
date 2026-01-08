"""Dashboard Generator - Generate analytics dashboards"""
from typing import Dict
from pathlib import Path

class DashboardGenerator:
    def __init__(self, config: Dict): self.config = config

    async def generate_html(self, data: Dict, output_path: str = None) -> str:
        if not output_path: output_path = "output/dashboard.html"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        html = f"""<!DOCTYPE html>
<html><head><title>Analytics Dashboard</title>
<style>body{{font-family:sans-serif;background:#1A1A2E;color:white;padding:20px}}
.card{{background:#16213E;padding:20px;margin:10px;border-radius:8px;display:inline-block}}</style></head>
<body><h1>Analytics Dashboard</h1>
<div class="card"><h3>Views</h3><p>{data.get('views', 0)}</p></div>
<div class="card"><h3>Subscribers</h3><p>{data.get('subscribers', 0)}</p></div>
<div class="card"><h3>Watch Time</h3><p>{data.get('watch_time', 0)}h</p></div>
</body></html>"""
        with open(output_path, 'w') as f: f.write(html)
        return output_path

    async def start_server(self, port: int = 8080):
        print(f"Dashboard would be available at http://localhost:{port}")
