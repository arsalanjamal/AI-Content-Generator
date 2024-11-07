import gradio as gr
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

# Function to handle the Gradio interface
def generate_content(content_type, tone, length, prompt):
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

        # Generate PDF for download
        pdf_output = export_to_pdf(f"{content_type} on {prompt}", content)

        return content, pdf_output
    else:
        return "Please provide a topic or keywords.", None

# Set up Gradio interface
def create_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# AI-Based Content Generator")
        
        # Dropdown for content type selection
        content_type = gr.Dropdown(
            choices=["Blog Post", "Social Media Post", "Product Description"],
            label="Content Type"
        )
        
        # Dropdown for tone selection
        tone = gr.Dropdown(
            choices=["Formal", "Casual", "Professional", "Inspirational", "Humorous"],
            label="Tone"
        )
        
        # Slider for content length
        length = gr.Slider(minimum=100, maximum=1500, value=500, label="Content Length (in words)")
        
        # Textbox for the prompt or keywords
        prompt = gr.Textbox(lines=2, placeholder="e.g., Artificial Intelligence, Future of Tech", label="Enter Keywords or Topic")
        
        # Button to generate content
        generate_button = gr.Button("Generate Content")
        
        # Outputs
        generated_content = gr.Textbox(label="Generated Content", interactive=False)
        pdf_output = gr.File(label="Download Content as PDF", interactive=False)
        
        # Button callback
        generate_button.click(generate_content, inputs=[content_type, tone, length, prompt], outputs=[generated_content, pdf_output])

    demo.launch()

if __name__ == "__main__":
    create_interface()
