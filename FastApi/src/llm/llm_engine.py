
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.postprocessor import SimilarityPostprocessor
from llama_index import StorageContext, load_index_from_storage, ServiceContext

from llama_index.llms import ChatMessage, MessageRole
from llama_index.prompts import ChatPromptTemplate
import torch
from transformers import BitsAndBytesConfig
from llama_index.prompts import PromptTemplate
from llama_index.llms import HuggingFaceLLM

DATA_PATH = "./data/film_summaries_index_dump"

def messages_to_prompt(messages):
  prompt = ""
  for message in messages:
    if message.role == 'system':
      prompt += f"<|system|>\n{message.content}</s>\n"
    elif message.role == 'user':
      prompt += f"<|user|>\n{message.content}</s>\n"
    elif message.role == 'assistant':
      prompt += f"<|assistant|>\n{message.content}</s>\n"

  # ensure we start with a system prompt, insert blank if needed
  if not prompt.startswith("<|system|>\n"):
    prompt = "<|system|>\n</s>\n" + prompt

  # add final assistant prompt
  prompt = prompt + "<|assistant|>\n"

  return prompt

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)


def get_llm_engine():

    llm = HuggingFaceLLM(
        model_name="HuggingFaceH4/zephyr-7b-alpha",
        tokenizer_name="HuggingFaceH4/zephyr-7b-alpha",
        query_wrapper_prompt=PromptTemplate("<|system|>\n</s>\n<|user|>\n{query_str}</s>\n<|assistant|>\n"),
        context_window=3900,
        max_new_tokens=512,
        model_kwargs={"quantization_config": quantization_config},
        # tokenizer_kwargs={},
        generate_kwargs={"temperature": 0.7, "top_k": 50, "top_p": 0.95},
        messages_to_prompt=messages_to_prompt,
        device_map="auto",
    )

    """Setting up our retrieval system"""


    # Text QA Prompt
    chat_text_qa_msgs = [
        ChatMessage(
            role=MessageRole.SYSTEM,
            content=(
                "You are a Film Recomendation Assistant. You are very knowledgeable about movies, "
                "know a huge number of films, and are eager to make great movie recommendations. "
                "You are very helpful, responsive and are always attentive to the interests of your interlocutor."
            ),
        ),
        ChatMessage(
            role=MessageRole.USER,
            content=(
                "You will be asked a question, here is some context information that may be useful to answer the question:\n"
                "---------------------\n"
                "{context_str}\n"
                "---------------------\n"
                "Given the context information about relevant films (that may appear relevant for current question) "
                "or by using your expertise"
                "answer the question: {query_str}\n"
            ),
        ),
    ]
    text_qa_template = ChatPromptTemplate(chat_text_qa_msgs)

    # build index
    service_context = ServiceContext.from_defaults(llm=llm, embed_model="local:BAAI/bge-large-en-v1.5")

    storage_context = StorageContext.from_defaults(persist_dir=DATA_PATH)

    # load index
    index = load_index_from_storage(storage_context, service_context=service_context,
                                    show_progress = True)


    # assemble query engine
    query_engine = index.as_query_engine(
        response_mode="compact",
        text_qa_template=text_qa_template,
        similarity_top_k=3
        )

    return query_engine