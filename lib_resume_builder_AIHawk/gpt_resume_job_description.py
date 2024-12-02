import json
import os
import tempfile
import textwrap
import time
from datetime import datetime
from typing import Dict, List
from langchain_community.document_loaders import TextLoader
from langchain_core.messages.ai import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import StringPromptValue
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_text_splitters import TokenTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from lib_resume_builder_AIHawk.config import global_config
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import re  # For regex parsing, especially in `parse_wait_time_from_error_message`
from requests.exceptions import (
    HTTPError as HTTPStatusError,
)  # Handling HTTP status errors
import openai


load_dotenv()

log_folder = "log"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Configura il file di log
log_file = os.path.join(log_folder, "app.log")

# Configura il logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file, encoding="utf-8")],
)

logger = logging.getLogger(__name__)


class LLMLogger:

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    @staticmethod
    def log_request(prompts, parsed_reply: Dict[str, Dict]):
        calls_log = global_config.LOG_OUTPUT_FILE_PATH / "open_ai_calls.json"
        if isinstance(prompts, StringPromptValue):
            prompts = prompts.text
        elif isinstance(prompts, Dict):
            # Convert prompts to a dictionary if they are not in the expected format
            prompts = {
                f"prompt_{i+1}": prompt.content
                for i, prompt in enumerate(prompts.messages)
            }
        else:
            prompts = {
                f"prompt_{i+1}": prompt.content
                for i, prompt in enumerate(prompts.messages)
            }

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extract token usage details from the response
        token_usage = parsed_reply["usage_metadata"]
        output_tokens = token_usage["output_tokens"]
        input_tokens = token_usage["input_tokens"]
        total_tokens = token_usage["total_tokens"]

        # Extract model details from the response
        model_name = parsed_reply["response_metadata"]["model_name"]
        prompt_price_per_token = 0.00000015
        completion_price_per_token = 0.0000006

        # Calculate the total cost of the API call
        total_cost = (input_tokens * prompt_price_per_token) + (
            output_tokens * completion_price_per_token
        )

        # Create a log entry with all relevant information
        log_entry = {
            "model": model_name,
            "time": current_time,
            "prompts": prompts,
            "replies": parsed_reply["content"],  # Response content
            "total_tokens": total_tokens,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_cost": total_cost,
        }

        # Write the log entry to the log file in JSON format
        with open(calls_log, "a", encoding="utf-8") as f:
            json_string = json.dumps(log_entry, ensure_ascii=False, indent=4)
            f.write(json_string + "\n")


class LoggerChatModel:

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def __call__(self, messages: List[Dict[str, str]]) -> str:
        max_retries = 15
        retry_delay = 10

        for attempt in range(max_retries):
            try:

                reply = self.llm(messages)
                parsed_reply = self.parse_llmresult(reply)
                LLMLogger.log_request(prompts=messages, parsed_reply=parsed_reply)
                return reply
            except (openai.RateLimitError, HTTPStatusError) as err:
                if isinstance(err, HTTPStatusError) and err.response.status_code == 429:
                    self.logger.warning(
                        f"HTTP 429 Too Many Requests: Waiting for {retry_delay} seconds before retrying (Attempt {attempt + 1}/{max_retries})..."
                    )
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    wait_time = self.parse_wait_time_from_error_message(str(err))
                    self.logger.warning(
                        f"Rate limit exceeded or API error. Waiting for {wait_time} seconds before retrying (Attempt {attempt + 1}/{max_retries})..."
                    )
                    time.sleep(wait_time)
            except Exception as e:
                self.logger.error(
                    f"Unexpected error occurred: {str(e)}, retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})"
                )
                time.sleep(retry_delay)
                retry_delay *= 2

        self.logger.critical(
            "Failed to get a response from the model after multiple attempts."
        )
        raise Exception(
            "Failed to get a response from the model after multiple attempts."
        )

    def parse_llmresult(self, llmresult: AIMessage) -> Dict[str, Dict]:
        content = llmresult.content
        response_metadata = llmresult.response_metadata
        id_ = llmresult.id
        usage_metadata = llmresult.usage_metadata
        parsed_result = {
            "content": content,
            "response_metadata": {
                "model_name": response_metadata.get("model_name", ""),
                "system_fingerprint": response_metadata.get("system_fingerprint", ""),
                "finish_reason": response_metadata.get("finish_reason", ""),
                "logprobs": response_metadata.get("logprobs", None),
            },
            "id": id_,
            "usage_metadata": {
                "input_tokens": usage_metadata.get("input_tokens", 0),
                "output_tokens": usage_metadata.get("output_tokens", 0),
                "total_tokens": usage_metadata.get("total_tokens", 0),
            },
        }
        return parsed_result

    def parse_wait_time_from_error_message(self, error_message: str) -> int:
        # Extract wait time from error message
        match = re.search(r"Please try again in (\d+)([smhd])", error_message)
        if match:
            value, unit = match.groups()
            value = int(value)
            if unit == "s":
                return value
            elif unit == "m":
                return value * 60
            elif unit == "h":
                return value * 3600
            elif unit == "d":
                return value * 86400
        # Default wait time if not found
        return 30


class LLMResumeJobDescription:
    def __init__(self, openai_api_key, strings):
        self.llm_cheap = LoggerChatModel(
            ChatOpenAI(
                model_name="gpt-4o-mini", openai_api_key=openai_api_key, temperature=0.4
            )
        )
        self.llm_embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.strings = strings

    @staticmethod
    def _preprocess_template_string(template: str) -> str:
        # Preprocess a template string to remove unnecessary indentation.
        return textwrap.dedent(template)

    def set_resume(self, resume):
        self.resume = resume

    def set_job_description_from_url(self, url_job_description):
        from lib_resume_builder_AIHawk.utils import create_driver_selenium

        driver = create_driver_selenium()
        driver.get(url_job_description)
        time.sleep(3)
        body_element = driver.find_element("tag name", "body")
        response = body_element.get_attribute("outerHTML")
        driver.quit()
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".html", mode="w", encoding="utf-8"
        ) as temp_file:
            temp_file.write(response)
            temp_file_path = temp_file.name
        try:
            loader = TextLoader(
                temp_file_path, encoding="utf-8", autodetect_encoding=True
            )
            document = loader.load()
        finally:
            os.remove(temp_file_path)
        text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=50)
        all_splits = text_splitter.split_documents(document)
        vectorstore = FAISS.from_documents(
            documents=all_splits, embedding=self.llm_embeddings
        )
        prompt = PromptTemplate(
            template="""
            You are an expert job description analyst. Your role is to meticulously analyze and interpret job descriptions. 
            After analyzing the job description, answer the following question in a clear, and informative manner.
            
            Question: {question}
            Job Description: {context}
            Answer:
            """,
            input_variables=["question", "context"],
        )

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        context_formatter = vectorstore.as_retriever() | format_docs
        question_passthrough = RunnablePassthrough()
        chain_job_descroption = prompt | self.llm_cheap | StrOutputParser()
        summarize_prompt_template = self._preprocess_template_string(
            self.strings.summarize_prompt_template
        )
        prompt_summarize = ChatPromptTemplate.from_template(summarize_prompt_template)
        chain_summarize = prompt_summarize | self.llm_cheap | StrOutputParser()
        qa_chain = (
            {
                "context": context_formatter,
                "question": question_passthrough,
            }
            | chain_job_descroption
            | (lambda output: {"text": output})
            | chain_summarize
        )
        result = qa_chain.invoke("Provide, full job description")
        self.job_description = result

    def set_job_description_from_text(self, job_description_text):
        prompt = ChatPromptTemplate.from_template(
            self.strings.summarize_prompt_template
        )
        chain = prompt | self.llm_cheap | StrOutputParser()
        output = chain.invoke({"text": job_description_text})
        self.job_description = output

    def generate_header(self) -> str:
        header_prompt_template = self._preprocess_template_string(
            self.strings.prompt_header
        )
        prompt = ChatPromptTemplate.from_template(header_prompt_template)
        chain = prompt | self.llm_cheap | StrOutputParser()
        output = chain.invoke(
            {
                "name": self.resume.name,
                "job_title": self.resume.job_title,
            }
        )
        return output

    def generate_contact_section(self, section) -> str:
        contact_template = self._preprocess_template_string(
            self.strings.prompt_contact_section
        )
        prompt = ChatPromptTemplate.from_template(contact_template)
        chain = prompt | self.llm_cheap | StrOutputParser()
        output = chain.invoke(
            {
                "title": section.title,
                "icon": section.icon,
                "address": section.address,
                "phone": section.phone,
                "email": section.email,
                "linkedin": section.linkedin,
                "github": section.github,
                "website": section.website,
                "custom_entries": section.custom_entries,
            }
        )
        return output

    def generate_summary_section(self, section) -> str:
        summary_template = self._preprocess_template_string(
            self.strings.prompt_summary_section
        )
        prompt = ChatPromptTemplate.from_template(summary_template)
        chain = prompt | self.llm_cheap | StrOutputParser()
        output = chain.invoke(
            {
                "title": section.title,
                "icon": section.icon,
                "entries": section.entries,
                "job_description": self.job_description,
            }
        )
        return output

    def generate_chronological_section(self, section) -> str:
        chronological_template = self._preprocess_template_string(
            self.strings.prompt_chronological_section
        )
        prompt = ChatPromptTemplate.from_template(chronological_template)
        chain = prompt | self.llm_cheap | StrOutputParser()
        output = chain.invoke(
            {
                "title": section.title,
                "icon": section.icon,
                "entries": section.entries,
                "job_description": self.job_description,
            }
        )
        return output

    def generate_list_section(self, section) -> str:
        list_template = self._preprocess_template_string(
            self.strings.prompt_list_section
        )
        prompt = ChatPromptTemplate.from_template(list_template)
        chain = prompt | self.llm_cheap | StrOutputParser()
        output = chain.invoke(
            {
                "icon": section.icon,
                "title": section.title,
                "orientation": section.orientation,
                "entries": section.entries,
                "job_description": self.job_description,
            }
        )
        return output

    def generate_html_resume(self) -> str:
        def header_fn():
            return self.generate_header()

        def get_fn(section):
            match section.variant:
                case "contact":
                    return lambda: self.generate_contact_section(section)
                case "summary":
                    return lambda: self.generate_summary_section(section)
                case "chronological":
                    return lambda: self.generate_chronological_section(section)
                case "list":
                    return lambda: self.generate_list_section(section)
                case _:
                    return lambda: self.logger.critical(
                        f"Invalid section variant {section.variant}"
                    )

        # Create a dictionary to map the function names to their respective callables
        functions = {
            "header": header_fn,
        }

        for index, section in enumerate(self.resume.sections):
            functions[f"section-{index}"] = get_fn(section)

        # Use ThreadPoolExecutor to run the functions in parallel
        with ThreadPoolExecutor() as executor:
            future_to_section = {
                executor.submit(fn): section for section, fn in functions.items()
            }
            results = {}
            for future in as_completed(future_to_section):
                section = future_to_section[future]
                try:
                    result = future.result()
                    if result:
                        results[section] = result
                except Exception as exc:
                    logging.debug(f"{section} generated 1 exc: {exc}")
        full_resume = "<body>\n"
        full_resume += f"  {results.get('header', '')}\n"
        for index, val in enumerate(self.resume.sections):
            full_resume += f"    {results.get(f'section-{index}', '')}\n"
        full_resume += "</body>"
        return full_resume
