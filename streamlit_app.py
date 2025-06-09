import streamlit as st
from PIL import Image
import easyocr
import io
import fitz # PyMuPDF for PDF processing
import json
import base64

# --- Firebase/LLM API Configuration ---
# These variables are expected to be provided by the environment.
# We use try-except to gracefully handle cases where they might not be defined
# in a non-Canvas environment, though they are mandatory in Canvas.
try:
    appId = __app_id
except NameError:
    appId = 'default-app-id'

try:
    firebaseConfig = json.loads(__firebase_config)
except NameError:
    firebaseConfig = {}

try:
    initialAuthToken = __initial_auth_token
except NameError:
    initialAuthToken = ''

# --- Initialize EasyOCR Reader (run once) ---
@st.cache_resource
def load_ocr_reader():
    # Initialize EasyOCR reader for English language
    # 'gpu': False forces CPU usage, set to True if you have a compatible GPU
    # This will download necessary models on first run
    return easyocr.Reader(['en'], gpu=False)

reader = load_ocr_reader()

# --- Function to perform OCR ---
def perform_ocr_on_image(image_bytes):
    """
    Performs OCR on an image byte stream using EasyOCR.
    Returns the raw extracted text.
    """
    try:
        # EasyOCR can directly read from bytes
        result = reader.readtext(image_bytes)
        # Concatenate all detected text lines
        raw_text = "\n".join([text for (bbox, text, prob) in result])
        return raw_text
    except Exception as e:
        st.error(f"Error during OCR: {e}")
        return None

def perform_ocr_on_pdf(pdf_bytes):
    """
    Performs OCR on a PDF byte stream by converting pages to images
    and then applying EasyOCR.
    Returns the raw extracted text from all pages.
    """
    all_text = []
    try:
        # Open the PDF document from bytes
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            # Render page to a pixmap (image)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # Increase resolution for better OCR
            img_bytes = pix.pil_tobytes(format="PNG") # Convert pixmap to PNG bytes
            
            st.info(f"Processing page {page_num + 1} of PDF...")
            page_text = perform_ocr_on_image(img_bytes)
            if page_text:
                all_text.append(page_text)
            else:
                st.warning(f"Could not extract text from page {page_num + 1}.")
        doc.close()
        return "\n\n--- Page Break ---\n\n".join(all_text)
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None

# --- Function to call LLM for structured data extraction ---
async def extract_invoice_data_with_llm(raw_text):
    """
    Uses the Gemini API to extract structured invoice data from raw OCR text.
    """
    st.info("Sending extracted text to LLM for structured data extraction...")
    chatHistory = []
    prompt = f"""
    You are an expert invoice parser. Extract the following details from the provided invoice text.
    If a field is not found, return null for its value.
    Extract all line items, each with a description, quantity, unit_price, and total.
    The response must strictly adhere to the JSON schema provided.

    Invoice Text:
    {raw_text}
    """
    chatHistory.push({ role: "user", parts: [{ text: prompt }] });

    # Define the structured response schema
    payload = {
        contents: chatHistory,
        generationConfig: {
            responseMimeType: "application/json",
            responseSchema: {
                type: "OBJECT",
                properties: {
                    "invoice_number": { "type": "STRING", "description": "The unique identifier for the invoice." },
                    "invoice_date": { "type": "STRING", "description": "The date the invoice was issued (e.g.,YYYY-MM-DD or MM/DD/YYYY)." },
                    "due_date": { "type": "STRING", "description": "The date payment is due (e.g.,YYYY-MM-DD or MM/DD/YYYY)." },
                    "vendor_name": { "type": "STRING", "description": "The name of the company or person issuing the invoice." },
                    "vendor_address": { "type": "STRING", "description": "The full address of the vendor." },
                    "customer_name": { "type": "STRING", "description": "The name of the customer the invoice is addressed to." },
                    "customer_address": { "type": "STRING", "description": "The full address of the customer." },
                    "subtotal": { "type": "NUMBER", "description": "The total amount before taxes." },
                    "tax_amount": { "type": "NUMBER", "description": "The total tax amount." },
                    "total_amount": { "type": "NUMBER", "description": "The grand total amount including taxes." },
                    "currency": { "type": "STRING", "description": "The currency symbol (e.g., $, €, £)." },
                    "line_items": {
                        "type": "ARRAY",
                        "description": "A list of individual items or services on the invoice.",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "description": { "type": "STRING", "description": "Description of the item/service." },
                                "quantity": { "type": "NUMBER", "description": "Quantity of the item/service." },
                                "unit_price": { "type": "NUMBER", "description": "Price per unit of the item/service." },
                                "total": { "type": "NUMBER", "description": "Total price for this line item." }
                            },
                            "required": ["description", "quantity", "unit_price", "total"]
                        }
                    }
                },
                "propertyOrdering": [
                    "invoice_number", "invoice_date", "due_date",
                    "vendor_name", "vendor_address",
                    "customer_name", "customer_address",
                    "subtotal", "tax_amount", "total_amount", "currency",
                    "line_items"
                ]
            }
        }
    };

    try {
        const apiKey = ""; # Leave as empty string for Canvas environment
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await response.json();

        if (result.candidates && result.candidates.length > 0 and
            result.candidates[0].content && result.candidates[0].content.parts &&
            result.candidates[0].content.parts.length > 0) {
            const json_string = result.candidates[0].content.parts[0].text;
            # LLM may return markdown code block, so try to parse that
            if json_string.strip().startswith('```json') and json_string.strip().endswith('```'):
                parsed_json = json.loads(json_string.strip()[7:-3])
            else:
                parsed_json = json.loads(json_string)
            st.success("Invoice data successfully extracted and structured!")
            return parsed_json
        } else {
            st.error("LLM did not return a valid response for structured data.");
            print(f"LLM Response: {result}"); # For debugging
            return None
        }
    } catch (e) {
        st.error(f"Error calling LLM for structured data: {e}");
        return None

# --- Streamlit UI ---
st.set_page_config(layout="wide", page_title="Invoice OCR & Parser")

st.title("Invoice OCR & Parser 📄➡️📊")
st.markdown("""
    Upload an invoice (JPG, PNG, or PDF) to extract text and structure it into a consistent JSON format.
    This app uses EasyOCR for text extraction and a Large Language Model (LLM) for intelligent parsing.
""")

uploaded_file = st.file_uploader(
    "Choose an invoice image or PDF...",
    type=["jpg", "jpeg", "png", "pdf"]
)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    file_type = uploaded_file.type

    st.subheader("1. Original Invoice Preview")
    if "image" in file_type:
        st.image(file_bytes, caption="Uploaded Invoice Image", use_column_width=True)
    elif "pdf" in file_type:
        try:
            # Display the first page of the PDF as an image
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            page = doc.load_page(0)
            pix = page.get_pixmap()
            img_bytes = pix.pil_tobytes(format="PNG")
            st.image(img_bytes, caption="First Page of PDF", use_column_width=True)
            doc.close()
        except Exception as e:
            st.error(f"Could not display PDF preview: {e}")

    # Perform OCR
    st.subheader("2. Raw Extracted Text")
    with st.spinner("Performing OCR... This might take a moment."):
        if "image" in file_type:
            raw_invoice_text = perform_ocr_on_image(file_bytes)
        elif "pdf" in file_type:
            raw_invoice_text = perform_ocr_on_pdf(file_bytes)

    if raw_invoice_text:
        st.text_area("Extracted Text", raw_invoice_text, height=300)
    else:
        st.warning("No text could be extracted from the uploaded file.")

    # Extract structured data using LLM
    if raw_invoice_text:
        st.subheader("3. Structured Invoice Data (API Format)")
        with st.spinner("Structuring data with LLM..."):
            structured_data = await extract_invoice_data_with_llm(raw_invoice_text)

        if structured_data:
            json_output = json.dumps(structured_data, indent=4)
            st.code(json_output, language="json")

            col1, col2 = st.columns([0.2, 0.8])
            with col1:
                st.download_button(
                    label="Download JSON",
                    data=json_output,
                    file_name="invoice_data.json",
                    mime="application/json"
                )
            with col2:
                # Provide a button to copy to clipboard (requires specific handling in browser)
                # For actual clipboard functionality in Streamlit, you'd typically need a custom component
                # This is a fallback to simply display the content to be copied
                st.info("You can copy the JSON above manually or download it.")
                # This is a basic way to allow copying. For a real app, a custom component would be better.
                # However, direct clipboard access from a Streamlit app is restricted by browser security.
                # The download button is the most reliable "push" mechanism.
                # A more robust copy button would involve `st.components.v1.html` or a custom component.
                # For this example, we provide the JSON in a selectable code block.

            st.success("Processing Complete! Review the structured data above.")
            st.markdown("""
                **Next Steps:**
                * Review the extracted JSON for accuracy.
                * Manually copy the JSON or use the "Download JSON" button.
                * Integrate this JSON into your target application's API.
            """)
        else:
            st.error("Failed to structure invoice data. Please check the raw text or try another invoice.")
    else:
        st.info("Upload an invoice to see structured data.")

# --- End of Streamlit UI ---
