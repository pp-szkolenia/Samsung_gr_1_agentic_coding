import warnings
warnings.filterwarnings("ignore", message="LangchainEmbeddingsWrapper is deprecated")

from openai import OpenAI
from dotenv import load_dotenv
from ragas.metrics._context_precision import context_precision
from ragas.metrics._context_recall import context_recall
from ragas.metrics._faithfulness import faithfulness
from ragas.metrics._answer_relevance import answer_relevancy
from ragas.llms import llm_factory
from ragas.embeddings.base import LangchainEmbeddingsWrapper
from langchain_openai import OpenAIEmbeddings
from ragas import SingleTurnSample, EvaluationDataset, evaluate

load_dotenv()

client = OpenAI()
eval_llm = llm_factory("gpt-4o-mini", client=client)
eval_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-small"))

user_input = "Jaka jest stolica Hiszpanii?"
response = "Wieża Eiffla znajduje się w Paryżu"
contexts = [
    "Wieża Eiffla to słynny zabytek znajdujący się w Paryżu, we Francji.",
    "Madryt jest stolicą Hiszpanii",
    "Berlin jest stolicą Niemiec"
]
reference = "Stolicą Hiszpanii jest Madryt"

sample = SingleTurnSample(
    user_input=user_input,
    retrieved_contexts=contexts,
    response=response,
    reference=reference
)

dataset = EvaluationDataset(samples=[sample])

metrics = [
    context_precision,
    context_recall,
    faithfulness,
    answer_relevancy
]

results = evaluate(
    dataset=dataset,
    metrics=metrics,
    llm=eval_llm,
    embeddings=eval_embeddings
)

print(results)
