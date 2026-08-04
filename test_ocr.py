from ocr import read_receipt


text = read_receipt(
    r"B:\Expense-Tracker-Pro\receipt.png"
)


print(text)