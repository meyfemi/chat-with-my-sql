import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, Optional, List, Tuple
import json
import logging

logger = logging.getLogger(__name__)

class VisualizationManager:
    @staticmethod
    def create_visualization(data: str, viz_type: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a visualization based on the data and parameters.
        Returns a dictionary containing the plotly figure and metadata.
        """
        try:
            # Convert string data to DataFrame
            if isinstance(data, str):
                try:
                    # Try parsing as JSON first
                    data = json.loads(data)
                except json.JSONDecodeError:
                    # If not JSON, try parsing as CSV-like string
                    data = pd.read_csv(pd.StringIO(data))
            
            df = pd.DataFrame(data)
            
            # Create visualization based on type
            if viz_type == "bar":
                fig = px.bar(
                    df,
                    x=params.get("x"),
                    y=params.get("y"),
                    title=params.get("title", ""),
                    color=params.get("color"),
                    barmode=params.get("barmode", "group")
                )
            elif viz_type == "line":
                fig = px.line(
                    df,
                    x=params.get("x"),
                    y=params.get("y"),
                    title=params.get("title", ""),
                    color=params.get("color")
                )
            elif viz_type == "scatter":
                fig = px.scatter(
                    df,
                    x=params.get("x"),
                    y=params.get("y"),
                    title=params.get("title", ""),
                    color=params.get("color"),
                    size=params.get("size")
                )
            elif viz_type == "pie":
                fig = px.pie(
                    df,
                    values=params.get("values"),
                    names=params.get("names"),
                    title=params.get("title", "")
                )
            else:
                logger.warning(f"Unsupported visualization type: {viz_type}")
                return None

            # Update layout
            fig.update_layout(
                template="plotly_white",
                title_x=0.5,
                margin=dict(t=50, l=50, r=50, b=50)
            )

            return {
                "figure": fig,
                "type": viz_type,
                "data_shape": df.shape
            }
        except Exception as e:
            logger.error(f"Error creating visualization: {str(e)}")
            return None

    @staticmethod
    def suggest_visualization(data: str) -> Tuple[str, Dict[str, Any]]:
        """
        Analyze the data and suggest appropriate visualization type and parameters.
        """
        try:
            # Convert string data to DataFrame
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    data = pd.read_csv(pd.StringIO(data))
            
            df = pd.DataFrame(data)
            
            # Analyze columns
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns
            
            # Simple rules for visualization suggestions
            if len(df.columns) == 2:
                if len(numeric_cols) == 2:
                    return "scatter", {
                        "x": numeric_cols[0],
                        "y": numeric_cols[1],
                        "title": f"{numeric_cols[1]} vs {numeric_cols[0]}"
                    }
                elif len(numeric_cols) == 1 and len(categorical_cols) == 1:
                    return "bar", {
                        "x": categorical_cols[0],
                        "y": numeric_cols[0],
                        "title": f"{numeric_cols[0]} by {categorical_cols[0]}"
                    }
            elif len(df.columns) > 2:
                if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
                    return "bar", {
                        "x": categorical_cols[0],
                        "y": numeric_cols[0],
                        "color": categorical_cols[1] if len(categorical_cols) > 1 else None,
                        "title": f"{numeric_cols[0]} by {categorical_cols[0]}"
                    }
            
            # Default to bar chart if no specific suggestion
            return "bar", {
                "x": df.columns[0],
                "y": df.columns[1] if len(df.columns) > 1 else df.columns[0],
                "title": "Data Visualization"
            }
        except Exception as e:
            logger.error(f"Error suggesting visualization: {str(e)}")
            return "bar", {"title": "Data Visualization"} 