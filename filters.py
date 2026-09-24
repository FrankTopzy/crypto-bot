SUBREDDITS = [
    "coinbase",
    "kraken",
    "trustwalletcommunity",
    "metamask",
    "tangem",
    "ledgerwallet",
    "phantom",
    "defi",
    "solana",
]


SCAM_TERMS = [
    "i was scammed",
    "i got scammed",
    "i've been scammed",
    "i have been scammed",
    "got scammed",
    "crypto scam",
    "crypto scammer",
    "someone stole my crypto",
    "my crypto was stolen",
    "lost my crypto",
    "stole my crypto",
]


WITHDRAWAL_TERMS = [
    "unable to withdraw",
    "can't withdraw",
    "cannot withdraw",
    "can't make a withdrawal",
    "withdrawal failed",
    "withdrawal stuck",
    "withdrawal pending",
    "withdrawal is pending",
    "won't let me withdraw",
    "not letting me withdraw",
]


TRANSFER_TERMS = [
    "sent crypto to another account",
    "sent crypto to the wrong account",
    "sent crypto to the wrong address",
    "sent crypto to another wallet",
    "sent crypto to the wrong wallet",
    "accidentally sent crypto",
    "transferred crypto to the wrong",
    "sent btc to the wrong",
    "sent eth to the wrong",
    "sent usdt to the wrong",
]


CRYPTO_TERMS = [
    "crypto",
    "cryptocurrency",
    "bitcoin",
    "btc",
    "ethereum",
    "eth",
    "usdt",
    "usdc",
    "solana",
    "sol",
    "bnb",
    "xrp",
    "cardano",
    "ada",
    "dogecoin",
    "doge",
    "shiba",
    "shib",
    "pepe",
    "wallet",
    "blockchain",
    "token",
    "coin",
    "metamask",
    "trust wallet",
    "coinbase",
    "kraken",
    "phantom",
    "ledger",
    "tangem",
]


def find_matches(title, body):
    text = f"{title} {body}".lower()

    matches = []

    for term in SCAM_TERMS:
        if term in text:
            matches.append("Possible Scam")
            break

    for term in WITHDRAWAL_TERMS:
        if term in text:
            matches.append("Withdrawal Problem")
            break

    for term in TRANSFER_TERMS:
        if term in text:
            matches.append("Crypto Transfer Issue")
            break

    has_crypto_context = any(
        term in text for term in CRYPTO_TERMS
    )

    if not has_crypto_context:
        return []

    return matches