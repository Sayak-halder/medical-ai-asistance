import streamlit as st
import google.generativeai as genai
from api_key import api_key


genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

system_prompts = [
    """
    As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images
    for a renowned hospital. Your expertise is crucial  in identifying any anomalies, diseases, or health issues that may be
    present in the images.

Your responsibility includes:

1. Detailed Analysis: Torrent analyze each image focusing on identifying any abnormal findings
2. Findings Report: Document all observed anomalies or signs of diseases. Clearly articulate the findings in structured format.
3. Recommendations and Next steps: Based on your analysis, suggest potential next steps, including further tests and
treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:

1. Scope of Response: Only respond if the image pardons to human health issues only.
2. Clarity of Image: In case where the image quality impedes clear analysis, note that Certain aspects are 'Unable to be
determined based on the provided image.'
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a doctor before making any further decisions."
4. Your insights are invaluable in guiding technical decisions. Please proceed with the analysis adhering to the structured
 approach outlined above.

    Please provide the final response with these 4 headings : 
    Detailed Analysis, Analysis Report, Recommendations and Treatments

"""
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

st.set_page_config(page_title="Medical Assistant", page_icon="🩺")
st.title("Medical 🧑‍⚕️ Image 🩻 Analytics 📊")
st.subheader("An web application that can help users to identify medical conditions through images.")

file_uploaded = st.file_uploader('Upload the image for Analysis',
                                 type=['png', 'jpg', 'jpeg'])

if file_uploaded:
    st.image(file_uploaded, width=200, caption='Uploaded Image')

submit = st.button("Generate Analysis")

if submit:

    image_data = file_uploaded.getvalue()

    image_parts = [
        {
            "mime_type": "image/jpg",
            "data": image_data
        }
    ]

    prompt_parts = [
        image_parts[0],
        system_prompts[0],
    ]

    response = model.generate_content(prompt_parts)
    if response:
        st.title('Detailed analysis based on the uploaded image')
        st.write(response.text)