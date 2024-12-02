from typing import Optional, Literal
import yaml
from pydantic import BaseModel, EmailStr, HttpUrl, Field


class CandidatePersonalInformation(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    job_title: Optional[str]
    date_of_birth: Optional[str]
    country: Optional[str]
    city: Optional[str]
    address: Optional[str]
    zip_code: Optional[str] = Field(None, min_length=5, max_length=10)
    phone_prefix: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    github: Optional[HttpUrl] = None
    linkedin: Optional[HttpUrl] = None


class CandidateAvailability(BaseModel):
    notice_period: Optional[str]


class CandidateSalaryExpectations(BaseModel):
    salary_range_usd: Optional[str]


class CandidateSelfIdentification(BaseModel):
    gender: Optional[str]
    pronouns: Optional[str]
    veteran: Optional[str]
    disability: Optional[str]
    ethnicity: Optional[str]


YesOrNoField = Optional[Literal["Yes", "No"]]


class CandidateLegalAuthorization(BaseModel):
    eu_work_authorization: Optional[YesOrNoField]
    us_work_authorization: Optional[YesOrNoField]
    requires_us_visa: Optional[YesOrNoField]
    requires_us_sponsorship: Optional[YesOrNoField]
    requires_eu_visa: Optional[YesOrNoField]
    legally_allowed_to_work_in_eu: Optional[YesOrNoField]
    legally_allowed_to_work_in_us: Optional[YesOrNoField]
    requires_eu_sponsorship: Optional[YesOrNoField]
    canada_work_authorization: Optional[YesOrNoField]
    requires_canada_visa: Optional[YesOrNoField]
    legally_allowed_to_work_in_canada: Optional[YesOrNoField]
    requires_canada_sponsorship: Optional[YesOrNoField]
    uk_work_authorization: Optional[YesOrNoField]
    requires_uk_visa: Optional[YesOrNoField]
    legally_allowed_to_work_in_uk: Optional[YesOrNoField]
    requires_uk_sponsorship: Optional[YesOrNoField]


class CandidateWorkPreference(BaseModel):
    remote_work: Optional[YesOrNoField]
    in_person_work: Optional[YesOrNoField]
    open_to_relocation: Optional[YesOrNoField]
    willing_to_complete_assessments: Optional[YesOrNoField]
    willing_to_undergo_drug_tests: Optional[YesOrNoField]
    willing_to_undergo_background_checks: Optional[YesOrNoField]


class Candidate(BaseModel):
    personal_information: Optional[CandidatePersonalInformation]
    self_identification: Optional[CandidateSelfIdentification]
    availability: Optional[CandidateAvailability]
    salary_expectations: Optional[CandidateSalaryExpectations]
    legal_authorization: Optional[CandidateLegalAuthorization]
    work_preferences: Optional[CandidateWorkPreference]

    def __init__(self, yaml_str: str):
        try:
            # Parse the YAML string
            data = yaml.safe_load(yaml_str)

            # Create an instance of Resume from the parsed data
            super().__init__(**data)
        except yaml.YAMLError as e:
            raise ValueError("Error parsing YAML file.") from e
        except Exception as e:
            raise Exception(f"Unexpected error while parsing YAML: {e}") from e
