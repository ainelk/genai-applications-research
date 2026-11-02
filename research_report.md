# Research on Generative AI Applications

**Course:** EPAM Tech Orda — Generative AI for Software Development, Course Introduction  
**Research date:** 2 November 2026  
**Scope:** Eight business use cases, with two existing implementations per case.

## Approach and boundaries

Generative AI creates or transforms content, such as text, code, images, and structured records. This report examines where that capability can fit into real work. Each use case contains two analysis paragraphs followed by product examples. Product descriptions are based on the linked primary sources, consulted on the research date; availability depends on each provider's current plans and settings. Proposed architectures, benefits, weaknesses, and success measures are engineering analysis, not claims that every listed product uses that architecture. No product benchmark or paid account trial was performed.

A large language model (LLM) predicts and generates language from supplied input. Its fluent response is not proof that its statements are true. Retrieval-augmented generation (RAG) combines retrieval with generation, as described by [Lewis et al.](https://arxiv.org/abs/2005.11401). This pattern can provide relevant evidence, but does not guarantee correctness. Security recommendations in this report are informed by [OWASP's prompt injection guidance](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), including least privilege, output validation, and approval for privileged actions.

<!-- ANALYSIS_START -->
## 1. Customer support and service assistance

**Business value and workflow.** An LLM can draft replies, summarize cases, and help customers find answers outside business hours. A useful design is to look up approved articles before composing an answer. This reduces repeated work and can improve consistency, while difficult cases remain with the support team. Measure successful resolutions, repeat contacts, customer satisfaction, and cost per resolved case rather than counting generated replies.

**Technical challenges and weak points.** RAG needs current policies, relevant search results, and customer-specific access controls. Latency matters because customers expect an interactive conversation. An invented refund policy can turn a helpful reply into a costly mistake. Instructions hidden in a support ticket can try to redirect the assistant. Tool calling should use narrow permissions, and a staff member approves refunds before the system executes them. These controls reduce the impact of errors; they do not eliminate them.

**Existing implementations**

- [Fin AI Agent](https://fin.ai/help/en/articles/13975995-fin-ai-agent-explained) answers support questions using configured knowledge, connects to business systems, and supports handoff to human teams.
- [Microsoft Copilot in Dynamics 365 Customer Service](https://learn.microsoft.com/en-us/dynamics365/customer-service/administer/csw-faqs-ai-suggestions) assists representatives with answers, draft emails, chat responses, and case summaries.

## 2. Software development and testing

**Business value and workflow.** Coding assistants generate code, explain unfamiliar modules, propose tests, and help developers investigate errors. A developer supplies a prompt describing the expected behavior and reviews the resulting change. The benefit is less time spent on routine implementation and navigation; the business still needs maintainable, secure software. Measure accepted changes, review time, escaped defects, and total delivery time, including rework.

**Technical challenges and weak points.** A context window limits how much repository information a model can consider at once. Code and instructions consume tokens, so irrelevant files can crowd out useful evidence and increase cost. An assistant may invent a library method or produce a test that repeats the same bug as the implementation. Evaluation should include behavior checks and security review. A developer inspects the diff and authorizes merging. Restrict shell access and isolate execution, since generated commands can damage a working environment.

**Existing implementations**

- [GitHub Copilot](https://docs.github.com/en/copilot/get-started/about-github-copilot) supports AI-assisted coding through features such as suggestions, chat, and development agents.
- [Cursor Agent](https://prod.cursor.com/help/ai-features/agent) searches a codebase, edits files, runs commands, and helps verify software changes.

## 3. Internal knowledge search and research assistance

**Business value and workflow.** Employees can ask questions across internal documents instead of searching many applications. A common RAG design uses an embedding to represent meaning and a vector database to retrieve related passages. Grounding connects the answer to that evidence. A new employee, for example, could ask which onboarding policy applies to their team and open the supporting document. Measure answer correctness, search time saved, and citation usefulness.

**Technical challenges and weak points.** Search quality depends on document freshness, chunk boundaries, terminology, and permissions. A system may turn a question into a numeric representation and search a store of vectors for similar passages. That can still retrieve an obsolete policy. Each factual claim should be supported by a retrieved passage. Data provenance helps trace information to its source, version, and owner. A citation can exist without supporting the claim, and malicious instructions inside a retrieved document can redirect generation. Permission checks belong in retrieval and application code, not only in model instructions.

**Existing implementations**

- [Glean Assistant](https://docs.glean.com/user-guide/about/what-is-glean) provides answers and drafts from connected company applications, with citations and permission-aware access.
- [Gemini Notebook](https://support.google.com/gemininotebook/answer/16179559) lets users ask questions about selected source material and inspect supporting citations.

## 4. Business writing and language adaptation

**Business value and workflow.** A writing assistant can draft emails, rewrite a document for a different audience, and propose clearer wording. Prompt design should specify the intended reader, facts to preserve, tone, and output format. This can shorten drafting cycles and help teams communicate consistently. Measure editing time and reviewer acceptance, and compare quality across supported languages instead of assuming the same performance everywhere.

**Technical challenges and weak points.** A polished rewrite can subtly change a promise, omit an exception, or introduce a fabricated claim. During inference, the model produces an output from the provided input; it does not verify every fact automatically. Fine-tuning changes model weights using examples and may help with a specialized style, but it is not a substitute for retrieving current facts. An editor checks that names, numbers, and commitments match the source. Sending confidential drafts to an external service also requires an appropriate data-handling setup.

**Existing implementations**

- [Microsoft Copilot in Word](https://support.microsoft.com/en-us/word/copilot/draft-and-add-content-with-copilot-in-word) drafts, expands, rewrites, and transforms document content from instructions and available reference material.
- [DeepL Write](https://support.deepl.com/hc/en-us/articles/6318834492700-About-DeepL-Write) improves grammar and phrasing and suggests alternative wording in its supported languages.

## 5. Marketing visuals and creative production

**Business value and workflow.** Generative tools create draft images, concept variations, backgrounds, and short video assets from a brief. A multimodal model can work with more than one type of information, such as text and images. Teams can explore visual directions before investing in final production. Measure time to an approved asset, revision effort, and brand consistency; producing more variations does not itself demonstrate a better campaign.

**Technical challenges and weak points.** Generated visuals may contain distorted details, inconsistent products, or inaccurate text. A model can combine a written brief with a reference image to suggest a composition. The output can still violate brand requirements or misrepresent a product. Guardrails can block some prohibited requests, but a designer must inspect the final asset. Keep a record of source assets, permissions, generation settings, and edits. Commercial suitability must be checked for the specific model, input assets, and planned use.

**Existing implementations**

- [Adobe Firefly](https://helpx.adobe.com/firefly/web/get-started/learn-the-basics/adobe-firefly-overview.html) generates and edits creative content, including images and videos, from prompts and supported reference inputs.
- [Canva AI](https://www.canva.com/canva-ai/) creates and refines designs and elements through conversational instructions within Canva's creative workflow.

## 6. Tutoring and language practice

**Business value and workflow.** A tutor can provide hints, ask follow-up questions, and adapt explanations to the learner's responses. A language partner can simulate everyday conversations without requiring a human partner at every session. Human-in-the-loop review is useful for curriculum and sensitive learning situations. Measure learning gains and transfer to independent tasks, alongside engagement and completion rates.

**Technical challenges and weak points.** An assistant can give a convincing but incorrect explanation or reveal an answer before the learner has tried. Adaptive dialogue also needs limits on age-inappropriate material and unnecessary collection of student information. A teacher reviews misleading explanations and adjusts the learning activity. Test with representative questions and expert-reviewed expected answers. Personalization must not be confused with proven educational benefit, and model-generated grading needs separate validation before it affects a learner's outcome.

**Existing implementations**

- [Khanmigo](https://www.khanmigo.ai/) acts as an AI tutor and teaching assistant, guiding learners through questions rather than simply providing answers.
- [Duolingo Max](https://blog.duolingo.com/duolingo-max/) offers AI-powered conversation practice through features including Roleplay and Video Call.

## 7. Meeting summaries and follow-up drafting

**Business value and workflow.** Meeting assistants turn conversations into concise notes, decisions, and proposed action items. This reduces note-taking effort and helps people catch up on missed discussions. The useful output is an accurate shared record, not just a shorter transcript. Measure summary factuality, action-owner accuracy, review time, and the number of corrections participants request.

**Technical challenges and weak points.** Speech recognition and speaker attribution errors can propagate into the summary. Hallucination can create an agreement that nobody made. Long meetings may exceed the available input budget, so summaries of smaller sections can lose cross-meeting context. Participants should confirm decisions and task owners before follow-ups are sent. Recording permissions, access, retention, and automatic sharing settings also need attention. Link important decisions back to the relevant transcript segment so reviewers can verify them.

**Existing implementations**

- [Microsoft Copilot in Teams](https://support.microsoft.com/en-us/teams/copilot/catch-up-on-meetings-with-microsoft-365-copilot-in-teams) summarizes discussions, suggests action items, and answers questions using available meeting information.
- [Otter](https://help.otter.ai/hc/en-us/articles/9156381229079-Meeting-Summary-Overview) generates meeting summaries and presents topics, highlights, and action items alongside the transcript.

## 8. Document extraction and workflow preparation

**Business value and workflow.** Generative document processing converts invoices, forms, and free-text communications into records that software can use. Structured output makes fields predictable for downstream systems. A schema might require a supplier name, invoice number, currency, and line items, with missing values represented explicitly. The value is reduced manual entry and quicker processing; measure field accuracy, exception rates, review effort, and cost per correctly processed document.

**Technical challenges and weak points.** A valid JSON object can still contain the wrong amount or attach a value to the wrong document. Scans, handwriting, unusual layouts, and ambiguous fields require careful testing. Return a record with predefined fields and types, then validate totals and required values using deterministic code. Preserve a link from each extracted value to its source page. Low-confidence or inconsistent cases go to a person for review before the system updates business records. Treat embedded document instructions as untrusted content and constrain integrations to approved operations.

**Existing implementations**

- [Amazon Bedrock Data Automation](https://docs.aws.amazon.com/us_en/bedrock/latest/userguide/bda.html) uses generative AI to transform documents and other unstructured media into structured information for applications and workflows.
- [UiPath IXP](https://www.uipath.com/product/ixp) combines document processing capabilities with generative extraction for complex unstructured content and connects results to automation workflows.

## Cross-cutting implementation choices

Start with a narrow task, a trusted data source, and a measurable baseline. Prompt injection is a risk when external content is interpreted as instructions. Guardrails, application-level authorization, and output validation are complementary defenses. Test accuracy, permissions, and failure handling before expanding autonomy. Compare outputs against a representative reference set and track regressions after changes. An AI-based evaluator can help scale reviews, but it also needs calibration against human judgments.

Keep inference cost and latency visible in the operating budget. The system must account for time spent searching, generating, validating, and waiting for connected services. Fine-tuning is worth considering when a stable task needs consistent behavior and suitable examples exist; it should be compared against simpler prompting and retrieval approaches. Updating learned weights using curated examples is a training activity, while generating a response with the trained model is a runtime activity. Tool calling lets a model request an external function; backend code should validate arguments, permissions, and results before allowing side effects.
<!-- ANALYSIS_END -->

## Research limitations and next steps

This is a desk-research report, not a product ranking or proof of return on investment. The product examples demonstrate existing implementations; they were not tested against a shared dataset. Business benefits are hypotheses to validate in a pilot. Before adopting a tool, verify its current availability, access controls, retention behavior, integration limits, and total cost for the intended environment.

The separate [vocabulary](vocabulary.md) explains 20 terms used in this analysis. The optional [relationship graph](vocabulary_graph.html) links those terms to use cases and displays explicit and implicit usage separately. Its counting method and auditable evidence are included in the project.

**AI assistance disclosure:** This report and the initial vocabulary explanations were prepared with AI assistance. The vocabulary is a study draft for the learner to review and personalize, not a claim that the learner manually wrote the definitions or has already mastered every term.
