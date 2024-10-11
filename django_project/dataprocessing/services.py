import fitz  # PyMuPDF
import re
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

model = AutoModelForSequenceClassification.from_pretrained("mgrella/autonlp-bank-transaction-classification-5521155", use_auth_token=False)
tokenizer = AutoTokenizer.from_pretrained("mgrella/autonlp-bank-transaction-classification-5521155", use_auth_token=False)
categories = {"0": "Subscriptions", # dataset: https://huggingface.co/mgrella/autonlp-bank-transaction-classification-5521155/blob/main/config.json
    "1": "Subscriptions",
    "2": "Subscriptions",
    "3": "Subscriptions",
    "4": "Credit Card",
    "5": "Restaurant",
    "6": "Restaurant",
    "7": "Restaurant",
    "8": "Restaurant",
    "9": "Misc.",
    "10": "Misc.",
    "11": "Gym",
    "12": "Misc.",
    "13": "Misc.",
    "14": "Misc.",
    "15": "Home Goods",
    "16": "Home Goods",
    "17": "Home Goods",
    "18": "Groceries",
    "19": "Home Payments",
    "20": "Home Payments",
    "21": "Home Goods",
    "22": "Rent",
    "23": "Home Goods",
    "24": "Home Goods",
    "25": "Shopping",
    "26": "Shopping",
    "27": "Shopping",
    "28": "Misc.",
    "29": "Shopping",
    "30": "Concerts",
    "31": "Misc.",
    "32": "Misc.",
    "33": "Misc.",
    "34": "Shopping",
    "35": "Home Payments",
    "36": "Home Payments",
    "37": "Misc.",
    "38": "Misc.",
    "39": "Misc.",
    "40": "Category.PROFITS_PROFITS",
    "41": "Misc.",
    "42": "Shopping",
    "43": "Shopping",
    "44": "Shopping",
    "45": "Shopping",
    "46": "Shopping",
    "47": "Misc.",
    "48": "Misc.",
    "49": "Misc.",
    "50": "Misc.",
    "51": "Misc.",
    "52": "Misc.",
    "53": "Misc.",
    "54": "Misc.",
    "55": "Misc.",
    "56": "Investing",
    "57": "Misc.",
    "58": "Misc.",
    "59": "",
    "60": "",
    "61": "Travel",
    "62": "Travel",
    "63": "Travel",
    "64": "Travel",
    "65": "Travel",
    "66": "Travel",
    "67": "Travel",
    "68": "Travel",
    "69": "Travel",
    "70": "Travel",
    "71": "Travel",
    "72": "Travel",
    "73": "",
    "74": "",
    "75": ""}


def extract_pdf_data(file_path):
    pdf_document = fitz.open(file_path)
    text = ""
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    pdf_document.close()
    return text

def extract_transactions(text):
    # Define regex pattern to capture date, description, and amount
    transaction_pattern = re.compile(r'(\d{2}/\d{2})\s+([A-Za-z0-9\s\-\.,&/#*(-)]+?)\s+([0-9,]+\.[0-9]{2})')
    transactions = transaction_pattern.findall(text)
    transactions_data = []

    for transaction in transactions:
        date, description, amount = transaction
        amount = float(amount.replace('$', '').replace(',', '').strip())
        transactions_data.append({
            'date': date,
            'description': categorize_description(description),
            'amount': amount,
        })
    
    return transactions_data

def categorize_description(description):
    inputs = tokenizer(description, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    
    predicted_category_idx = torch.argmax(outputs.logits, dim=1).item()
    
    return categories[str(predicted_category_idx)]
