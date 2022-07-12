# RazorpayTransactionSummaryReports
Razorpay Transaction reports automation

![alt text](https://raw.githubusercontent.com/tush4hworks/RazorpayAPIReports/main/razorpay_transactions/images/razorpay.png)

Many businesses use Razorpay as a payments solution. 
Razorpay keeps a track of every transaction and often those are audited and summarized by analysts.
Theoretically, you could get payment level info from the Razorpay dashboard. That, however, is time-consuming and error-prone.
Razorpay exposes APIs and clients to get that information programmatically. This tool wraps around that API and provides additional functionality to automatically generate summary reports.

# How-to-use

There are two ways to use this tool:
- Install wheel file from dist folder 
  - This will add a cli utility `razorpay-transactions-summary` in your virtualenv. You can run `razorpay-transactions-summary --help` to verify successful installation.  
- Clone the repo to your local disk
  - You can then invoke `python main.py --help`

# Output
A successful run will generate csv(s) with name(s) `<current_datestring>.csv` in `YYYY-MM-DD` format of `<current_datestring>`  and a corresponding `app.log` in user's home directory

# Usage
```buildoutcfg
[ razorpay-transactions-summary  generate-reports --help  ]                                                                                               

Usage: razorpay-transactions-summary generate-reports [OPTIONS]

Options:
  --mode [quick_run|backlog|schedule]
                                  [required]
  --columns-in-summary TEXT       [required]
  --days-preceding INTEGER        [default: 1]
  --polling-interval INTEGER      [default: 3600]
  --filters TEXT
  --input-json-path TEXT
  --help                          Show this message and exit.
```

# Run Modes

There are three run modes supported:
- `quickrun` - Generates current day's summary report
- `backlog` - Generates daily reports for `n` preceding-days till yesterday
- `schedule` - Starts a thread which will keep continuously polling razorpay API and updating current day's csv. It will automatically start a new csv for the following day and so on.
  - This will leave your terminal hanging with the script running continuously. You can run this process in background to avoid that and kill using `ps -eaf` later on when required.
    
# Description of Options
- `columns-in-summary`: comma separated list of columns to include in the csv. Should be one-or-more of `id,entity,amount,currency,status,method,order_id,description,international,refund_status,amount_refunded,captured,email,contact,fee,tax,error_code,error_description,error_step,error_source,error_reason,created_at`
- `days-preceding`: Applicable for backlog mode. Number of preceding days to generate report for
- `polling-interval`: Applicable for schedule mode. Seconds to sleep before next update.

# Filtering

Filtering is supported for following condition:
- equals
- not_equals
- is_in
- is_not_in
- greater_than
- less_than

Additionally, filters can be combined with `OR` / `AND` conditions as demonstrated below.

Providing filters value:
filters argument accepts a valid json as a string in the following form:
```
[
 [
  {
   "filter_type": "equals",
   "filter_column": "status",
   "filter_value": "failed"
  }
 ],
 [
  {
   "filter_type": "greater_than",
   "filter_column": "amount",
   "filter_value": "100"
  },
  {
   "filter_type": "equals",
   "filter_column": "amount",
   "filter_value": "0"
  }
 ]
]

```

Explanation:
The top level list is a list of filter-blocks.
filter-blocks are logically combined via the AND operation.
The filter specs that make up a filter-block themselves are logically combined via the OR operation.

In the preceding example, therefore it will include payments in which :

`status == failed and (amount==0 or amount>100)`

# Passing params via command line or json file
You can either pass `polling-interval, filters, days-preceding` arguments via command line or by giving path to a json file which has information in below format:
```
{
"filters": [[{"filter_type": "equals","filter_column": "status","filter_value": "failed"}]],
"polling_interval":1200,
"days_preceding":12
}

```

* Note: dashes are replaced with underscores in the json file.
* Passing via json file is helpful as updates to parameters will get reflected automatically in schedule mode.
  
# Sample Run

Before running you need to get razorpay key id and key secret from RazorPay dashboard in test/live mode and export them as following environment variables:
```buildoutcfg
export RAZORPAY_KEY_ID=xxxxxxxxxxxx
export RAZORPAY_KEY_SECRET=yyyyyyyyyyyyyyyyyyyyy
```


```buildoutcfg
razorpay-transactions-summary  generate-reports --mode backlog --days-preceding 10 --columns-in-summary id,created_at,amount,status,error_reason,error_description,error_step,order_id --filters '[
  [
    {
      "filter_type": "equals",
      "filter_column": "status",
      "filter_value": "failed"
    }
  ]
]'
2022-07-12 22:43:41,302 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - Starting Run with following properties.
2022-07-12 22:43:41,302 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - Mode: backlog
2022-07-12 22:43:41,302 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - Columns_in_summary:['id', 'created_at', 'amount', 'status', 'error_reason', 'error_description', 'error_step', 'order_id']
2022-07-12 22:43:41,302 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - Polling interval:3600
2022-07-12 22:43:41,303 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - Filters:[[{'filter_type': 'equals', 'filter_column': 'status', 'filter_value': 'failed'}]]
2022-07-12 22:43:41,303 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - Days preceding:10
2022-07-12 22:43:41,303 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - Backlog worker starting
2022-07-12 22:43:41,303 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - Filling backlog for 2022-07-02
2022-07-12 22:43:43,908 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - []
2022-07-12 22:43:43,914 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - Dataclass Generated
2022-07-12 22:43:43,915 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - Filling backlog for 2022-07-03
2022-07-12 22:43:44,529 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - []
2022-07-12 22:43:44,530 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - Dataclass Generated
2022-07-12 22:43:44,530 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - Filling backlog for 2022-07-04
2022-07-12 22:43:46,117 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - [Payment(id='pay_JpHPUxNGVrg4sz', entity='payment', amount=10.0, currency='INR', status='failed', method='card', order_id='order_JpHPTkzbeXcWZi', description='Failed Recurring Payment via Subscription', international=False, refund_status=None, amount_refunded=0, captured=False, email='tss@gmail.com', contact='+919468707417', fee=None, tax=None, error_code='BAD_REQUEST_ERROR', error_description='Subscription charge underwent an expected failure.', error_source='internal', error_step='payment_initiation', error_reason='server_error', created_at='2022-07-04 17:25:06', last4=None, network=<CardNetwork.Unknown: 'Unknown'>, issuer=None, sub_type=None, notes=[], base_amount=None, base_currency=None, vpa=None, card_id='card_JpHCuuAnUrPqUf', acquirer_data={'auth_code': None}, bank=None, wallet=None, invoice_id='inv_JpHPTiVHVcYwvA', emi=None, name=None, customer_id='cust_JpHCuqq7AfEj12', token_id='token_JpHCv1GFgeNdTA', created_at_epoch=1656935706), Payment(id='pay_JpHh9qY2zOIa4g', entity='payment', amount=5.0, currency='INR', status='failed', method='card', order_id=None, description=None, international=False, refund_status=None, amount_refunded=0, captured=False, email='tss@gmail.com', contact='+919468707417', fee=None, tax=None, error_code='BAD_REQUEST_ERROR', error_description='Payment processing cancelled by user', error_source='customer', error_step='payment_authentication', error_reason='payment_cancelled', created_at='2022-07-04 17:41:49', last4=None, network=<CardNetwork.Unknown: 'Unknown'>, issuer=None, sub_type=None, notes=[], base_amount=None, base_currency=None, vpa=None, card_id='card_JpHhAMS5GbNdm8', acquirer_data={'auth_code': None}, bank=None, wallet=None, invoice_id=None, emi=None, name=None, customer_id='cust_JpHCuqq7AfEj12', token_id='token_JpHhATmWApeiu7', created_at_epoch=1656936709), Payment(id='pay_JpFJDHFYE5L2xo', entity='payment', amount=100.0, currency='INR', status='failed', method='wallet', order_id='order_JpFIZNUOnKaXta', description='#JpFIHCyIZI9koP', international=False, refund_status=None, amount_refunded=0, captured=False, email='tanuushree04@gmail.com', contact='+919468361642', fee=None, tax=None, error_code='BAD_REQUEST_ERROR', error_description="Your payment didn't go through due to a temporary issue. Any debited amount will be refunded in 4-5 business days.", error_source='issuer', error_step='payment_authorization', error_reason='payment_failed', created_at='2022-07-04 15:21:45', last4=None, network=<CardNetwork.Unknown: 'Unknown'>, issuer=None, sub_type=None, notes=[], base_amount=None, base_currency=None, vpa=None, card_id=None, acquirer_data={'transaction_id': None}, bank=None, wallet='olamoney', invoice_id=None, emi=None, name=None, customer_id=None, token_id=None, created_at_epoch=1656928305)]
2022-07-12 22:43:46,119 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - Dataclass Generated
2022-07-12 22:43:46,119 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - Filling backlog for 2022-07-05
2022-07-12 22:43:46,554 - razorpay_transactions.payment_dataclasses.razorpay_payments - INFO - []

```

```buildoutcfg
cat ~/2022-07-04.csv 
id,created_at,amount,status,error_reason,error_description,error_step,order_id
pay_JpHPUxNGVrg4sz,2022-07-04 17:25:06,10.0,failed,server_error,Subscription charge underwent an expected failure.,payment_initiation,order_JpHPTkzbeXcWZi
pay_JpHh9qY2zOIa4g,2022-07-04 17:41:49,5.0,failed,payment_cancelled,Payment processing cancelled by user,payment_authentication,
pay_JpFJDHFYE5L2xo,2022-07-04 15:21:45,100.0,failed,payment_failed,Your payment didn't go through due to a temporary issue. Any debited amount will be refunded in 4-5 business days.,payment_authorization,order_JpFIZNUOnKaXta
```

