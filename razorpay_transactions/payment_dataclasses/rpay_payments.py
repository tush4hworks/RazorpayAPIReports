import datetime
from dataclasses import dataclass, field, fields,make_dataclass
from typing import Iterable, Dict, Any
from razorpay_transactions.utils.log import ModuleLogger
from razorpay_transactions.errors.exceptions import PaymentReportBaseException
from enum import Enum

logger = ModuleLogger.get_logger(__name__)


class PaymentStatus(Enum):
    created = "created"
    authorized = "authorized"
    captured = "captured"
    refunded = "refunded"
    failed = "failed"


class PaymentMethod(Enum):
    card = "card"
    netbanking = "netbanking"
    wallet = "wallet"
    emi = "emi"
    upi = "upi"


class RefundStatus(Enum):
    null = "null"
    partial = "partial"
    full = "full"


class CardNetwork(Enum):
    AmericanExpress = "American Express"
    DinersClub = "Diners Club"
    Maestro = "Maestro"
    MasterCard = "MasterCard"
    RuPay = "RuPay"
    Unknown = "Unknown"
    Visa = "Visa"


class CardType(Enum):
    credit = "credit"
    debit = "debit"
    prepaid = "prepaid"
    unknown = "unkown"


@dataclass
class Payment:
    id: str
    entity: str
    amount: float
    currency: str
    status: PaymentStatus
    method: PaymentMethod
    order_id: str
    description: str
    international: bool
    refund_status: RefundStatus
    amount_refunded: int
    captured: bool
    email: str
    contact: int
    fee: int
    tax: int
    error_code: str
    error_description: str
    error_source: str
    error_step: str
    error_reason: str
    created_at: Any
    last4: int = None
    network: CardNetwork = CardNetwork.Unknown
    type = CardType = CardType.unknown
    issuer: str = None
    sub_type: str = None
    notes: Dict = field(default_factory=dict)
    base_amount: int = None
    base_currency: str = None
    vpa: str = None
    card_id: str = None
    acquirer_data: Dict = field(default_factory=dict)
    bank: str = None
    wallet: str = None
    invoice_id: str = None
    emi: bool = None
    name: str = None
    customer_id: str = None
    token_id: str = None
    created_at_epoch: int = field(init=False)

    def __post_init__(self):
        self.created_at_epoch = self.created_at
        self.created_at = datetime.datetime.fromtimestamp(int(self.created_at)).strftime('%Y-%m-%d %H:%M:%S')
        self.amount = round(float(self.amount / 100), 2)

    def __eq__(self, other):
        return self.id == other.id


class PaymentSummaryDAO:
    PaymentSummary = None

    @classmethod
    def initialize_payment_summary_data_class(cls, fields: Iterable):
        try:
            cls.PaymentSummary = make_dataclass("PaymentSummary", fields=fields, init=False)
            logger.info("Dataclass Generated")
        except Exception as e:
            logger.error(e.__str__())
            raise PaymentReportBaseException(e)

    @classmethod
    def map_attributes(cls, payment: Payment):
        payment_summary = cls.PaymentSummary()
        for f in set([f.name for f in fields(cls.PaymentSummary)]):
            setattr(payment_summary, f, getattr(payment, f))
        return payment_summary
