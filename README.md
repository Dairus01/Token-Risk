
# Token Risk Screener

A powerful tool for crypto investors, developers, and auditors to assess the risk profile of any ERC-20 token across multiple EVM chains. This dashboard fetches live data from Sim API to analyze token holder distribution, market stats, and concentration metrics, providing a clear risk score and safety verdict to guide smarter trading decisions.



## Badges

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)



## API Reference

#### Get Token Holders

```http
  GET /v1/evm/token-holders/{chain_id}/{token_address}
```

| Parameter       | Type     | Description                                        |
| :-------------- | :------- | :------------------------------------------------- |
| `chain_id`      | `int`    | **Required.** EVM chain ID (e.g. `1` for Ethereum) |
| `token_address` | `string` | **Required.** Contract address of the token        |
| `limit`         | `int`    | Optional. Max number of holders to fetch           |
| `X-Sim-Api-Key` | `string` | **Required.** Your API key in the header           |


#### Get Token Info

```http
  GET /v1/evm/token-info/{token_address}
```

| Parameter       | Type     | Description                                 |
| :-------------- | :------- | :------------------------------------------ |
| `token_address` | `string` | **Required.** Contract address of the token |
| `chain_ids`     | `string` | Optional. Comma-separated list of chain IDs |
| `X-Sim-Api-Key` | `string` | **Required.** Your API key in the header    |



## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`X_SIM_API_KEY=your_sim_api_key_here
`



## Features

- Token risk scoring based on holder distribution
- Market data: price, supply, and market cap
- Interactive pie charts and top holders table
- Multi-chain support (50+ EVM chains)
- Token logo and metadata display
- Streamlit-powered responsive dashboard
- Secure API key integration via environment variables


## Deployment

This project is deployed and accessible at:
```bash
https://token-risk.streamlit.app/
```

To deploy locally with Streamlit, run:

```bash
streamlit run app.py
```


## Demo

https://token-risk.streamlit.app/


## Contributing

Contributions are always welcome! t




## Feedback

If you have any feedback, please reach out to me on X : @DairusOkoh


## Acknowledgements

- [Sim API](https://sim.dune.com/) – Token data provider powering the analytics
- [Streamlit](https://streamlit.io/) – UI framework for building the dashboard
- [Plotly](https://plotly.com/python/) – Data visualization library used for pie charts
- [Pandas](https://pandas.pydata.org/) – Data



## Authors

- [@Dairus01](https://github.com/Dairus01)


## About Me
I'm a Blockchain Data Scientist focused on analyzing on-chain data to uncover insights, assess risks, and build practical tools for the crypto space. I specialize in token distribution analysis, security screening, and data-driven decision-making. I'm passionate about using data to enhance transparency, trust, and safety in Web3 ecosystems.

I'm open to collaboration on research, analytics, and product-focused blockchain projects. Let's build together.

You can connect with me on [LinkedIn](https://www.linkedin.com/in/dairus-okoh/) or follow my insights on [Twitter](https://twitter.com/dairusokoh).
