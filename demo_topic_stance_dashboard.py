"""
Demo script for Topic-Based Granular Stance Analysis Dashboard.

This script demonstrates how to run the integrated dashboard that combines
topic modeling results with granular stance analysis.

Usage:
    python demo_topic_stance_dashboard.py
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required files exist."""
    required_files = [
        "streamlit_granular_stance.py",
        "topic_stance_integration.py",
        "stance_analysis_granular.py",
        "load_data.py"
    ]

    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)

    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False

    # Check if results directory exists
    if not Path("results").exists():
        print("❌ Results directory not found. Please run topic modeling first.")
        return False

    # Check for topic modeling results
    topic_files = list(Path("results").glob("posts_with_topics_*.csv"))
    stance_files = list(Path("results").glob("comments_with_stance_*.csv"))

    if not topic_files or not stance_files:
        print("❌ Topic modeling or stance analysis results not found in results/")
        print("Please run topic modeling and stance analysis first.")
        return False

    return True

def run_dashboard():
    """Run the Streamlit dashboard."""
    print("🚀 Starting Topic-Based Granular Stance Analysis Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8501")
    print("💡 Select 'Topic Modeling Results' as data source to see the integrated view")
    print("🔍 Use filters to explore: Topic → Posts → Comments → Stance Analysis")
    print("")
    print("Press Ctrl+C to stop the dashboard")
    print("-" * 60)

    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "streamlit_granular_stance.py",
            "--server.headless", "true",
            "--server.port", "8501"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running dashboard: {e}")
        return False

    return True

def show_available_data():
    """Show summary of available data."""
    print("📋 Available Data Summary:")
    print("-" * 40)

    # Show available timestamps
    from topic_stance_integration import get_available_timestamps
    timestamps = get_available_timestamps("results")

    if timestamps:
        print(f"📅 Available analysis periods: {len(timestamps)}")
        for ts in timestamps[:5]:  # Show first 5
            print(f"   • {ts[:8]} {ts[9:11]}:{ts[11:13]}:{ts[13:15]}")
        if len(timestamps) > 5:
            print(f"   ... and {len(timestamps) - 5} more")
    else:
        print("❌ No analysis periods found")

    # Show latest data summary
    if timestamps:
        try:
            from topic_stance_integration import load_topic_stance_data, get_topic_summary
            posts_df, comments_df, merged_df = load_topic_stance_data("results", timestamps[0])
            topic_summary = get_topic_summary(merged_df)

            print(f"\n📊 Latest Dataset ({timestamps[0][:8]}):")
            print(f"   • Posts: {len(posts_df)}")
            print(f"   • Comments: {len(comments_df)}")
            print(f"   • Topics: {len(topic_summary)}")
            print(f"   • Comments with stance: {len(comments_df[comments_df['stance_label'].notna()])}")

        except Exception as e:
            print(f"❌ Error loading latest data: {e}")

    print()

def main():
    """Main function."""
    print("🎯 Topic-Based Granular Stance Analysis Dashboard Demo")
    print("=" * 60)

    # Check requirements
    if not check_requirements():
        print("❌ Requirements not met. Please check the errors above.")
        return 1

    # Show data summary
    show_available_data()

    # Run dashboard
    success = run_dashboard()

    if success:
        print("✅ Dashboard demo completed successfully!")
        return 0
    else:
        print("❌ Dashboard demo failed!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
