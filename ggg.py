import telebot
from telebot import types
import requests
import time

bot = telebot.TeleBot("7308362259:AAHWUn1p_ju-wJqRvgXYG3bUyep36QYr0es")

# Список ID администраторов (замените на свои ID)
ADMIN_IDS = [1241864384, 7593884818, 7252193120]

crypta = {
    "BTC": "btc-bitcoin",
    "ETH": "eth-ethereum",
    "BNB": "bnb-binance-coin",
    "SOL": "sol-solana",
    "XRP": "xrp-xrp",
    "ADA": "ada-cardano",
    "DOGE": "doge-dogecoin",
    "DOT": "dot-polkadot",
    "SHIB": "shib-shiba-inu",
    "MATIC": "matic-polygon",
    "LTC": "ltc-litecoin",
    "AVAX": "avax-avalanche",
    "LINK": "link-chainlink",
    "ATOM": "atom-cosmos",
    "XLM": "xlm-stellar",
    "ALGO": "algo-algorand",
    "VET": "vet-vechain",
    "FIL": "fil-filecoin",
    "THETA": "theta-theta-network",
    "XTZ": "xtz-tezos",
    "USDT": "usdt-tether",
    "USDC": "usdc-usd-coin",
    "BUSD": "busd-binance-usd",
    "DAI": "dai-dai",
    "AAVE": "aave-aave",
    "COMP": "comp-compound",
    "MKR": "mkr-maker",
    "SNX": "snx-synthetix-network-token",
    "CRV": "crv-curve-dao-token",
    "UNI": "uni-uniswap",
    "SUSHI": "sushi-sushiswap",
    "YFI": "yfi-yearn-finance",
    "1INCH": "1inch-1inch",
    "REN": "ren-republic-protocol",
    "BAL": "bal-balancer",
    "UMA": "uma-uma",
    "BAND": "band-band-protocol",
    "NMR": "nmr-numeraire",
    "OGN": "ogn-origin-protocol",
    "MANA": "mana-decentraland",
    "SAND": "sand-the-sandbox",
    "AXS": "axs-axie-infinity",
    "ENJ": "enj-enjin-coin",
    "FLOW": "flow-flow",
    "WAXP": "wax-wax",
    "GALA": "gala-gala",
    "IMX": "imx-immutable-x",
    "APE": "ape-apecoin",
    "RARI": "rari-rarible",
    "OP": "op-optimism",
    "ARB": "arb-arbitrum",
    "METIS": "metis-metis-token",
    "BOBA": "boba-boba-network",
    "LRC": "lrc-loopring",
    "GRT": "grt-the-graph",
    "TRB": "trb-tellor",
    "DIA": "dia-dia",
    "ZEC": "zec-zcash",
    "XMR": "xmr-monero",
    "DASH": "dash-dash",
    "ZEN": "zen-horizen",
    "SCRT": "scrt-secret",
    "FLOKI": "floki-floki-inu",
    "BABYDOGE": "baby-baby-doge-coin",
    "ELON": "elon-dogelon-mars",
    "KISHU": "kishu-kishu-inu",
    "EOS": "eos-eos",
    "NEO": "neo-neo",
    "KLAY": "klay-klaytn",
    "TWT": "twt-trust-wallet-token",
    "RUNE": "rune-thorchain",
    "CHZ": "chz-chiliz",
    "HOT": "hot-holo",
    "WAVES": "waves-waves",
    "OMG": "omg-omisego",
    "ICX": "icx-icon",
    "NANO": "nano-nano",
    "SC": "sc-siacoin",
    "ZIL": "zil-zilliqa",
    "RVN": "rvn-ravencoin",
    "ONE": "one-harmony",
    "IOST": "iost-iost",
    "CELO": "celo-celo",
    "AR": "ar-arweave",
    "KSM": "ksm-kusama",
    "ANKR": "ankr-ankr",
    "STORJ": "storj-storj",
    "HNT": "hnt-helium",
    "AMP": "amp-amp",
    "TFUEL": "tfuel-theta-fuel",
    "TON": "ton-toncoin",
    "PYTH": "pyth-pyth-network",
    "SEI": "sei-sei",
    "SUI": "sui-sui",
    "ORDI": "ordi-ordinals",
    "MINA": "mina-mina",
    "INJ": "inj-injective",
    "RNDR": "rndr-render-token",
    "FET": "fet-fetch-ai",
    "AGIX": "agix-singularitynet",
    "OCEAN": "ocean-ocean-protocol",
    "GMT": "gmt-stepn",
    "APT": "apt-aptos",
    "BLUR": "blur-blur",
    "LDO": "ldo-lido-dao",
    "STX": "stx-stacks",
    "HBAR": "hbar-hedera",
    "NEAR": "near-near",
    "QNT": "qnt-quant",
    "ICP": "icp-internet-computer",
    "CRO": "cro-cronos",
    "FTM": "ftm-fantom",
    "EGLD": "egld-multiversx",
    "KAVA": "kava-kava",
    "ROSE": "rose-oasis-network",
    "OSMO": "osmo-osmosis",
    "JUP": "jup-jupiter",
    "WIF": "wif-dogwifcoin",
    "BONK": "bonk-bonk",
    "PEPE": "pepe-pepe",
    "MEME": "meme-memecoin"
}


def get_crypto_price(crypto_id):
    try:
        url = f"https://api.coinpaprika.com/v1/tickers/{crypto_id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data['quotes']['USD']['price'])
    except Exception as e:
        print(f"Ошибка при получении цены: {e}")
        return None


def is_admin(user_id):
    """Проверяет, является ли пользователь администратором"""
    return user_id in ADMIN_IDS


@bot.inline_handler(lambda query: len(query.query) > 0)
def inline_query(query):
    try:
        # Проверяем, является ли пользователь администратором
        if not is_admin(query.from_user.id):
            # Если не админ - показываем сообщение об ошибке
            error_article = types.InlineQueryResultArticle(
                id='access_denied',
                title="Доступ запрещен",
                description="Инлайн-режим доступен только администраторам",
                input_message_content=types.InputTextMessageContent(
                    message_text="❌ Извините, эта функция доступна только администраторам."
                )
            )
            bot.answer_inline_query(query.id, [error_article])
            return

        # Если пользователь админ - выполняем основную логику
        parts = query.query.split()
        if len(parts) < 2:
            raise ValueError("Недостаточно параметров")

        amount = float(parts[0].strip())
        payment_link = parts[1].strip()
        currency = parts[2].strip().upper() if len(parts) > 2 else "USDT"

        if not payment_link.startswith(('http://', 'https://')):
            raise ValueError("Ссылка должна начинаться с http:// или https://")

        crypto_id = crypta.get(currency)
        if not crypto_id:
            raise ValueError(f"Валюта {currency} не поддерживается")

        price_usd = get_crypto_price(crypto_id)
        if price_usd is None:
            raise ValueError(f"Не удалось получить курс для {currency}")

        total_usd = amount * price_usd

        image_url = f"https://imggen.send.tg/checks/image?asset={currency}&asset_amount={amount}&fiat=USD&fiat_amount={total_usd:.2f}&main=asset"
        cryptobot_url = "https://t.me/CryptoBotRU/23"

        html_message = (
            f'<tg-emoji emoji-id="5438562476692087643">🦋</tg-emoji><a href="{image_url}"> </a><a href="{cryptobot_url}">Чек</a> на <b><tg-emoji emoji-id="5215699136258524363">🪙</tg-emoji> {amount} {currency}</b> '
            f"(${total_usd:.2f})."
        )

        button_text = f"Получить {amount} {currency}"
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text=button_text, url=payment_link)
        keyboard.add(url_button)

        article = types.InlineQueryResultArticle(
            id='1',
            title="Создать чек",
            description=f"Чек на {amount} {currency} (${total_usd:.2f})",
            input_message_content=types.InputTextMessageContent(
                message_text=html_message,
                parse_mode='HTML'
            ),
            reply_markup=keyboard
        )

        bot.answer_inline_query(query.id, [article])

    except ValueError as ve:
        bot.answer_inline_query(query.id, [types.InlineQueryResultArticle(
            id='error',
            title="Ошибка",
            description=str(ve),
            input_message_content=types.InputTextMessageContent(
                message_text=str(ve)
            )
        )])
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.answer_inline_query(query.id, [types.InlineQueryResultArticle(
            id='error',
            title="Ошибка",
            description="Произошла ошибка",
            input_message_content=types.InputTextMessageContent(
                message_text="Произошла ошибка, попробуйте позже"
            )
        )])


def run_bot():
    while True:
        try:
            print("Запускаем бота...")
            # Используем skip_pending=True для пропуска ожидающих обновлений
            bot.polling(none_stop=True, interval=0, timeout=20, skip_pending=True)
        except Exception as e:
            print(f"Ошибка в работе бота: {e}")
            time.sleep(5)
            continue


if __name__ == '__main__':
    print("Бот запущен в бесконечном режиме...")
    print(f"Администраторы: {ADMIN_IDS}")

    # Перед запуском убедитесь, что другие процессы завершены
    print("Убедитесь, что другие экземпляры бота завершены...")
    time.sleep(2)

    run_bot()