import streamlit as st
from transformers import pipeline
from fpdf import FPDF

# Set up Hugging Face GPT-Neo 2.7B model using pipeline
pipe = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")

# Function to generate content using GPT-Neo
def generate_content_from_gpt_neo(prompt, max_length=500):
    # Use the pipeline to generate text
    content = pipe(prompt, max_length=max_length, num_return_sequences=1)[0]['generated_text']
    return content

# Function to create a PDF file for download
def export_to_pdf(title, content):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Add title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=title, ln=True, align="C")
    
    # Add content
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=content)
    
    # Save the PDF to BytesIO for download
    pdf_output = pdf.output(dest="S").encode("latin1")
    return pdf_output

# Streamlit interface to collect user input and generate content
def main():
    st.title("AI-Based Content Generator")

    st.header("Content Type")
    content_type = st.selectbox("Select Content Type", ["Blog Post", "Social Media Post", "Product Description"])
    
    tone = st.selectbox("Select Tone", ["Formal", "Casual", "Professional", "Inspirational", "Humorous"])
    
    # Length slider for content
    length = st.slider("Content Length (in words)", min_value=100, max_value=1500, value=500)
    
    # Prompt or keywords input
    prompt = st.text_area("Enter Keywords or Topic", "e.g., Artificial Intelligence, Future of Tech")
    
    # Button to generate content
    if st.button("Generate Content"):
        if prompt:
            # Construct a custom prompt based on user input
            if content_type == "Blog Post":
                user_prompt = f"Write a {tone} blog post of {length} words about {prompt}. Include an engaging introduction and conclusion."
            elif content_type == "Social Media Post":
                user_prompt = f"Write a {tone} social media post of {length} words about {prompt}. The tone should be short, catchy, and engaging."
            else:  # Product Description
                user_prompt = f"Write a {tone} product description of {length} words about {prompt}. Focus on key features and benefits."

            # Generate content using GPT-Neo
            content = generate_content_from_gpt_neo(user_prompt, max_length=length)

            st.subheader("Generated Content")
            st.write(content)

            # Option to download content as PDF
            pdf_output = export_to_pdf(f"{content_type} on {prompt}", content)
            st.download_button("Download Content as PDF", pdf_output, file_name=f"{prompt}_generated_content.pdf")
        else:
            st.error("Please provide a topic or keywords.")

if __name__ == "__main__":
    main()
