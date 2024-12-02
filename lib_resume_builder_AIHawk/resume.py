from typing import List, Optional, Union, Literal
import yaml
from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing_extensions import Annotated


class ResumeSectionBase(BaseModel):
    variant: str
    title: Optional[str] = None
    icon: Optional[str] = Field(None, pattern=r"^fa")


class ResumeSectionEntryBase(BaseModel):
    title: Optional[str] = None
    link: Optional[AnyUrl] = None


class ResumeSummarySection(ResumeSectionBase):
    variant: Literal["summary"]
    content: str


class ResumeContactCustomSectionEntry(ResumeSectionEntryBase):
    title: str
    icon: str = Field(..., pattern=r"^fa")


class ResumeContactSection(ResumeSectionBase):
    variant: Literal["contact"]
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    linkedin: Optional[AnyUrl] = None
    github: Optional[AnyUrl] = None
    website: Optional[AnyUrl] = None
    custom_entries: Optional[List[ResumeContactCustomSectionEntry]] = Field(
        None, min_items=1
    )


class ResumeChronologicalSectionEntry(ResumeSectionEntryBase):
    title: str
    dates: List[str] = Field(..., min_items=1, max_item=2)
    location_name: Optional[str]
    location_address: Optional[str]
    content: Optional[str] = None
    details: Optional[List[str]] = Field(None, min_items=1)


class ResumeChronologicalSection(ResumeSectionBase):
    variant: Literal["chronological"]
    title: str
    entries: List[ResumeChronologicalSectionEntry] = Field(..., min_items=1)


class ResumeListSectionEntry(ResumeSectionEntryBase):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    details: Optional[List[str]] = Field(None, min_items=1)


class ResumeListSectionContentEntry(ResumeSectionEntryBase):
    title: str
    description: Optional[str] = None
    details: Optional[None] = None
    content: Optional[str] = None


class ResumeListSection(ResumeSectionBase):
    variant: Literal["list"]
    orientation: Literal["horizontal", "vertical"]
    title: str
    entries: List[ResumeListSectionEntry] = Field(..., min_items=1)


ResumeSection = Annotated[
    Union[
        ResumeContactSection,
        ResumeSummarySection,
        ResumeChronologicalSection,
        ResumeListSection,
    ],
    Field(discriminator="variant"),
]


class Resume(BaseModel):
    name: str
    job_title: Optional[str]
    sections: List[ResumeSection] = Field(..., min_items=1)

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
