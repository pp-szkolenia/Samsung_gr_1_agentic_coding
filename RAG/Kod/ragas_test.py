from openai import OpenAI
from dotenv import load_dotenv
from ragas.metrics import (
    faithfulness,
    context_precision,
    context_recall
)
from ragas.llms import llm_factory
from ragas import SingleTurnSample, EvaluationDataset, evaluate

load_dotenv()

client = OpenAI()
eval_llm = llm_factory("gpt-4o-mini", client=client)

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
    faithfulness
]

results = evaluate(
    dataset=dataset,
    metrics=metrics,
    llm=eval_llm
)

print(results)