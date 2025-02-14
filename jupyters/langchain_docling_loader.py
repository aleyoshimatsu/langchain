from datetime import datetime, timedelta
import json
import yaml

# from docling.chunking import HybridChunker
from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType

from docling.backend.docling_parse_backend import DoclingParseDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    EasyOcrOptions,
    OcrMacOptions,
    PdfPipelineOptions,
    RapidOcrOptions,
    TesseractCliOcrOptions,
    TesseractOcrOptions,
    AcceleratorOptions,
    AcceleratorDevice
)
from docling.datamodel.settings import settings
from docling.document_converter import DocumentConverter, PdfFormatOption

from docling.chunking import HybridChunker

import os

# Using current time
print (f"initial_date: {datetime.now()}")

OCR = True


do_ocr: bool = OCR

do_table_structure: bool = True
generate_page_images: bool = False
generate_picture_images: bool = False

# Explicitly set the accelerator
accelerator_options = AcceleratorOptions(
    num_threads=8, device=AcceleratorDevice.AUTO
)
# accelerator_options = AcceleratorOptions(
#     num_threads=8, device=AcceleratorDevice.CPU
# )
# accelerator_options = AcceleratorOptions(
#     num_threads=8, device=AcceleratorDevice.MPS
# )
# accelerator_options = AcceleratorOptions(
#     num_threads=8, device=AcceleratorDevice.CUDA
# )

do_cell_matching: bool = True

pipeline_options = PdfPipelineOptions(
    do_ocr=do_ocr,
    do_table_structure=do_table_structure,
    generate_page_images=generate_page_images,
    generate_picture_images=generate_picture_images,
    accelerator_options = accelerator_options,
)
pipeline_options.table_structure_options.do_cell_matching = do_cell_matching

force_full_page_ocr: bool = OCR

# Any of the OCR options can be used:EasyOcrOptions, TesseractOcrOptions, TesseractCliOcrOptions, OcrMacOptions(Mac only), RapidOcrOptions
# ocr_options = EasyOcrOptions(force_full_page_ocr=force_full_page_ocr)
# ocr_options = TesseractOcrOptions(force_full_page_ocr=force_full_page_ocr)
# ocr_options = OcrMacOptions(force_full_page_ocr=force_full_page_ocr)
# ocr_options = RapidOcrOptions(force_full_page_ocr=force_full_page_ocr)
ocr_options = TesseractCliOcrOptions(force_full_page_ocr=force_full_page_ocr, lang=["Latin"])
pipeline_options.ocr_options = ocr_options

# Enable the profiling to measure the time spent
settings.debug.profile_pipeline_timings = True

doc_converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)


FILE_PATH_ASSEMBLEIA = '../files/BRPVSCCRI3Y2-ASS31012025V01-000829323.pdf'
FILE_PATH_ASSEMBLEIA_NAO_INSTALADA = '../files/BRASTECRI0C3-ASS04022025V01-000830908.pdf'
FILE_PATH_ASSEMBLEIA_OCR = '../files/23A1772203-ASS04022025V01-000831063.pdf'
FILE_PATH_TS = '../files/831141.pdf'
FILE_PATH_TS_2 = '../files/24F1234491-TDS07062024V01-000675608.pdf'
FILE_PATH_TS_CRA = '../files/797444.pdf'
FILE_PATH_TS_3 = '../files/018759000101010.pdf'
FILE_PATH_TS_4 = '../files/819915.pdf'
FILE_PATH_TS_5 = '../files/CRA02400DL4-TDS17122024V01-000803501.pdf'

FILE_PATH_ESCRITURA = '../files/676706.pdf'

FILE_PATH = FILE_PATH_TS_5

EMBED_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"

loader = DoclingLoader(
    converter=doc_converter,
    file_path=FILE_PATH,
    export_type=ExportType.MARKDOWN,
    chunker=HybridChunker(tokenizer=EMBED_MODEL_ID),
)

print(f"loading {FILE_PATH}")
docs = loader.load()

str_docs = "\n\n ------------".join(doc.page_content for doc in docs)

try:
    txt_file = FILE_PATH.replace('.pdf', '.txt')
    with open(txt_file, "w") as f:
        print(f"saving {txt_file}")
        f.write(str_docs)
        # Using current time
        print(f"final_date: {datetime.now()}")
except FileExistsError:
    print("Already exists.")