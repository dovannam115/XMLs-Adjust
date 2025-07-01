import streamlit as st
import xml.etree.ElementTree as ET
import io
import zipfile

st.title("🧹 XML Cleaner")

uploaded_files = st.file_uploader("Upload XMLs", type="xml", accept_multiple_files=True)

if uploaded_files:
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zipf:
        for uploaded_file in uploaded_files:
            try:
                tree = ET.parse(uploaded_file)
                root = tree.getroot()

                # Xóa thẻ <DSCKS>
                for dscks in root.findall('DSCKS'):
                    root.remove(dscks)

                # Ghi ra nội dung mới vào bộ nhớ
                output = io.BytesIO()
                tree.write(output, encoding='utf-8', xml_declaration=True)
                output.seek(0)

                # Đưa file vào trong zip
                zipf.writestr(f"{uploaded_file.name.replace('.xml', '')}_cleaned.xml", output.read())
            except Exception as e:
                st.warning(f"⚠️ Lỗi xử lý file: {uploaded_file.name} ({e})")

    zip_buffer.seek(0)

    st.success("✅ Đã xử lý xong tất cả file!")

    st.download_button(
        label="📦 Tải về file ZIP chứa các XMLs",
        data=zip_buffer,
        file_name="cleaned_xml_files.zip",
        mime="application/zip"
    )
