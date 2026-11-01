from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Quick Voucher Supplier API")

transactions = {}


class VoucherRequest(BaseModel):
    clientReference: str
    productId: str
    amount: float


@app.post("/voucher/issue", status_code=201)
def issue_voucher(request: VoucherRequest):
    transaction_id = f"QV_{len(transactions) + 1001}"

    transaction = {
        "transactionId": transaction_id,
        "clientReference": request.clientReference,
        "productId": request.productId,
        "amount": request.amount,
        "status": "Pending",
        "voucherCode": None,
    }

    transactions[transaction_id] = transaction

    return transaction


@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: str):
    if transaction_id not in transactions:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transactions[transaction_id]