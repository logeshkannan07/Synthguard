
import os
import sys
import tempfile

import streamlit as st

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

from analysis.evidence_engine import SynthGuardEvidenceEngine


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SynthGuard",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# LOAD EVIDENCE ENGINE
# ============================================================

@st.cache_resource
def load_engine():
    return SynthGuardEvidenceEngine()


evidence_engine = load_engine()


# ============================================================
# HEADER
# ============================================================

st.title("🛡️ SynthGuard")

st.subheader("AI-Generated Content Detection System")

st.write(
    "SynthGuard analyzes images and text using pretrained AI detection "
    "models and provides probabilistic estimates with supporting evidence."
)

st.warning(
    "Important: Detection results are probabilistic estimates, "
    "not definitive proof that content was created by AI."
)


# ============================================================
# MODULE SELECTION
# ============================================================

st.divider()

module = st.radio(
    "Select Detection Module",
    ["🖼️ Image Detection", "📝 Text Detection"],
    horizontal=True
)


# ============================================================
# IMAGE DETECTION
# ============================================================

if module == "🖼️ Image Detection":

    st.header("🖼️ Image AI Detection")

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_file is not None:

        st.image(
            uploaded_file,
            caption=uploaded_file.name,
            use_container_width=True
        )

        if st.button("🔍 Analyze Image", type="primary"):

            temp_path = None

            try:

                # Preserve original extension
                file_extension = os.path.splitext(
                    uploaded_file.name
                )[1]

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=file_extension
                ) as temp_file:

                    temp_file.write(uploaded_file.getbuffer())
                    temp_path = temp_file.name

                with st.spinner("Analyzing image..."):

                    result = evidence_engine.analyze_image(temp_path)

                st.success("Image analysis completed.")


                # ------------------------------------------------
                # MAIN RESULT
                # ------------------------------------------------

                st.subheader("Detection Result")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Prediction",
                        result["prediction"]
                    )

                with col2:
                    st.metric(
                        "AI Probability",
                        f'{result["ai_probability"]:.2f}%'
                    )

                with col3:
                    st.metric(
                        "Real Probability",
                        f'{result["real_probability"]:.2f}%'
                    )


                # ------------------------------------------------
                # RISK
                # ------------------------------------------------

                st.subheader("Risk Assessment")

                risk = result["risk"]

                if risk == "HIGH":
                    st.error(f"🔴 HIGH RISK — {risk}")

                elif risk == "MEDIUM":
                    st.warning(f"🟠 MEDIUM RISK — {risk}")

                else:
                    st.success(f"🟢 LOW RISK — {risk}")


                # ------------------------------------------------
                # EXPLANATION
                # ------------------------------------------------

                st.subheader("Explanation")

                st.info(result["explanation"])


                # ------------------------------------------------
                # IMAGE INFORMATION
                # ------------------------------------------------

                st.subheader("Image Information")

                image_info = result.get("image_info", {})

                if image_info:

                    info_col1, info_col2 = st.columns(2)

                    with info_col1:
                        st.write(
                            "**Filename:**",
                            image_info.get(
                                "filename",
                                uploaded_file.name
                            )
                        )

                        st.write(
                            "**Format:**",
                            image_info.get("format", "Unknown")
                        )

                        st.write(
                            "**Dimensions:**",
                            image_info.get("width", "Unknown"),
                            "×",
                            image_info.get("height", "Unknown")
                        )

                    with info_col2:
                        st.write(
                            "**Color Mode:**",
                            image_info.get(
                                "color_mode",
                                "Unknown"
                            )
                        )

                        st.write(
                            "**File Size:**",
                            image_info.get(
                                "file_size_bytes",
                                "Unknown"
                            ),
                            "bytes"
                        )


                # ------------------------------------------------
                # METADATA
                # ------------------------------------------------

                st.subheader("Metadata Evidence")

                metadata = result.get("metadata", {})

                if metadata:

                    metadata_display = {
                        "EXIF Present":
                            metadata.get(
                                "has_exif",
                                "Unknown"
                            ),
                        "Camera Make":
                            metadata.get(
                                "camera_make",
                                "Not available"
                            ),
                        "Camera Model":
                            metadata.get(
                                "camera_model",
                                "Not available"
                            ),
                        "Software":
                            metadata.get(
                                "software",
                                "Not available"
                            )
                    }

                    st.json(metadata_display)

                else:
                    st.write("No metadata information available.")


                # ------------------------------------------------
                # SUPPORTING EVIDENCE
                # ------------------------------------------------

                st.subheader("Supporting Evidence")

                evidence = result.get("evidence", [])

                if evidence:

                    for item in evidence:
                        st.write("•", item)

                else:
                    st.write(
                        "No additional supporting evidence available."
                    )


            except Exception as e:

                st.error(
                    f"Error while analyzing the image: {e}"
                )

            finally:

                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)


# ============================================================
# TEXT DETECTION
# ============================================================

else:

    st.header("📝 Text AI Detection")

    user_text = st.text_area(
        "Enter or paste the text you want to analyze:",
        height=300,
        placeholder="Paste your text here..."
    )

    if st.button("🔍 Analyze Text", type="primary"):

        if not user_text.strip():

            st.warning(
                "Please enter some text before analyzing."
            )

        else:

            try:

                with st.spinner("Analyzing text..."):

                    result = evidence_engine.analyze_text(
                        user_text
                    )

                st.success("Text analysis completed.")


                # ------------------------------------------------
                # MAIN RESULT
                # ------------------------------------------------

                st.subheader("Detection Result")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Prediction",
                        result["prediction"]
                    )

                with col2:
                    st.metric(
                        "AI Probability",
                        f'{result["ai_probability"]:.2f}%'
                    )

                with col3:
                    st.metric(
                        "Human Probability",
                        f'{result["human_probability"]:.2f}%'
                    )


                # ------------------------------------------------
                # RISK
                # ------------------------------------------------

                st.subheader("Risk Assessment")

                risk = result["risk"]

                if risk == "HIGH":
                    st.error(f"🔴 HIGH RISK — {risk}")

                elif risk == "MEDIUM":
                    st.warning(f"🟠 MEDIUM RISK — {risk}")

                else:
                    st.success(f"🟢 LOW RISK — {risk}")


                # ------------------------------------------------
                # EXPLANATION
                # ------------------------------------------------

                st.subheader("Explanation")

                st.info(result["explanation"])


                # ------------------------------------------------
                # ANALYZED TEXT
                # ------------------------------------------------

                with st.expander("View Analyzed Text"):

                    st.write(user_text)


            except Exception as e:

                st.error(
                    f"Error while analyzing the text: {e}"
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SynthGuard — AI-Generated Content Detection System"
)

st.caption(
    "Results are probabilistic estimates and should not be "
    "treated as absolute proof of AI generation."
)
