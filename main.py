import fitz
from PIL import Image
import io
from PyPDF2 import PdfReader
import PyPDF2
import streamlit as st
import anthropic
import base64
from fpdf import FPDF
from io import BytesIO

# Importing your custom analysis functions
from analyse_car_accident_images import analyze_image
from image_encoder import encode_image


prompts = ["You are a car insurance agent. Your job is to create a comprehensive report analyzing the documents\
            which includes car accident report, a detailed description of the damaged car parts(car repair estimate)\
            and insurance claim document. \
            Your goal is to use this information and infer the type of damage and make a payout estimate",
           "As a claims adjuster, review the accident image, repair cost estimate image, and insurance claim document image provided. Determine the cause of the accident, assess liability, and calculate the appropriate payout amount. Provide a detailed analysis and recommendation based on the evidence in these documents.",
           "You're a vehicle damage assessor. Analyze the police report (accident image), vehicle photos, and mechanic's repair cost estimate image. Prepare a report detailing the extent of damage, likely cause based on the evidence, and estimated repair cost for the insurance claim.",
           "Act as an expert witness evaluating this disputed accident claim. Review the accident image, repair estimates image, and insurance claim documents. Provide an objective analysis determining fault based on the evidence, assessing validity of claimed damages, and estimating fair repair/replacement costs.",
           "As an AI claims assistant, streamline this claim by analyzing the accident image, repair cost estimate image, and insurance claim documents provided. Generate a report summarizing the incident based on the evidence, identifying the responsible party, detailing damages, and recommending a payout amount per the coverage."]

# Anthropi API key
# Note: Please input your Claude api key here if in case it gives error as low credits.
api_k = "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"


def create_accident_report_pdf(accident_report, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)

    # Write the long text using multi_cell
    # Assuming line spacing of 5 mm
    pdf.multi_cell(200, 5, txt=accident_report)

    pdf.output(filename)

    print(f'PDF report {filename} created successfully!')

# Generate report content


def report_generation(accident_image, repair_estimate, insurance_claim):
    report_content = "Accident Analysis Results:\n"

    report_content += "Car Accident Image Analysis Result:\n"

    print(encode_image(accident_image))

    accident_image_analysis = analyze_image(encode_image(
        accident_image), "Visually describe this car accident. Explain the damage on the car. Return a detailed accident report.")
    report_content += accident_image_analysis

    report_content += "\nRepair Estimate Analysis Result:\n"
    repair_estimate_analysis = analyze_image(encode_image(
        repair_estimate), "Provide concise analysis for car repair estimate document")
    report_content += repair_estimate_analysis

    report_content += "\nInsurance Claim Analysis Result:\n"
    insurance_claim_analysis = analyze_image(
        encode_image(insurance_claim), "Provide concise analysis")
    report_content += insurance_claim_analysis

    return report_content


def main():
    # Streamlit interface
    st.title("Car Accident Report Generator")

    st.subheader("Upload Images")

    accident_image = st.file_uploader(
        "Upload Car Accident Image", type=["jpg", "jpeg", "png"])
    if accident_image:
        st.image(Image.open(accident_image),
                 caption="Car Accident Image", use_column_width=True)

        # print(encode_image(accident_image))
        # print("h")
    repair_estimate = st.file_uploader(
        "Upload Car Repair Estimate Document", type=["jpg", "jpeg", "png"])
    if repair_estimate:
        st.image(Image.open(repair_estimate),
                 caption="Car Repair Estimate", use_column_width=True)

    insurance_claim = st.file_uploader(
        "Upload Car Insurance Claim Document", type=["jpg", "jpeg", "png"])
    if insurance_claim:
        st.image(Image.open(insurance_claim),
                 caption="Car Insurance Claim", use_column_width=True)

        if st.button("Generate Report"):
            with st.spinner("Generating report..."):

                report_content = "Accident Analysis Results:\n"
                report_content += "Car Accident Image Analysis Result:\n"

                print(encode_image(accident_image))

                accident_image_analysis = analyze_image(encode_image(
                    accident_image), "Visually describe this car accident. Explain the damage on the car. Return a detailed accident report.")

                report_content += accident_image_analysis

                report_content += "\nRepair Estimate Analysis Result:\n"

                repair_estimate_analysis = analyze_image(encode_image(
                    repair_estimate), "Provide concise analysis for car repair estimate document")

                report_content += repair_estimate_analysis

                report_content += "\nInsurance Claim Analysis Result:\n"

                insurance_claim_analysis = analyze_image(
                    encode_image(insurance_claim), "Provide concise analysis")
                report_content += insurance_claim_analysis

                # report_content = report_generation(accident_image, repair_estimate, insurance_claim)
                create_accident_report_pdf(
                    report_content, "car_accident_report.pdf")
                st.success("Report generated successfully!")
                st.download_button("Download Report", data=open(
                    "car_accident_report.pdf", "rb"), file_name="car_accident_report.pdf", mime="application/pdf")


if __name__ == "__main__":
    main()
