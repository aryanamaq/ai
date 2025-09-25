from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class DocumentType(str, Enum):
    LEASE = "lease"
    LOAN = "loan"
    MSA = "msa"

class ValidationStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"

class CoreFields(BaseModel):
    document_id: str
    type: DocumentType
    effective_date: Optional[datetime]
    execution_date: Optional[datetime]
    governing_law: Optional[str]
    jurisdiction: Optional[str]
    parties: List[Dict[str, str]]
    monetary_terms: Dict[str, float]
    key_dates: Dict[str, datetime]
    clauses: List[Dict[str, Any]]
    signatures_present: bool
    tables_extracted: List[Dict[str, Any]]
    validation: Dict[str, ValidationStatus]

class LeaseFields(BaseModel):
    rent_amount: float
    deposit_amount: float
    lease_term: str
    renewal_terms: Optional[str]
    property_details: Dict[str, str]

class LoanFields(BaseModel):
    interest_rate: float
    principal_amount: float
    repayment_schedule: Dict[str, Any]
    covenants: List[str]
    collateral: Optional[Dict[str, Any]]

class MSAFields(BaseModel):
    service_scope: List[str]
    payment_terms: Dict[str, Any]
    sla_terms: Dict[str, Any]
    termination_clause: Dict[str, str]

class DocumentExtraction(BaseModel):
    core: CoreFields
    domain_specific: Optional[Dict[str, Any]]
    metadata: Dict[str, Any]
    processing_stats: Dict[str, Any]
    validation_results: List[Dict[str, Any]]
    document_hash: str