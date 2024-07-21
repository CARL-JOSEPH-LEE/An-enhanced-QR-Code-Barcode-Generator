
# Enhanced QR Code & Barcode Generator

## Overview

The Enhanced QR Code & Barcode Generator is a robust and versatile application developed using Python and the Tkinter library. This tool allows users to generate various types of barcodes and QR codes, customize their appearance, preview them, and save them as image files. The supported formats include QR Code, EAN13, Code128, Code39, UPCA, ISBN13, PZN, JAN, DataMatrix, Aztec, and PDF417.

## Features

-   **QR Code Generation**: Create QR codes with customizable versions, error correction levels, box sizes, and border sizes.
-   **Barcode Generation**: Generate different types of barcodes with adjustable module width, module height, font size, and text distance.
-   **DataMatrix, Aztec, and PDF417 Codes**: Support for additional 2D barcode formats.
-   **Color Customization**: Choose custom fill and background colors for the codes.
-   **Preview Functionality**: Preview the generated codes before saving.
-   **Save Options**: Save the generated codes as PNG, JPG, or SVG files.

## Installation

To run the Enhanced QR Code & Barcode Generator, you need to install the required dependencies. Follow these steps:

1.  **Clone the repository**:
    
    `git clone https://github.com/CARL-JOSEPH-LEE/qr-barcode-generator.git
    cd qr-barcode-generator` 
    
2.  **Create a virtual environment**:
    
    `python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate` 
    
3.  **Install the dependencies**:
    
    `pip install -r requirements.txt` 
    

## Requirements

-   Python 3.7 or higher
-   tkinter
-   qrcode
-   python-barcode
-   pylibdmtx
-   pillow
-   pdf417gen
-   pyqrcodeng

You can install the dependencies via `pip`:

`pip install tkinter qrcode python-barcode pylibdmtx pillow pdf417gen pyqrcodeng` 

## Usage

To run the application, execute the following command in your terminal:

`python main.py` 

### User Interface

1.  **Select Code Type**: Choose the type of code you want to generate from the dropdown menu.
2.  **Enter Data**: Input the data you want to encode.
3.  **QR Code Settings** (if applicable):
    -   Version (1-40)
    -   Error Correction Level (L, M, Q, H)
    -   Box Size
    -   Border Size
4.  **Barcode Settings** (if applicable):
    -   Module Width
    -   Module Height
    -   Font Size
    -   Text Distance
5.  **Color Customization**:
    -   Fill Color
    -   Background Color
6.  **Generate or Preview**:
    -   Click "Generate" to save the code as an image file.
    -   Click "Preview" to see a preview of the code.

## Screenshots

## Contribution

Contributions are welcome! If you have suggestions for improvements or new features, feel free to create an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements

-   The [qrcode](https://pypi.org/project/qrcode/) library for QR code generation.
-   The [python-barcode](https://pypi.org/project/python-barcode/) library for barcode generation.
-   The [pylibdmtx](https://pypi.org/project/pylibdmtx/) library for DataMatrix code generation.
-   The [Pillow](https://pypi.org/project/Pillow/) library for image processing.
-   The [pdf417gen](https://pypi.org/project/pdf417gen/) library for PDF417 code generation.
-   The [pyqrcodeng](https://pypi.org/project/pyqrcodeng/) library for Aztec code generation."# qr-barcode-generator" 
