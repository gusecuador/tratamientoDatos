from flask import Flask, Response
import requests
import json
import logging

app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def hello_world():
    return "<p>Hola mundo!</p>"


@app.route("/get-price/<ticker>")
def get_price(ticker):
    #url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=price%2CsummaryDetail%2CpageViews%2CfinancialsTemplate"
    url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/AAPL?modules=assetProfile%2CsummaryProfile%2CsummaryDetail%2CesgScores%2Cprice%2CincomeStatementHistory%2CincomeStatementHistoryQuarterly%2CbalanceSheetHistory%2CbalanceSheetHistoryQuarterly%2CcashflowStatementHistory%2CcashflowStatementHistoryQuarterly%2CdefaultKeyStatistics%2CfinancialData%2CcalendarEvents%2CsecFilings%2CrecommendationTrend%2CupgradeDowngradeHistory%2CinstitutionOwnership%2CfundOwnership%2CmajorDirectHolders%2CmajorHoldersBreakdown%2CinsiderTransactions%2CinsiderHolders%2CnetSharePurchaseActivity%2Cearnings%2CearningsHistory%2CearningsTrend%2CindustryTrend%2CindexTrend%2CsectorTrend"
    
    response = requests.get(url)
    company_info = response.json()
    app.logger.info(f"Requested ticker: {ticker}")

    if response.status_code > 400:
        app.logger.info(f"Yahoo has problem with ticker: {ticker}.")
        app.logger.info(f"Yahoo status code: {response.status_code}.")
        return Response({}, status=404, mimetype='application/json')

    app.logger.info(company_info)

    try:
        price = company_info['quoteSummary']['result'][0]['price']['regularMarketPrice']['raw']
        company_name = company_info['quoteSummary']['result'][0]['price']['longName']
        exchange = company_info['quoteSummary']['result'][0]['price']['exchangeName']
        currency = company_info['quoteSummary']['result'][0]['price']['currency']

        result = {
            "price": price,
            "name": company_name,
            "exchange": exchange,
            "currency": currency
        }
        app.logger.info(result)

        return Response(json.dumps(result), status=200, mimetype='application/json')
    except (KeyError, TypeError):
        return Response({}, status=404, mimetype='application/json')
    except Exception as e:
        app.logger.error("Exception occurred", exc_info=True)


if __name__ == '__main__':
    app.run()
