# Chapter 1 — Examples

## EX-CH01-001 — Zero-shot sentiment classification

**Purpose:** demonstrate explicit task + constrained output space.  
**Lesson:** clearly define instruction and allowed output format.  
**Source:** zero-shot prompting section.

## EX-CH01-002 — Few-shot palindrome task

**Purpose:** demonstrate adding examples when natural-language task description is insufficient.  
**Lesson:** few-shot prompting changes context, not model weights.  
**Source:** few-shot prompting section.

## EX-CH01-003 — Prompt chaining for extraction + postprocessing

**Purpose:** split a complex task into two prompts.  
**Procedure:** extract first; postprocess missing/outlier values second.  
**Lesson:** decomposition can be more robust than one giant prompt.  
**Source:** Prompt Chaining section.

## EX-CH01-004 — Chat with PDF

**Purpose:** build a minimal retrieval-backed chatbot.  
**Pipeline:** PDF → chunks → embeddings → vector store → query embedding → retrieval → LLM → history.  
**Lesson:** an application is a pipeline of replaceable capabilities, not just an LLM call.  
**Source:** Building Your First Chatbot Prototype.

## EX-CH01-005 — Adversarial prompting

**Purpose:** show that alignment/refusal behavior can be bypassed by crafted prompts.  
**Lesson:** alignment behavior alone is not a sufficient security boundary.  
**Source:** Adversarial Prompting section.
