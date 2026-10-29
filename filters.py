import re

SUBREDDITS = [
    # Original
    "coinbase",
    "kraken",
    "trustwalletcommunity",
    "metamask",
    "tangem",
    "ledgerwallet",
    "phantom",
    "defi",
    "solana",
    # New exchanges
    "OKX",
    "Bybit",
    "Crypto_com",
    "kucoin",
    "gateio",
    "Bitget",
    # mexc subreddit is 404 (doesn't exist) - excluded
    # New wallets & support
    "ExodusWallet",
    # CoinbaseWallet is a private subreddit (403) - excluded
    "KrakenSupport",
    # blockchain subreddit is private/restricted (403) - excluded
    "ledger",
    "TREZOR",
    # Binance
    "binance",
]


# ── Scam / theft ─────────────────────────────────────────────────────────────
SCAM_TERMS = [
    # Direct scam statements
    "i was scammed",
    "i got scammed",
    "i've been scammed",
    "i have been scammed",
    "got scammed",
    "being scammed",
    "just got scammed",
    "crypto scam",
    "crypto scammer",
    "crypto fraud",
    # Theft
    "someone stole my crypto",
    "my crypto was stolen",
    "lost my crypto",
    "stole my crypto",
    "scam",
    "scammed",
    "hacked",
    "drain",
    "drained",
    "phishing",
    "my funds are gone",
    "my coins are gone",
    "my tokens are gone",
    "balance is zero",
    "balance went to zero",
    "funds disappeared",
    "coins disappeared",
    "tokens disappeared",
    # Hacking / compromise
    "my account was hacked",
    "account got hacked",
    "got hacked",
    "wallet was hacked",
    "wallet got hacked",
    "wallet drained",
    "wallet has been drained",
    "wallet emptied",
    "account compromised",
    "account was compromised",
    "unauthorized transaction",
    "unauthorized transfer",
    "someone accessed my account",
    "someone logged into my account",
    "seed phrase stolen",
    "private key stolen",
    "seed phrase compromised",
    "someone has my seed phrase",
    # Phishing
    "phishing",
    "fake support",
    "fake customer support",
    "impersonator",
    # Rug / exit scam
    "rug pull",
    "rugpull",
    "exit scam",
    "honeypot",
]


# ── Withdrawal problems ───────────────────────────────────────────────────────
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
    "withdrawal issue",
    "withdraw",
    "withdrawal blocked",
    "withdrawal rejected",
    "withdrawal cancelled",
    "withdrawal not arriving",
    "withdrawal not received",
    "withdrawal delayed",
    "waiting for my withdrawal",
    "funds stuck",
    "funds on hold",
    "funds frozen",
    "funds locked",
    "funds not available",
    "funds not released",
    "cannot get my funds",
    "can't get my funds",
    "can't access my funds",
    "cannot access my funds",
    "unable to access my funds",
    "cannot withdraw my funds",
    "can't withdraw my funds",
    "account frozen",
    "account locked",
    "account suspended",
    "account restricted",
    "account on hold",
    "locked out of my account",
    "can't login",
    "cannot login",
    "can't log in",
    "transaction stuck",
    "transaction pending forever",
    "pending for days",
    "pending for hours",
    "transaction not confirmed",
]


# ── Wrong transfer / send mistakes ───────────────────────────────────────────
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
    "wrong address",
    "wrong network",
    "wrong memo",
    "wrong tag",
    "sent to wrong address",
    "wrong wallet address",
    "wrong address",
    "sent to scammer",
    "sent to a scammer",
    "sent to the scammer",
    "sent funds to wrong",
    "sent money to wrong",
    "mistakenly sent",
    "accidentally transferred",
    "sent to incorrect address",
    "transferred to wrong wallet",
]


# ── Crypto terms used to confirm context ─────────────────────────────────────
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
    "ripple",
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
    "airdrop",
    "dex",
    "swap",
    "seed phrase",
    "private key",
    "smart contract",
    "trezor",
    "exodus",
    "bybit",
    "okx",
    "kucoin",
    "binance",
    "gate.io",
    "gateio",
    "bitget",
    "crypto.com",
    "defi",
    "nft",
    "seed phrase",
    "private key",
    "recovery phrase",
    "mnemonic",
    "smart contract",
    "transaction hash",
    "txid",
    "gas fee",
    "gas fees",
]


def find_matches(title, body):
    text = f"{title} {body}".lower()

    matches = []

    for term in SCAM_TERMS:
        if term in text:
            matches.append("Possible Scam / Hack")
            break

    for term in WITHDRAWAL_TERMS:
        if term in text:
            matches.append("Withdrawal / Account Problem")
            break

    for term in TRANSFER_TERMS:
        if term in text:
            matches.append("Crypto Transfer Issue")
            break

    for term in CRYPTO_TERMS:
        pattern = r"\b" + re.escape(term) + r"\b"
        if re.search(pattern, text):
            matches.append("Crypto Related")
            break

    # If no specific category matched, it is still a new post under the subreddit
    if not matches:
        matches.append("New Post")

    return matches