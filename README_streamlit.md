# UGC AI Workflow - Streamlit App

A Streamlit application that generates authentic User-Generated Content (UGC) using AI-powered persona creation and video scripts.

## Features

- **AI Persona Generation**: Creates detailed profiles of ideal creators for your product
- **Creator Image Generation**: Generates photorealistic images of the creator
- **First Frame Creation**: Creates the opening shot with creator holding your product
- **Video Script Generation**: Writes natural 12-second UGC video scripts
- **Progress Tracking**: Visual feedback during workflow execution
- **Download Results**: Download generated images and scripts

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the project root with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
FAL_API_KEY=your_fal_api_key_here
```

### 3. Run the App

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Input Product Details**: Fill in the product name and description in the sidebar
2. **Upload Product Image**: Upload an image of your product (PNG, JPG, or JPEG)
3. **Generate Content**: Click "Generate UGC Content" to start the workflow
4. **Monitor Progress**: Watch the progress bar and step descriptions
5. **Download Results**: Download the generated first frame image and video script

## Workflow Steps

1. **Step 1**: AI analyzes your product and generates a detailed persona profile
2. **Step 2**: Creates a photorealistic image of the ideal creator
3. **Step 3**: Generates the first frame with creator holding your product
4. **Step 4**: Writes a natural 12-second UGC video script

## API Requirements

- **OpenAI API**: For persona generation and video script creation
- **Gemini API**: For image generation capabilities
- **Fal.ai API**: For image editing and manipulation

## Troubleshooting

- Ensure all API keys are correctly set in your `.env` file
- Check that you have sufficient API quota for all services
- Verify that your product image is in a supported format (PNG, JPG, JPEG)
- Make sure all required dependencies are installed

## Output

The app generates:
- A detailed persona profile of the ideal creator
- A photorealistic creator image
- The first frame of the video with creator holding the product
- A complete 12-second UGC video script with shot-by-shot breakdown


