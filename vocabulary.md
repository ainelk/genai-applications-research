# Generative AI Vocabulary

| Term | Plain-language explanation | Example in the report |
| --- | --- | --- |
| **Large language model (LLM)** | A model trained on large amounts of language-related data to predict and generate text. It can write a fluent answer without knowing whether the answer is correct. | A support assistant drafts a reply to a customer's question. |
| **Prompt** | The input that tells a model what task to do and provides relevant instructions or examples. Better instructions can help, but they cannot guarantee a correct result. | A developer describes the behavior that a code change should implement. |
| **Token** | A unit a model uses to process text, often a word piece or punctuation mark. Tokens affect input capacity and often usage cost. | Repository files and instructions consume the coding assistant's input budget. |
| **Context window** | The maximum amount of information a model can process in a single request, measured in tokens. It is a capacity limit, not a guarantee that every detail will be used well. | A long repository or meeting may not fit in one request. |
| **Retrieval-augmented generation (RAG)** | Finding relevant information first and giving it to a model so it can build an answer using that material. Search can still return the wrong evidence. | A support bot consults approved policy articles before replying. |
| **Embedding** | A numeric representation used to compare meaning or other learned similarities. Similar wording or concepts may have nearby representations, depending on the model. | A question and document passages are represented as vectors for search. |
| **Vector database** | A data store that can index and search vectors to find similar items, often alongside metadata filters. It stores representations; it does not itself generate the answer. | A knowledge assistant retrieves passages related to an employee's question. |
| **Grounding** | Connecting generated claims to relevant evidence or external data. A grounded answer should be checked against its evidence. | An onboarding answer points to the policy passage that supports it. |
| **Hallucination** | Output that sounds plausible but is invented or unsupported by the available evidence. Fluency and confidence do not make it reliable. | A meeting summary invents a decision that participants never made. |
| **Prompt injection** | Content that tries to make an AI application treat untrusted material as instructions and behave in an unintended way. It can arrive through a user's message or retrieved documents. | Instructions hidden in a ticket attempt to redirect a support assistant. |
| **Fine-tuning** | Additional training that changes a model's weights using selected examples. It can adapt behavior, but is not a reliable store of constantly changing facts. | A stable writing task may use examples to adapt a model's style. |
| **Inference** | Running a trained model on an input to produce an output. This is different from training or changing its weights. | A writing model generates a new draft from supplied instructions. |
| **Latency** | The time a user waits for a system's response or a defined part of that response. Search, generation, validation, and integrations all add delay. | A support conversation becomes frustrating if each reply takes too long. |
| **Multimodal model** | A model that works with more than one type of information, such as text and images. Supported input and output types depend on the model. | A creative tool uses both a written brief and a reference image. |
| **Structured output** | Model output arranged to follow a defined format, such as a JSON schema. Correct formatting does not mean the values are factually correct. | An invoice extractor returns named fields with specified types. |
| **Tool calling** | A model requesting that an application run a particular external function with specified arguments. The application must decide whether and how to execute it. | A support assistant requests a permitted operation in a business system. |
| **Guardrails** | Controls intended to limit unwanted behavior, such as content checks, output rules, and restrictions on available actions. They need testing and do not remove all risk. | A creative tool blocks some prohibited requests before producing content. |
| **Human-in-the-loop** | A workflow where a person reviews, corrects, or approves an AI-related step. The person needs enough information and time to make the review meaningful. | A staff member approves a refund before execution. |
| **Evaluation** | Checking an AI system against representative tasks and agreed measures of success. It should include realistic failures and repeat after important changes. | Review code behavior, summary accuracy, and permission failures before release. |
| **Data provenance** | A record of where information came from and how it changed. It helps reviewers trace an answer or extracted field back to the original material. | An extracted value remains linked to its source page and document version. |

## Distinctions to remember

- **RAG vs. fine-tuning:** RAG supplies retrieved information during a request; fine-tuning changes model weights through training.
- **Grounding vs. provenance:** Grounding concerns the evidence supporting a claim; provenance records the origin and history of the underlying information.
- **Structured output vs. correctness:** A response can follow a schema perfectly and still contain a wrong value.
- **Tool calling vs. authorization:** Requesting a function does not grant the model permission to execute it.

