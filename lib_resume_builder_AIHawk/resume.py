from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union, Literal
import yaml
from pydantic import BaseModel, EmailStr, HttpUrl, Field


class SectionBase(BaseModel):
    section_icon: Optional[str]
    section_title: Optional[str]


class SectionEntryBase(BaseModel):
    title: Optional[str]
    description: Optional[str] = None
    icon: Optional[str] = None
    link: Optional[str] = None
    details: Optional[List[str]] = None


class ContactSection(SectionBase):
    section_type: Literal["contact"]
    section_entries: Optional[List[SectionEntryBase]] = None


class SummarySection(SectionBase):
    section_type: Literal["summary"]
    section_content: Optional[str]


class ChronologicalSectionEntry(SectionEntryBase):
    location_name: Optional[str]
    location_address: Optional[str]


class ChronologicalSection(SectionBase):
    section_type: Literal["chronological"]
    section_entries: Optional[List[ChronologicalSectionEntry]] = None


class ListSection(SectionBase):
    section_type: Literal["list"]
    section_entries: Optional[List[SectionEntryBase]] = None
    section_orientation: Literal["horizontal", "vertical"]


Section = Union[ContactSection, SummarySection, ChronologicalSection, ListSection]


class PersonalInformation(BaseModel):
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


class Availability(BaseModel):
    notice_period: Optional[str]


class SalaryExpectations(BaseModel):
    salary_range_usd: Optional[str]


class SelfIdentification(BaseModel):
    gender: Optional[str]
    pronouns: Optional[str]
    veteran: Optional[str]
    disability: Optional[str]
    ethnicity: Optional[str]


class LegalAuthorization(BaseModel):
    eu_work_authorization: Optional[str]
    us_work_authorization: Optional[str]
    requires_us_visa: Optional[str]
    requires_us_sponsorship: Optional[str]
    requires_eu_visa: Optional[str]
    legally_allowed_to_work_in_eu: Optional[str]
    legally_allowed_to_work_in_us: Optional[str]
    requires_eu_sponsorship: Optional[str]


class Resume(BaseModel):
    personal_information: Optional[PersonalInformation]
    sections: Optional[List[Section]] = None

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
