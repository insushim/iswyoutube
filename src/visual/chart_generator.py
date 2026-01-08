"""
Chart Generator Module
======================
Generate charts and graphs
"""

from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Chart:
    """차트"""
    path: str
    chart_type: str
    data: Dict


class ChartGenerator:
    """차트 생성기"""

    CHART_TYPES = ["bar", "line", "pie", "area", "scatter", "heatmap"]

    def __init__(self, config: Dict):
        self.config = config

    async def create(
        self,
        data: Dict,
        chart_type: str,
        title: str = None,
        output_path: str = None
    ) -> Chart:
        """
        차트 생성

        Args:
            data: 차트 데이터
            chart_type: 차트 유형
            title: 제목
            output_path: 출력 경로

        Returns:
            생성된 차트
        """
        if not output_path:
            output_path = f"output/charts/{chart_type}.png"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        library = self.config.get('visual', {}).get('infographic', {}).get('chart_library', 'matplotlib')

        if library == 'plotly':
            return await self._create_plotly(data, chart_type, title, output_path)
        else:
            return await self._create_matplotlib(data, chart_type, title, output_path)

    async def _create_matplotlib(
        self,
        data: Dict,
        chart_type: str,
        title: str,
        output_path: str
    ) -> Chart:
        """Matplotlib 차트"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')

            fig, ax = plt.subplots(figsize=(19.2, 10.8))

            # 스타일 설정
            fig.patch.set_facecolor('#1A1A2E')
            ax.set_facecolor('#1A1A2E')

            labels = data.get('labels', [])
            values = data.get('values', [])
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

            if chart_type == 'bar':
                ax.bar(labels, values, color=colors[:len(labels)])
            elif chart_type == 'line':
                ax.plot(labels, values, color='#FF6B6B', linewidth=3, marker='o')
                ax.fill_between(labels, values, alpha=0.3, color='#FF6B6B')
            elif chart_type == 'pie':
                ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%')
            elif chart_type == 'area':
                ax.fill_between(range(len(values)), values, alpha=0.7, color='#4ECDC4')
                ax.plot(values, color='#4ECDC4', linewidth=2)

            if title:
                ax.set_title(title, color='white', fontsize=28, pad=20)

            ax.tick_params(colors='white', labelsize=14)
            for spine in ax.spines.values():
                spine.set_color('white')

            plt.tight_layout()
            plt.savefig(output_path, dpi=100, facecolor='#1A1A2E')
            plt.close()

            return Chart(
                path=output_path,
                chart_type=chart_type,
                data=data
            )
        except ImportError:
            raise RuntimeError("matplotlib not installed")

    async def _create_plotly(
        self,
        data: Dict,
        chart_type: str,
        title: str,
        output_path: str
    ) -> Chart:
        """Plotly 차트"""
        try:
            import plotly.graph_objects as go
            import plotly.io as pio

            fig = go.Figure()

            labels = data.get('labels', [])
            values = data.get('values', [])

            if chart_type == 'bar':
                fig.add_trace(go.Bar(x=labels, y=values, marker_color='#FF6B6B'))
            elif chart_type == 'line':
                fig.add_trace(go.Scatter(x=labels, y=values, mode='lines+markers', line=dict(color='#FF6B6B')))
            elif chart_type == 'pie':
                fig.add_trace(go.Pie(labels=labels, values=values))

            fig.update_layout(
                title=title,
                paper_bgcolor='#1A1A2E',
                plot_bgcolor='#1A1A2E',
                font=dict(color='white'),
                width=1920,
                height=1080
            )

            pio.write_image(fig, output_path)

            return Chart(
                path=output_path,
                chart_type=chart_type,
                data=data
            )
        except ImportError:
            raise RuntimeError("plotly not installed")
