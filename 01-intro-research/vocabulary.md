# GenAI Vocabulary

Terms I picked from my report and the course intro, explained in my own words. Will keep adding to it during the course.

**LLM (Large Language Model)** - neural network trained on huge amount of text to predict the next token. Base for most AI tools today.

**Token** - piece of text the model works with (part of a word, word, or symbol). Pricing, limits and speed are all counted in tokens.

**Tokenomics** - economics of token usage: how much input/output tokens cost, and how to design a solution so it doesn't burn money.

**Context window** - max amount of tokens model can "see" at once (prompt + history + docs + answer). Everything outside is forgotten.

**Prompt** - input text/instructions we give the model to steer what it generates.

**System prompt** - hidden instructions set by the developer that define model behavior, role and rules for the whole conversation.

**Prompt engineering** - practice of writing and structuring prompts (examples, format, constraints) to get stable and useful results.

**Hallucination** - when model generates something that sounds confident and correct but is made up (fake API, fake fact, fake link).

**Grounding** - tying model answers to real sources (docs, DB, search results) so it doesn't make things up.

**RAG (Retrieval-Augmented Generation)** - pattern where we first search relevant documents and put them into the prompt, then the model answers based on them.

**Embedding** - vector (list of numbers) that represents meaning of a text. Similar texts have close vectors.

**Vector database** - DB that stores embeddings and quickly finds the most similar ones. Used in RAG (e.g. pgvector, Pinecone, Qdrant).

**Chunking** - splitting documents into smaller pieces before embedding them, so retrieval returns relevant parts, not whole files.

**Fine-tuning** - additional training of an existing model on our own data to adapt it to a specific task or style.

**Inference** - running the trained model to get an answer (as opposed to training it).

**Temperature** - parameter that controls randomness of output. Low = more deterministic, high = more creative/random.

**Multimodal** - model or system that works with more than text: images, audio, video.

**Agent** - LLM-based system that can plan steps, call tools (search, code, APIs) and act in a loop to complete a task, not just answer once.

**Agentic workflow** - process where one or several agents plan and execute multi-step tasks, often with handoffs between them.

**Tool calling (function calling)** - model returns structured request to call some function/API, the app executes it and gives result back to the model.

**MCP (Model Context Protocol)** - open protocol for connecting AI apps to external tools and data sources in a standard way.

**Copilot** - AI assistant added into existing software (IDE, Office) as a helper, human stays in control.

**AI-native tool** - tool designed around AI from the start (e.g. Cursor), not just an AI plugin bolted on.

**Vibe coding** - building software by describing what you want in natural language and letting AI write most of the code.

**Guardrails** - checks and limits around a model (input/output filters, rules, validation) to keep it safe and on-task.

**Prompt injection** - attack where malicious text in user input or in data the model reads overrides its instructions.

**Human-in-the-loop** - human reviews or approves AI output before important actions are taken.

**PoC (Proof of Concept)** - small experiment to check if an idea is technically possible, before building a real product.

**SME (Subject Matter Expert)** - person with deep knowledge in a specific domain.

**Deepfake** - AI-generated fake image, video or voice of a real person.
