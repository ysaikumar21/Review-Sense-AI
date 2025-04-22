import streamlit as st
import pandas as pd
from analysis import analyze_feedback
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import base64
from io import BytesIO
import matplotlib.pyplot as plt

# Custom CSS
st.markdown("""
    <style>
        .download-pdf-btn {
            background-color: #ff4b4b !important;
            margin: 15px 0;
            color: white;
            padding: 10px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# PDF generation function
def create_pdf(content):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Add custom styles if they don't exist
    if 'MainTitle' not in styles:
        styles.add(ParagraphStyle(
            name='MainTitle',
            fontSize=18,
            leading=22,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=20
        ))
    if 'SectionTitle' not in styles:
        styles.add(ParagraphStyle(
            name='SectionTitle',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#3498db'),
            spaceAfter=12
        ))
    if 'BodyText' not in styles:
        styles.add(ParagraphStyle(
            name='BodyText',
            fontSize=12,
            leading=15,
            textColor=colors.HexColor('#212529'),
            spaceAfter=6
        ))

    story = [Paragraph("Customer Feedback Analysis Report", styles['MainTitle'])]

    for line in content.split('\n'):
        if line.startswith('## '):
            story.append(Paragraph(line[3:], styles['SectionTitle']))
        elif line.startswith('### '):
            story.append(Paragraph(line[4:], styles['SectionTitle']))
        elif line.strip():
            story.append(Paragraph(line, styles['BodyText']))
        story.append(Spacer(1, 12))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# Main App
st.title("📊 Customer Feedback Analyzer")

uploaded_file = st.file_uploader("**Upload a CSV file** 📂", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.markdown("### 📋 Uploaded Data Preview")
    st.dataframe(df.head())

    column_name = st.selectbox("🔍 Select the column containing reviews", df.columns)

    analysis_focus = st.radio(
        "**What would you like to focus on?**",
        ('Sentiment Analysis', 'Theme Identification', 'Improvement Suggestions', 'All of the Above'),
        index=3
    )

    if st.button("✨ Analyze Feedback", type="primary"):
        with st.spinner('🔍 Analyzing your feedback...'):
            feedback_list = df[column_name].dropna().tolist()
            result = analyze_feedback(feedback_list, analysis_focus)

            # Display analysis result
            st.markdown("## 📈 Analysis Results")
            st.markdown(result, unsafe_allow_html=True)

            # Visualization for sentiment (only in "All of the Above")
            if analysis_focus == 'All of the Above':
                st.markdown("## 📊 Visual Feedback Summary")

                sentiments = ['Positive', 'Neutral', 'Negative']
                sentiment_counts = {s: result.lower().count(s.lower()) for s in sentiments}

                # Bar Chart
                st.markdown("### 📶 Sentiment Distribution (Bar Chart)")
                fig_bar, ax_bar = plt.subplots()
                ax_bar.bar(sentiment_counts.keys(), sentiment_counts.values(), color=['green', 'gray', 'red'])
                ax_bar.set_ylabel('Count')
                ax_bar.set_title('Sentiment Overview')
                st.pyplot(fig_bar)

                # Pie Chart
                st.markdown("### 🥧 Sentiment Breakdown (Pie Chart)")
                fig_pie, ax_pie = plt.subplots()
                ax_pie.pie(sentiment_counts.values(), labels=sentiment_counts.keys(), autopct='%1.1f%%', colors=['green', 'gray', 'red'], startangle=140)
                ax_pie.axis('equal')
                st.pyplot(fig_pie)

                # PDF download
                pdf_buffer = create_pdf(result)
                st.markdown("---")
                st.markdown("### 📥 Download Professional Report")

                b64 = base64.b64encode(pdf_buffer.read()).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="feedback_analysis.pdf">\
                        <button class="download-pdf-btn">Download PDF Report</button></a>'
                st.markdown(href, unsafe_allow_html=True)
