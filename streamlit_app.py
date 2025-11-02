import streamlit as st
import os
import requests
import dotenv
from PIL import Image
from io import BytesIO
import ai

# Load environment variables (as fallback)
dotenv.load_dotenv()


def main():
    st.set_page_config(page_title="UGC AI Workflow", page_icon="🎬", layout="wide")

    st.title("🎬 UGC AI Workflow Generator")
    st.markdown(
        "Generate authentic User-Generated Content with AI-powered persona creation and video scripts"
    )

    # Sidebar for inputs
    with st.sidebar:
        st.header("🔑 API Keys")
        st.markdown(
            "Enter your API keys below. These are required to generate content."
        )

        # API Key inputs
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Your OpenAI API key for persona and script generation",
            value=st.session_state.get("openai_key", ""),
        )
        if openai_key:
            st.session_state["openai_key"] = openai_key

        gemini_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="AIza...",
            help="Your Google Gemini API key for video generation",
            value=st.session_state.get("gemini_key", ""),
        )
        if gemini_key:
            st.session_state["gemini_key"] = gemini_key

        fal_key = st.text_input(
            "Fal.ai API Key",
            type="password",
            placeholder="fal_...",
            help="Your Fal.ai API key for image generation",
            value=st.session_state.get("fal_key", ""),
        )
        if fal_key:
            st.session_state["fal_key"] = fal_key

        st.divider()

        st.header("📝 Input Parameters")

        # Product inputs
        product_name = st.text_input(
            "Product Name",
            placeholder="e.g., Peach Perfect Powder",
            help="Enter the name of your product",
        )

        product_description = st.text_area(
            "Product Description",
            placeholder="Describe your product in detail...",
            height=150,
            help="Provide a detailed description of your product",
        )

        # Product image upload
        uploaded_file = st.file_uploader(
            "Product Image",
            type=["png", "jpg", "jpeg"],
            help="Upload an image of your product",
        )

        # Generate button
        generate_button = st.button(
            "🚀 Generate UGC Content", type="primary", use_container_width=True
        )

    # Main content area
    if generate_button:
        # Validate API keys
        if not all([openai_key, gemini_key, fal_key]):
            st.error(
                "⚠️ Please enter all required API keys (OpenAI, Gemini, and Fal.ai) in the sidebar."
            )
            return

        # Validate product inputs
        if not all([product_name, product_description, uploaded_file]):
            st.error("Please fill in all required fields and upload a product image.")
            return

        # Initialize clients with user-provided keys
        try:
            openai_client, gemini_client = ai.initialize_clients(
                openai_key, gemini_key, fal_key
            )
        except Exception as e:
            st.error(f"Error initializing API clients: {str(e)}")
            st.info("Please check that your API keys are correct and try again.")
            return

        # Create progress container
        progress_container = st.container()
        results_container = st.container()

        with progress_container:
            st.header("🔄 Workflow Progress")

            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Step 1: Generate Persona Profile
            status_text.text("Step 1/5: Generating AI persona profile...")
            progress_bar.progress(20)

            try:
                persona_profile = ai.generate_persona_profile(
                    product_name, product_description, openai_client
                )

                with st.expander("👤 Generated Persona Profile", expanded=False):
                    st.text(persona_profile)

            except Exception as e:
                st.error(f"Error generating persona: {str(e)}")
                return

            # Step 2: Generate Creator Image
            status_text.text("Step 2/5: Creating creator image...")
            progress_bar.progress(40)

            try:
                # Upload product image to fal
                product_image_bytes = uploaded_file.read()
                product_image_pil = Image.open(BytesIO(product_image_bytes))

                # Save temporarily for fal upload
                temp_path = "temp_product.png"
                product_image_url = ai.upload_product_image(
                    product_image_pil, temp_path
                )

                # Generate creator image
                creator_image_url = ai.generate_creator_image(persona_profile, fal_key)

                # Display creator image
                st.image(
                    creator_image_url, caption="Generated Creator Image", width=300
                )

            except Exception as e:
                st.error(f"Error generating creator image: {str(e)}")
                return

            # Step 3: Generate First Frame
            status_text.text("Step 3/5: Creating first frame with product...")
            progress_bar.progress(60)

            try:
                first_frame_url = ai.generate_first_frame(
                    creator_image_url, product_image_url, fal_key
                )

                # Display first frame
                st.image(
                    first_frame_url,
                    caption="First Frame - Creator with Product",
                    width=300,
                )

            except Exception as e:
                st.error(f"Error generating first frame: {str(e)}")
                return

            # Step 4: Generate Video Script
            status_text.text("Step 4/5: Creating video script...")
            progress_bar.progress(80)

            try:
                video_script = ai.generate_video_script(
                    product_name, product_description, persona_profile, openai_client
                )

            except Exception as e:
                st.error(f"Error generating video script: {str(e)}")
                return

            # Step 5: Generate Video
            status_text.text(
                "Step 5/5: Generating video (this may take 5-10 minutes)..."
            )
            progress_bar.progress(90)

            try:
                # Download first frame image from URL to local file
                first_frame_response = requests.get(first_frame_url)
                first_frame_local_path = "temp_first_frame.jpg"
                with open(first_frame_local_path, "wb") as f:
                    f.write(first_frame_response.content)

                # Create a status container for video generation progress
                video_status = st.empty()
                video_status.info(
                    "⏳ Generating video... This process includes:\n- First half (8 seconds): ~2-3 minutes\n- Second half (8 seconds): ~2-3 minutes\n\nPlease wait, this may take several minutes."
                )

                # Generate video using the function from ai_google.py
                # The function handles both halves internally and is synchronous
                full_video_path = ai.generate_video(
                    script_lines=video_script,
                    first_frame_path=first_frame_local_path,
                    gemini_client=gemini_client,
                    output_dir=".",
                )

                # Store video path in session state for display
                st.session_state["full_video_path"] = full_video_path

                # Clear the status message once complete
                video_status.empty()
                progress_bar.progress(100)

            except Exception as e:
                st.error(f"Error generating video: {str(e)}")
                # Clean up temporary files
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                if os.path.exists(first_frame_local_path):
                    os.remove(first_frame_local_path)
                return

            # Clean up temporary files
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if os.path.exists(first_frame_local_path):
                os.remove(first_frame_local_path)

            status_text.text("✅ Workflow completed successfully!")

        # Display results
        with results_container:
            st.header("🎯 Results")

            # Video section (full width at top)
            try:
                # Check session state first, then locals as fallback
                video_path = st.session_state.get("full_video_path", None)
                if not video_path:
                    # Try to get from locals if available
                    video_path = locals().get("full_video_path", None)

                if video_path and os.path.exists(video_path):
                    st.subheader("🎬 Generated Video")
                    video_file = open(video_path, "rb")
                    video_bytes = video_file.read()
                    st.video(video_bytes)

                    # Download button for video
                    st.download_button(
                        label="📥 Download Video",
                        data=video_bytes,
                        file_name="ugc_video.mp4",
                        mime="video/mp4",
                        type="primary",
                    )
                    video_file.close()
            except Exception as e:
                st.warning(f"Video display error: {str(e)}")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📸 First Frame")
                st.image(
                    first_frame_url,
                    caption="First Frame of the Video",
                    use_container_width=True,
                )

                # Download button for first frame
                response = requests.get(first_frame_url)
                st.download_button(
                    label="📥 Download First Frame",
                    data=response.content,
                    file_name="first_frame.jpg",
                    mime="image/jpeg",
                )

            with col2:
                st.subheader("📝 Video Script")
                st.text_area(
                    "Generated Script", value=video_script, height=400, disabled=True
                )

                # Download button for script
                st.download_button(
                    label="📥 Download Script",
                    data=video_script,
                    file_name="video_script.txt",
                    mime="text/plain",
                )

            # Additional information
            st.subheader("ℹ️ Workflow Summary")
            st.info(
                f"""
            **Product:** {product_name}
            **Creator Image:** Generated based on AI persona
            **First Frame:** Creator holding the product
            **Script:** 12-second UGC-style video script
            **Video:** Full 16-second UGC video generated
            """
            )

    else:
        # Show instructions when not generating
        st.markdown(
            """
        ## 🎯 How it works
        
        This AI-powered workflow creates authentic User-Generated Content by:
        
        1. **👤 AI Persona Generation** - Creates a detailed profile of the ideal creator
        2. **🖼️ Creator Image** - Generates a photorealistic image of the creator
        3. **📸 First Frame** - Creates the opening shot with creator holding your product
        4. **📝 Video Script** - Writes a natural 12-second UGC video script
        5. **🎬 Video Generation** - Generates a full 16-second UGC video using Veo 3.1
        
        ### 📋 Requirements
        - Product name and description
        - Product image (PNG, JPG, or JPEG)
        - OpenAI API key (for persona and script generation)
        - Gemini API key (for video generation)
        - Fal.ai API key (for image generation and editing)
        
        ### 🚀 Getting Started
        1. Enter your API keys in the sidebar (OpenAI, Gemini, and Fal.ai)
        2. Fill in the product details in the sidebar
        3. Upload your product image
        4. Click "Generate UGC Content"
        5. Wait for the AI to complete all steps
        6. Download your results!

        ### 🎬 Example Workflow Output
        Here's an example of what the workflow generates:
        """
        )

        # Example workflow output section
        example_video_path = "./example_generation.mp4"
        if os.path.exists(example_video_path):
            st.divider()
            st.subheader("🎬 Example Workflow Output")
            st.markdown("Here's an example of what the workflow generates:")

            try:
                video_file = open(example_video_path, "rb")
                video_bytes = video_file.read()
                st.video(video_bytes)
                video_file.close()
            except Exception as e:
                st.warning(f"Could not display example video: {str(e)}")


if __name__ == "__main__":
    main()
