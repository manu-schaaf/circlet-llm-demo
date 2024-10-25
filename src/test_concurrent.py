import argparse
import base64
import json
import sys
import traceback
from itertools import batched, product
from pathlib import Path
from random import shuffle

from pqdm.processes import pqdm as pqdm_t
from requests import post
from tqdm import tqdm

from circlet.lib.chat import Message, SystemMessage, TemplateUserMessage
from circlet.lib.response import Err, Response


def run_test_query(messages: list[Message], model: str = "nemotron:latest"):
    try:
        response = post(
            "http://gondor.hucompute.org:11434/v1/chat/completions",
            json={
                "model": model,
                "messages": messages,
            },
        )

        return Response.process(response)
    except Exception as e:
        return Err({"exception": e})


def load_model(model_name: str):
    try:
        response = post(
            "http://gondor.hucompute.org:11434/api/generate",
            json={
                "model": model_name,
                # "keep_alive": 3600 * 10,  # keep the model in memory for 10 hours
            },
            timeout=600,  # wait for 5min max.
        )
    except Exception:
        print(f"Caught exception during model load!", file=sys.stderr)
        traceback.print_exc()

    print(repr(Response.process(response)))


def run_test(
    story_types: list[str],
    story_topics: list[str],
    story_lengths: list[str],
    system_prompt: SystemMessage,
    template: TemplateUserMessage,
    model_names: list[str],
    n_concurrent: tuple[int] = (1, 2, 4, 8),
):
    parameters = list(product(story_types, story_topics, story_lengths))
    shuffle(parameters)

    for batch, n_jobs in zip(
        tqdm(
            batched(parameters, len(parameters) // len(n_concurrent)),
            desc="Batch",
            position=0,
        ),
        n_concurrent,
    ):
        prompts: list[list[Message]] = [
            {
                "messages": [
                    system_prompt,
                    template.format(length=length, topic=topic, n_words=n_words),
                ],
                "model": model,
            }
            for model in model_names
            for length, topic, n_words in batch
        ]
        results = pqdm_t(
            prompts,
            run_test_query,
            n_jobs=n_jobs,
            desc=f"Queries: n_jobs={n_jobs}",
            argument_type="kwargs",
            position=1,
        )
        output_directory = Path(f"test/output/{n_jobs}/")
        output_directory.mkdir(parents=True, exist_ok=True)
        for (l, t, n, m), response in zip(parameters, results):
            try:
                t = base64.b64encode(t.encode()).decode("utf-8")
                m = m.replace(":", "-").replace(" ", "-").replace("/", "-")
                with (output_directory / f"l={l}-n={n}-m={m}-t={t}.json").open(
                    "w"
                ) as f:
                    json.dump(response.data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(
                    f"Caught exception during write: {e}\n{json.dumps(response.data, indent=2)}"
                )


PARAM_TYPE = ["short", "exciting", "funny", "boring"]
PARAM_TOPIC = [
    "a talking lizard with a lisp",
    "a very small wizard with a large hat",
    "a sentient rubber tire escaping a landfill",
    "a guy with a kangoroo as a flat mate",
]
PARAM_WORDS = list(range(300, 309))
SYSTEM_PROMPT = SystemMessage("You are an AI assistant writing stories.")
TEMPLATE = TemplateUserMessage(
    "Write a {length} story about {topic} with at least {n_words} words."
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["load", "run", "big"])
    parser.add_argument(
        "-m",
        "--models",
        nargs="+",
        default=[
            "llama3.1:8b-circlet",
            "llama3.1:70b-circlet",
            "reflection:circlet",
        ],
        type=str,
    )
    parser.add_argument("-j", "--n_jobs", nargs="+", default=(8, 16, 32), type=int)
    args = parser.parse_args()

    match args.command:
        case "load":
            load_model(args.model)
        case "run":
            run_test(
                story_types=PARAM_TYPE,
                story_topics=PARAM_TOPIC,
                story_lengths=PARAM_WORDS,
                system_prompt=SYSTEM_PROMPT,
                template=TEMPLATE,
                model_names=args.models,
                n_concurrent=args.n_jobs,
            )
