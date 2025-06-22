import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from decimal import Decimal, getcontext

# ===== Configuration =====
SIM_API_KEY = st.secrets["api_key"]
HEADERS = {"X-Sim-Api-Key": SIM_API_KEY}

getcontext().prec = 50

CHAIN_ID_MAP = {
    "ethereum": 1,
    "optimism": 10,
    "cronos": 25,
    "bsc": 56,
    "linea": 59144,
    "polygon": 137,
    "fantom": 250,
    "base": 8453,
    "blast": 81457,
    "zora": 7777777,
    "scroll": 534352,
    "arbitrum": 42161,
    "avalanche": 43114,
    "celo": 42220,
    "mantle": 5000,
    "metis": 1088,
    "gnosis": 100,
    "moonbeam": 1284,
    "moonriver": 1285,
    "klaytn": 8217,
    "evmos": 9001,
    "harmony": 1666600000,
    "aurora": 1313161554,
    "okc": 66,
    "boba": 288,
    "core": 1116,
    "dogechain": 2000,
    "fuse": 122,
    "iotex": 4689,
    "kava": 2222,
    "meter": 82,
    "oasis": 42262,
    "shiden": 336,
    "sx": 416,
    "telos": 40,
    "wanchain": 888,
    "xdc": 50,
    "astar": 592,
    "btt": 199,
    "bitgert": 32520,
    "canto": 7700,
    "clv": 1024,
    "conflux": 1030,
    "exosama": 2109,
    "godwoken": 71402,
    "hydra": 77612,
    "kcc": 321,
    "milkomeda": 2001,
    "oneledger": 311752642,
    "palm": 11297108109,
    "rootstock": 30,
    "sapphire": 23294,
    "syscoin": 57,
    "velas": 106,
    "zkevm": 1101,
    "meter_testnet": 83,
    "sepolia": 11155111
}

def get_token_holders(address: str, chain: str, limit: int = 500):
    chain_id = CHAIN_ID_MAP.get(chain.lower())
    if chain_id is None:
        st.error(f"Unsupported chain: {chain}")
        return []
    url = f"https://api.sim.dune.com/v1/evm/token-holders/{chain_id}/{address.lower()}?limit={limit}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        st.error(f"Sim API {res.status_code}: {res.text}")
        return []
    return res.json().get("holders", [])

def get_token_info(address: str, chain_id: int, limit: int = 1):
    url = f"https://api.sim.dune.com/v1/evm/token-info/{address}"
    params = {"chain_ids": str(chain_id), "limit": limit}
    res = requests.get(url, headers=HEADERS, params=params)
    if res.status_code != 200:
        st.error(f"Token Info API {res.status_code}: {res.text}")
        return []
    return res.json().get("tokens", [])

def to_human(raw: int, decimals: int) -> Decimal:
    return Decimal(raw) / Decimal(10 ** decimals)

def prepare_holders(raw_list):
    processed = []
    for h in raw_list:
        processed.append({
            "wallet": h["wallet_address"],
            "raw":    int(h.get("balance", 0)),
        }
    )
    return sorted(processed, key=lambda x: x["raw"], reverse=True)

def score(holders):
    total_raw = sum(h["raw"] for h in holders)
    if total_raw == 0:
        return 0, ["Zero supply"], "AVOID – No liquidity"

    score = 100
    flags = []

    if len(holders) < 20:
        score -= 20
        flags.append("<20 holders")

    top_pct = holders[0]["raw"] / total_raw * 100
    if top_pct > 70:
        score -= 30
        flags.append("Top holder >70%")

    top20_pct = sum(h["raw"] for h in holders[:20]) / total_raw * 100
    if top20_pct > 90:
        score -= 20
        flags.append("Top20 >90%")


    verdict = "Likely Safe" if score >= 75 else "Use Caution" if score >= 50 else "AVOID – Very Risky"
    return score, flags, verdict

def create_data_bar(pct):
    color = "#FF6B6B" if pct > 70 else "#FFD166" if pct > 50 else "#4CAF50"
    return f'''
    <div style="
        background: linear-gradient(90deg, {color} {pct}%, transparent {pct}%);
        height: 24px;
        border-radius: 4px;
        border: 1px solid #e0e0e0;
        position: relative;
    ">
        <span style="
            position: absolute;
            left: 8px;
            top: 50%;
            transform: translateY(-50%);
            color: {'white' if pct > 30 else 'black'};
            font-weight: bold;
            font-size: 12px;
        ">
            {pct:.1f}%
        </span>
    </div>
    '''

st.set_page_config(page_title="Token Risk Screener", layout="wide")
st.title("Token Risk Screener")
with st.expander("ℹ️ About this dashboard", expanded=False):
    st.markdown(
        """
        <div style="
          padding: 24px;
          font-size: 18px;
          line-height: 1.6;
        ">
          <h2>About This Dashboard</h2>

          <p><strong>Token Risk Screener</strong> lets you analyze ERC-20 tokens across 57 EVM chains simultaneously.  
          Enter a token contract address and select any number of chains to compare their holder distributions, market data, and risk scores side-by-side.</p>

          <h3>Risk score (0–100)</h3>
          <p>We start at 100 and subtract:</p>
          <ul>
            <li><strong>&lt;20 holders:</strong> –20 points</li>
            <li><strong>Top holder &gt; 70%:</strong> –30 points</li>
            <li><strong>Top 20 &gt; 90%:</strong> –20 points</li>
          </ul>

          <h3>Holder distribution</h3>
          <p>See a <strong>table</strong> of the top 20 wallets with bar-charts and percentages, plus an “Others” row,  
          and a <strong>pie chart</strong> breaking out those same slices.</p>

          <h3>How to use</h3>
          <ol>
            <li>Paste the ERC-20 contract address you wish to inspect.</li>
            <li>Select one or more chains from the “Chains to compare” box.</li>
            <li>Review token metadata (price, supply, market cap), risk score, holder table, and distribution chart for each chain.</li>
          </ol>
        </div>
        """,
        unsafe_allow_html=True
    )


contract = st.text_input("Token Contract Address (0x…)")
chains = st.multiselect(
    "Chains to compare",
    options=list(CHAIN_ID_MAP.keys()),
    default=[list(CHAIN_ID_MAP.keys())[0]]
)

if contract.strip() and chains:
    with st.spinner(f"Fetching holder data for {len(chains)} chains…"):
        holders_map = {
            ch: get_token_holders(contract.strip(), ch)
            for ch in chains
        }
    
    for ch in chains:
        raw = holders_map[ch]
        if not raw:
            st.warning(f"No holder data on {ch}.")
            continue
        token_list = get_token_info(contract.strip(), CHAIN_ID_MAP[ch])
        if not token_list:
            st.error(f"No token-info on {ch}.")
            continue
        token = token_list[0]
    
        holders = prepare_holders(raw)
        token   = next((t for t in token_list if t["chain_id"] == CHAIN_ID_MAP[ch]), None)
        if not token:
            st.error(f"No token‐info on {ch}.")
            continue

        
        dec = int(token["decimals"] or 0)
        for h in holders:
            h["human"] = h["raw"] / 10**dec
        rs, flag_list, verdict = score(holders)

        
        st.subheader(f"{token['symbol']} on {ch} — {token.get('name','')}")

        raw_supply    = int(token["total_supply"])
        decimals      = token["decimals"]
        human_supply  = raw_supply / 10**decimals
        price         = token["price_usd"] or 0
        market_cap    = human_supply * price
        symbol        = token["symbol"]


        if human_supply >= 1e9:
            words = f"({human_supply/1e9:.1f} billion {symbol} tokens)"
        elif human_supply >= 1e6:
            words = f"({human_supply/1e6:.1f} million {symbol} tokens)"
        else:
            words = f"({human_supply:,.0f} {symbol} tokens)"

        st.write(f"**Price:** ${price:,.4f}")
        st.write(f"**Supply:** {human_supply:,.0f} {symbol} {words}")
        st.write(f"**Market Cap:** ${market_cap:,.2f}")

        if token.get("logo"):
            st.image(token["logo"], width=100)


        col1, col2 = st.columns(2)
        with col1:
            st.metric("Risk Score", rs)
        with col2:
            st.markdown(f"### Recommendation: **{verdict}**")
        
        for f in flag_list:
            st.warning(f)

        raw_supply  = int(token["total_supply"])
        decimals    = token["decimals"]
        full_supply = raw_supply / 10**decimals

        top20 = holders[:20]
        df    = pd.DataFrame(top20)
        df["percent"] = (df["human"] / full_supply * 100).astype(float)

        df_display = df[["wallet", "human", "percent"]].rename(columns={
            "wallet": "Wallet Address",
            "human": "Balance",
            "percent": "Percent of Total"
        })

        df_display["Balance"] = df_display["Balance"].map(lambda x: f"{x:,.4f}")
        
        df_display["Distribution"] = df["percent"].apply(create_data_bar)
        
        df_display = df_display[["Wallet Address", "Balance", "Distribution", "Percent of Total"]]

        st.subheader(" Top 20 Holders")
        st.markdown(
            df_display.style.hide(axis="index").to_html(escape=False),
            unsafe_allow_html=True
        )

        others_amount = full_supply - df["human"].sum()
        
        others_row = pd.DataFrame([{"wallet": "Others", "human": others_amount}])
        df_chart   = pd.concat([df, others_row], ignore_index=True)

        df_chart["label"] = df_chart["wallet"].apply(
            lambda a: "Others" if a == "Others" else f"{a[:6]}…{a[-4:]}"
        )

        fig = px.pie(
            df_chart,
            names="label",      
            values="human",
            title="Token Distribution (Top-20 + Others)"
        )
        fig.update_traces(textinfo="label+percent")

        fig.update_traces(automargin=True)
        fig.update_layout(
            margin=dict(t=40, b=40, l=40, r=200),
            legend=dict(
                orientation="v",
                x=1.02,
                y=0.5,
                font=dict(size=10)
            ),
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

        
        with st.expander("Full address", expanded=False):
            st.dataframe(
                df_chart[["label","wallet"]]
                .rename(columns={"label":"Short","wallet":"Full Address"})
                .set_index("Short")
            )

st.markdown("""
<style>
    /* make header sticky above Streamlit’s blur */
    table {
        width: 100% !important;
        border-collapse: collapse !important;
    }
    th, td {
        padding: 12px 15px !important;
        text-align: left !important;
        border-bottom: 1px solid #ddd !important;
    }
    thead th {
        position: sticky !important;
        top: 0 !important;
        z-index: 9999 !important;          /* outranks Streamlit’s UI */
        background-color: #f8f9fa !important;
        background-color: #2a2a2a !important;   /* dark slate */
       color: white !important;     
        font-weight: 600 !important;
    }
        /* only highlight the 3rd (Distribution) column on hover */
    table tbody tr:hover td:nth-child(3) {
        background-color: #f5f5f5 !important;
    }
</style>
""", unsafe_allow_html=True)
