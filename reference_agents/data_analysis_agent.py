"""
Data Analysis Agent - Advanced Reference Implementation

This agent demonstrates sophisticated data analysis capabilities including:
- Statistical analysis and pattern detection
- Time series analysis and forecasting
- Data quality assessment and validation
- Automated insights generation
- Visualization recommendations
"""

import asyncio
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging

from src.core.agent_base import AgentBase, AgentCapability
from src.core.execution_context import ExecutionContext
from src.tools.llm_tools import get_llm_client

logger = logging.getLogger(__name__)

@dataclass
class DataAnalysisResult:
    """Result of data analysis operation."""
    summary: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]
    visualizations: List[Dict[str, Any]]
    quality_score: float
    anomalies: List[Dict[str, Any]]

class DataAnalysisAgent(AgentBase):
    """
    Professional data analysis agent for comprehensive data insights.

    Capabilities:
    - Descriptive statistics and data profiling
    - Pattern detection and anomaly identification
    - Time series analysis and forecasting
    - Data quality assessment
    - Automated insights generation
    - Visualization recommendations
    """

    def __init__(self, **kwargs):
        super().__init__(
            name="data_analysis_agent",
            description="Advanced data analysis and insights generation agent",
            capabilities=[
                AgentCapability.DATA_ANALYSIS,
                AgentCapability.DOCUMENT_ANALYSIS,
                AgentCapability.TEXT_PROCESSING
            ],
            **kwargs
        )
        self.llm_client = get_llm_client()
        self.analysis_history = []

    async def execute(self, input_data: Dict[str, Any], context: ExecutionContext) -> Dict[str, Any]:
        """
        Execute comprehensive data analysis.

        Args:
            input_data: Dictionary containing:
                - data: DataFrame or data structure to analyze
                - analysis_type: Type of analysis to perform
                - config: Analysis configuration options
            context: Execution context

        Returns:
            Comprehensive analysis results
        """
        try:
            # Extract input parameters
            data = input_data.get("data")
            analysis_type = input_data.get("analysis_type", "comprehensive")
            config = input_data.get("config", {})

            # Convert data if needed
            df = self._prepare_data(data)

            # Perform analysis based on type
            if analysis_type == "comprehensive":
                result = await self._comprehensive_analysis(df, config, context)
            elif analysis_type == "time_series":
                result = await self._time_series_analysis(df, config, context)
            elif analysis_type == "quality_assessment":
                result = await self._data_quality_assessment(df, config, context)
            elif analysis_type == "anomaly_detection":
                result = await self._anomaly_detection(df, config, context)
            else:
                result = await self._comprehensive_analysis(df, config, context)

            # Store analysis history
            self.analysis_history.append({
                "timestamp": datetime.now().isoformat(),
                "analysis_type": analysis_type,
                "data_shape": df.shape if df is not None else "unknown",
                "agent_id": self.id,
                "context_id": context.execution_id
            })

            return {
                "analysis_result": result.__dict__,
                "metadata": {
                    "analysis_type": analysis_type,
                    "data_shape": df.shape if df is not None else None,
                    "processing_time": context.elapsed_time,
                    "agent_id": self.id
                }
            }

        except Exception as e:
            logger.error(f"Data analysis failed: {str(e)}")
            return {
                "error": f"Analysis failed: {str(e)}",
                "analysis_result": None,
                "metadata": {"error_type": type(e).__name__}
            }

    def _prepare_data(self, data: Any) -> Optional[pd.DataFrame]:
        """Convert input data to pandas DataFrame."""
        try:
            if isinstance(data, pd.DataFrame):
                return data
            elif isinstance(data, dict):
                return pd.DataFrame(data)
            elif isinstance(data, list):
                return pd.DataFrame(data)
            elif isinstance(data, str):
                # Try to parse as JSON
                try:
                    parsed = json.loads(data)
                    return pd.DataFrame(parsed)
                except:
                    # Try to read as CSV
                    return pd.read_csv(data)
            else:
                logger.warning(f"Unsupported data type: {type(data)}")
                return None
        except Exception as e:
            logger.error(f"Data preparation failed: {str(e)}")
            return None

    async def _comprehensive_analysis(self, df: pd.DataFrame, config: Dict, context: ExecutionContext) -> DataAnalysisResult:
        """Perform comprehensive data analysis."""

        # Basic statistics
        summary = {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "memory_usage": df.memory_usage(deep=True).sum(),
            "numeric_columns": list(df.select_dtypes(include=[np.number]).columns),
            "categorical_columns": list(df.select_dtypes(include=['object', 'category']).columns)
        }

        # Descriptive statistics for numeric columns
        if summary["numeric_columns"]:
            summary["descriptive_stats"] = df[summary["numeric_columns"]].describe().to_dict()

        # Generate insights using LLM
        insights = await self._generate_insights(df, summary)

        # Generate recommendations
        recommendations = await self._generate_recommendations(df, summary, insights)

        # Suggest visualizations
        visualizations = self._suggest_visualizations(df, summary)

        # Calculate data quality score
        quality_score = self._calculate_quality_score(df, summary)

        # Detect anomalies
        anomalies = self._detect_basic_anomalies(df)

        return DataAnalysisResult(
            summary=summary,
            insights=insights,
            recommendations=recommendations,
            visualizations=visualizations,
            quality_score=quality_score,
            anomalies=anomalies
        )

    async def _time_series_analysis(self, df: pd.DataFrame, config: Dict, context: ExecutionContext) -> DataAnalysisResult:
        """Perform time series analysis."""

        # Identify time columns
        time_columns = []
        for col in df.columns:
            if df[col].dtype == 'datetime64[ns]' or 'time' in col.lower() or 'date' in col.lower():
                time_columns.append(col)

        if not time_columns:
            # Try to infer time column
            for col in df.columns:
                try:
                    pd.to_datetime(df[col].head())
                    time_columns.append(col)
                    break
                except:
                    continue

        summary = {
            "time_columns": time_columns,
            "shape": df.shape,
            "time_range": None,
            "frequency": None,
            "trends": [],
            "seasonality": None
        }

        insights = []
        recommendations = []

        if time_columns:
            time_col = time_columns[0]
            df[time_col] = pd.to_datetime(df[time_col])

            # Basic time series info
            summary["time_range"] = {
                "start": df[time_col].min().isoformat(),
                "end": df[time_col].max().isoformat(),
                "duration_days": (df[time_col].max() - df[time_col].min()).days
            }

            # Detect frequency
            if len(df) > 1:
                time_diffs = df[time_col].diff().dropna()
                most_common_diff = time_diffs.mode()
                if len(most_common_diff) > 0:
                    summary["frequency"] = str(most_common_diff.iloc[0])

            # Analyze numeric columns over time
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                trend = self._analyze_trend(df[time_col], df[col])
                summary["trends"].append({
                    "column": col,
                    "trend": trend
                })

            insights.append(f"Time series spans {summary['time_range']['duration_days']} days")
            insights.append(f"Data frequency appears to be {summary['frequency']}")

            recommendations.append("Consider using time-based visualizations like line charts")
            recommendations.append("Look for seasonal patterns in the data")
        else:
            insights.append("No clear time columns identified")
            recommendations.append("Consider adding timestamp information for time series analysis")

        return DataAnalysisResult(
            summary=summary,
            insights=insights,
            recommendations=recommendations,
            visualizations=self._suggest_time_series_visualizations(df, time_columns),
            quality_score=self._calculate_quality_score(df, summary),
            anomalies=[]
        )

    async def _data_quality_assessment(self, df: pd.DataFrame, config: Dict, context: ExecutionContext) -> DataAnalysisResult:
        """Assess data quality comprehensively."""

        # Quality metrics
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()

        quality_metrics = {
            "completeness": 1 - (missing_cells / total_cells) if total_cells > 0 else 0,
            "uniqueness": 1 - (duplicate_rows / len(df)) if len(df) > 0 else 0,
            "consistency": 1.0,  # Would need domain-specific rules
            "validity": 1.0,     # Would need validation rules
            "accuracy": 1.0      # Would need ground truth
        }

        # Column-level quality assessment
        column_quality = {}
        for col in df.columns:
            col_quality = {
                "missing_percentage": (df[col].isnull().sum() / len(df)) * 100,
                "unique_values": df[col].nunique(),
                "data_type": str(df[col].dtype),
                "sample_values": df[col].dropna().head(5).tolist()
            }

            # Type-specific checks
            if df[col].dtype == 'object':
                col_quality["avg_length"] = df[col].str.len().mean()
                col_quality["empty_strings"] = (df[col] == '').sum()
            elif np.issubdtype(df[col].dtype, np.number):
                col_quality["outliers"] = self._count_outliers(df[col])
                col_quality["zeros"] = (df[col] == 0).sum()
                col_quality["negatives"] = (df[col] < 0).sum()

            column_quality[col] = col_quality

        summary = {
            "overall_quality": quality_metrics,
            "column_quality": column_quality,
            "data_issues": self._identify_data_issues(df),
            "recommendations": []
        }

        # Generate quality insights
        insights = await self._generate_quality_insights(df, summary)

        # Quality-specific recommendations
        recommendations = []
        if quality_metrics["completeness"] < 0.95:
            recommendations.append("Address missing data through imputation or removal")
        if quality_metrics["uniqueness"] < 0.98:
            recommendations.append("Remove or investigate duplicate rows")
        if missing_cells > 0:
            recommendations.append("Consider data imputation strategies")

        overall_score = np.mean(list(quality_metrics.values()))

        return DataAnalysisResult(
            summary=summary,
            insights=insights,
            recommendations=recommendations,
            visualizations=self._suggest_quality_visualizations(df),
            quality_score=overall_score,
            anomalies=[]
        )

    async def _anomaly_detection(self, df: pd.DataFrame, config: Dict, context: ExecutionContext) -> DataAnalysisResult:
        """Detect anomalies in the data."""

        anomalies = []
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            # Statistical outliers (IQR method)
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

            if len(outliers) > 0:
                anomalies.append({
                    "type": "statistical_outlier",
                    "column": col,
                    "count": len(outliers),
                    "percentage": (len(outliers) / len(df)) * 100,
                    "indices": outliers.index.tolist()[:10],  # First 10 indices
                    "values": outliers[col].tolist()[:10]     # First 10 values
                })

        # Check for unusual patterns
        for col in df.select_dtypes(include=['object']).columns:
            # Extremely rare categories
            value_counts = df[col].value_counts()
            rare_values = value_counts[value_counts == 1]

            if len(rare_values) > len(value_counts) * 0.1:  # More than 10% are unique
                anomalies.append({
                    "type": "rare_categories",
                    "column": col,
                    "count": len(rare_values),
                    "percentage": (len(rare_values) / len(value_counts)) * 100,
                    "examples": rare_values.index.tolist()[:5]
                })

        summary = {
            "total_anomalies": len(anomalies),
            "anomaly_types": list(set([a["type"] for a in anomalies])),
            "affected_columns": list(set([a["column"] for a in anomalies]))
        }

        insights = [
            f"Found {len(anomalies)} types of anomalies across {len(set([a['column'] for a in anomalies]))} columns",
            f"Most common anomaly type: {max([a['type'] for a in anomalies], key=[a['type'] for a in anomalies].count) if anomalies else 'None'}"
        ]

        recommendations = []
        if len(anomalies) > 0:
            recommendations.append("Investigate detected anomalies for data quality issues")
            recommendations.append("Consider outlier treatment strategies")
            recommendations.append("Validate unusual values with domain experts")
        else:
            recommendations.append("No significant anomalies detected - data appears clean")

        return DataAnalysisResult(
            summary=summary,
            insights=insights,
            recommendations=recommendations,
            visualizations=self._suggest_anomaly_visualizations(df),
            quality_score=1.0 - (len(anomalies) / (len(df.columns) * 2)),  # Rough quality score
            anomalies=anomalies
        )

    async def _generate_insights(self, df: pd.DataFrame, summary: Dict) -> List[str]:
        """Generate insights using LLM analysis."""
        try:
            # Prepare data summary for LLM
            data_description = f"""
            Dataset Analysis Summary:
            - Shape: {summary['shape']} (rows x columns)
            - Columns: {', '.join(summary['columns'][:10])}{'...' if len(summary['columns']) > 10 else ''}
            - Missing values: {sum(summary['missing_values'].values())} total
            - Numeric columns: {len(summary['numeric_columns'])}
            - Categorical columns: {len(summary['categorical_columns'])}
            """

            if 'descriptive_stats' in summary:
                stats_summary = "\nKey Statistics:\n"
                for col, stats in list(summary['descriptive_stats'].items())[:3]:
                    stats_summary += f"- {col}: mean={stats.get('mean', 'N/A'):.2f}, std={stats.get('std', 'N/A'):.2f}\n"
                data_description += stats_summary

            prompt = f"""
            Analyze this dataset and provide 3-5 key insights about the data:

            {data_description}

            Focus on:
            1. Data distribution patterns
            2. Potential data quality concerns
            3. Interesting relationships or patterns
            4. Business implications

            Provide insights as a list of clear, actionable statements.
            """

            response = await self.llm_client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )

            # Parse insights from response
            insights_text = response.get("content", "")
            insights = [line.strip("- ").strip() for line in insights_text.split("\n") if line.strip() and not line.strip().isdigit()]

            return insights[:5] if insights else ["Data analysis completed successfully"]

        except Exception as e:
            logger.warning(f"LLM insight generation failed: {str(e)}")
            return [
                f"Dataset contains {summary['shape'][0]} rows and {summary['shape'][1]} columns",
                f"Found {sum(summary['missing_values'].values())} missing values across all columns",
                f"Data includes {len(summary['numeric_columns'])} numeric and {len(summary['categorical_columns'])} categorical features"
            ]

    async def _generate_recommendations(self, df: pd.DataFrame, summary: Dict, insights: List[str]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        # Data quality recommendations
        missing_pct = sum(summary['missing_values'].values()) / (df.shape[0] * df.shape[1]) * 100
        if missing_pct > 5:
            recommendations.append("Consider data imputation or removal strategies for missing values")

        # Memory optimization
        if summary['memory_usage'] > 100_000_000:  # > 100MB
            recommendations.append("Consider data type optimization to reduce memory usage")

        # Column recommendations
        if len(summary['categorical_columns']) > len(summary['numeric_columns']):
            recommendations.append("Consider encoding categorical variables for machine learning")

        # Analysis recommendations
        if len(summary['numeric_columns']) > 0:
            recommendations.append("Explore correlations between numeric variables")
            recommendations.append("Consider outlier detection and treatment")

        if df.shape[0] > 10000:
            recommendations.append("Consider sampling strategies for large dataset analysis")

        return recommendations[:5]

    async def _generate_quality_insights(self, df: pd.DataFrame, summary: Dict) -> List[str]:
        """Generate data quality specific insights."""
        quality = summary['overall_quality']
        insights = []

        insights.append(f"Data completeness: {quality['completeness']:.1%}")
        insights.append(f"Data uniqueness: {quality['uniqueness']:.1%}")

        # Column-specific insights
        problematic_cols = [col for col, info in summary['column_quality'].items()
                          if info['missing_percentage'] > 10]
        if problematic_cols:
            insights.append(f"Columns with >10% missing: {', '.join(problematic_cols[:3])}")

        # Data type insights
        object_cols = [col for col, info in summary['column_quality'].items()
                      if info['data_type'] == 'object']
        if object_cols:
            insights.append(f"Text columns may need preprocessing: {len(object_cols)} found")

        return insights

    def _analyze_trend(self, time_series: pd.Series, values: pd.Series) -> str:
        """Analyze trend in time series data."""
        try:
            # Simple linear trend analysis
            x = np.arange(len(values))
            y = values.dropna()
            if len(y) > 1:
                slope = np.polyfit(x[:len(y)], y, 1)[0]
                if slope > 0.01:
                    return "increasing"
                elif slope < -0.01:
                    return "decreasing"
                else:
                    return "stable"
            return "insufficient_data"
        except:
            return "unknown"

    def _calculate_quality_score(self, df: pd.DataFrame, summary: Dict) -> float:
        """Calculate overall data quality score."""
        factors = []

        # Completeness factor
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        completeness = 1 - (missing_cells / total_cells) if total_cells > 0 else 0
        factors.append(completeness)

        # Uniqueness factor (for appropriate columns)
        duplicates = df.duplicated().sum()
        uniqueness = 1 - (duplicates / len(df)) if len(df) > 0 else 0
        factors.append(uniqueness)

        # Consistency factor (basic check)
        consistency = 1.0  # Would need domain-specific rules
        factors.append(consistency)

        return np.mean(factors)

    def _detect_basic_anomalies(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect basic statistical anomalies."""
        anomalies = []

        for col in df.select_dtypes(include=[np.number]).columns:
            try:
                # Z-score method
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outliers = df[z_scores > 3]

                if len(outliers) > 0:
                    anomalies.append({
                        "type": "statistical_outlier",
                        "column": col,
                        "count": len(outliers),
                        "method": "z_score",
                        "threshold": 3.0
                    })
            except:
                continue

        return anomalies

    def _count_outliers(self, series: pd.Series) -> int:
        """Count outliers using IQR method."""
        try:
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return len(series[(series < lower_bound) | (series > upper_bound)])
        except:
            return 0

    def _identify_data_issues(self, df: pd.DataFrame) -> List[str]:
        """Identify potential data issues."""
        issues = []

        # Check for columns with all missing values
        all_missing = df.columns[df.isnull().all()].tolist()
        if all_missing:
            issues.append(f"Columns with all missing values: {', '.join(all_missing)}")

        # Check for constant columns
        constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
        if constant_cols:
            issues.append(f"Constant columns detected: {', '.join(constant_cols)}")

        # Check for potential ID columns
        potential_ids = [col for col in df.columns if df[col].nunique() == len(df)]
        if potential_ids:
            issues.append(f"Potential ID columns: {', '.join(potential_ids)}")

        return issues

    def _suggest_visualizations(self, df: pd.DataFrame, summary: Dict) -> List[Dict[str, Any]]:
        """Suggest appropriate visualizations."""
        suggestions = []

        # Numeric column visualizations
        if summary["numeric_columns"]:
            suggestions.append({
                "type": "histogram",
                "columns": summary["numeric_columns"][:3],
                "description": "Distribution of numeric variables"
            })

            if len(summary["numeric_columns"]) > 1:
                suggestions.append({
                    "type": "correlation_heatmap",
                    "columns": summary["numeric_columns"],
                    "description": "Correlation matrix of numeric variables"
                })

        # Categorical column visualizations
        if summary["categorical_columns"]:
            suggestions.append({
                "type": "bar_chart",
                "columns": summary["categorical_columns"][:2],
                "description": "Count of categorical variables"
            })

        # Missing data visualization
        if sum(summary["missing_values"].values()) > 0:
            suggestions.append({
                "type": "missing_data_matrix",
                "columns": list(summary["missing_values"].keys()),
                "description": "Pattern of missing data"
            })

        return suggestions

    def _suggest_time_series_visualizations(self, df: pd.DataFrame, time_columns: List[str]) -> List[Dict[str, Any]]:
        """Suggest time series specific visualizations."""
        suggestions = []

        if time_columns:
            numeric_cols = df.select_dtypes(include=[np.number]).columns

            suggestions.append({
                "type": "line_chart",
                "x_column": time_columns[0],
                "y_columns": numeric_cols.tolist()[:3],
                "description": "Time series line chart"
            })

            suggestions.append({
                "type": "seasonal_decomposition",
                "time_column": time_columns[0],
                "value_columns": numeric_cols.tolist()[:2],
                "description": "Seasonal pattern analysis"
            })

        return suggestions

    def _suggest_quality_visualizations(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Suggest data quality visualizations."""
        return [
            {
                "type": "missing_data_heatmap",
                "description": "Heatmap showing missing data patterns"
            },
            {
                "type": "data_types_summary",
                "description": "Summary of data types and null counts"
            },
            {
                "type": "outlier_detection_plot",
                "description": "Box plots showing potential outliers"
            }
        ]

    def _suggest_anomaly_visualizations(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Suggest anomaly detection visualizations."""
        return [
            {
                "type": "outlier_scatter",
                "description": "Scatter plot highlighting outliers"
            },
            {
                "type": "anomaly_score_distribution",
                "description": "Distribution of anomaly scores"
            },
            {
                "type": "box_plot_outliers",
                "description": "Box plots showing statistical outliers"
            }
        ]

    def get_analysis_history(self) -> List[Dict[str, Any]]:
        """Get history of analyses performed by this agent."""
        return self.analysis_history.copy()

    def get_capabilities_summary(self) -> Dict[str, Any]:
        """Get summary of agent capabilities."""
        return {
            "agent_id": self.id,
            "name": self.name,
            "analysis_types": [
                "comprehensive",
                "time_series",
                "quality_assessment",
                "anomaly_detection"
            ],
            "supported_formats": [
                "pandas.DataFrame",
                "JSON",
                "CSV",
                "Python dictionaries",
                "Lists"
            ],
            "outputs": [
                "Statistical summaries",
                "Data insights",
                "Quality assessments",
                "Anomaly detection",
                "Visualization recommendations",
                "Actionable recommendations"
            ],
            "total_analyses": len(self.analysis_history)
        }

# Example usage and testing
async def demo_data_analysis_agent():
    """Demonstrate the data analysis agent capabilities."""

    print("🔬 Data Analysis Agent Demo\n")

    # Create agent
    agent = DataAnalysisAgent()

    # Create sample data
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    np.random.seed(42)

    sample_data = pd.DataFrame({
        'date': dates,
        'sales': np.random.normal(1000, 200, 100) + np.sin(np.arange(100) * 0.1) * 100,
        'temperature': np.random.normal(20, 5, 100),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
        'customer_count': np.random.poisson(50, 100),
        'satisfaction': np.random.uniform(1, 5, 100)
    })

    # Add some missing values and outliers
    sample_data.loc[10:15, 'satisfaction'] = np.nan
    sample_data.loc[50, 'sales'] = 5000  # Outlier

    print("📊 Sample data created:")
    print(f"   Shape: {sample_data.shape}")
    print(f"   Columns: {list(sample_data.columns)}")
    print()

    # Test different analysis types
    analysis_types = [
        ("comprehensive", "Complete data analysis"),
        ("time_series", "Time series analysis"),
        ("quality_assessment", "Data quality assessment"),
        ("anomaly_detection", "Anomaly detection")
    ]

    for analysis_type, description in analysis_types:
        print(f"🔍 {description}:")

        context = ExecutionContext(agent_id=agent.id)
        result = await agent.run({
            "data": sample_data,
            "analysis_type": analysis_type,
            "config": {}
        }, context)

        if result["status"] == "completed":
            output = result["output"]
            analysis_result = output["analysis_result"]

            print(f"   ✅ Analysis completed")
            print(f"   📈 Quality Score: {analysis_result['quality_score']:.2f}")
            print(f"   💡 Insights: {len(analysis_result['insights'])} generated")
            print(f"   📋 Recommendations: {len(analysis_result['recommendations'])} provided")
            print(f"   📊 Visualizations: {len(analysis_result['visualizations'])} suggested")
            print(f"   🚨 Anomalies: {len(analysis_result['anomalies'])} detected")

            # Show first insight and recommendation
            if analysis_result['insights']:
                print(f"   First insight: {analysis_result['insights'][0]}")
            if analysis_result['recommendations']:
                print(f"   First recommendation: {analysis_result['recommendations'][0]}")
        else:
            print(f"   ❌ Analysis failed: {result.get('error', 'Unknown error')}")

        print()

    # Show agent capabilities
    print("🤖 Agent Capabilities:")
    capabilities = agent.get_capabilities_summary()
    print(f"   Analysis types: {', '.join(capabilities['analysis_types'])}")
    print(f"   Supported formats: {', '.join(capabilities['supported_formats'])}")
    print(f"   Total analyses performed: {capabilities['total_analyses']}")

    print("\n✅ Data Analysis Agent demo completed!")

if __name__ == "__main__":
    asyncio.run(demo_data_analysis_agent())
