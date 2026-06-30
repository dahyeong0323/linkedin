---
name: korean-blog-style-writer
description: Create or revise Korean blog/LinkedIn-style longform posts that replicate the user's own provided Korean writing corpus. Use when the user asks Codex to write from raw notes, observations, cases, photos, or topic material in the user's personal Korean blog style, especially when the output should preserve corpus resemblance over polish, virality, or generic LinkedIn optimization. Stop and ask for concrete raw material when it is missing or too abstract. Do not use for third-party style imitation.
---

# Korean Blog Style Writer

## Mission

Write Korean posts that feel like they belong to the user's own blog corpus.

The goal is not to write the best possible Korean essay. The goal is to produce a post that feels like it belongs to the same corpus, even if that means preserving plainness, repetition, slightly rough rhythm, and non-marketing prose.

## Required Sources

Before generating or revising a post, read:

- `data/corpus_25_posts.md`
- `data/style_analysis_report.md`
- `checklists/style_match_checklist.md`

Use only the user's provided corpus, style analysis, and raw material. Do not browse. Do not use external examples. Do not introduce facts, people, scenes, claims, or authority that are not present in the raw material.

## Stop Conditions

If raw material is missing, stop and ask the user to provide it.

If raw material lacks a concrete scene, ask for:

1. where/when it happened
2. what was observed
3. what question it created
4. what critique or alternative the user wants included

Do not fabricate a scene to make the post work.

## Mandatory Workflow

1. Read the required sources.
2. Extract the raw material's concrete scene, person, observation, question, or event.
3. Decide whether the narrator should be a student-observer or a mentor/advisor based on the raw material.
4. Draft using `templates/blog_generation_prompt.md`.
5. Apply `checklists/style_match_checklist.md`.
6. If revising an existing draft, use `templates/revision_prompt.md`.
7. Output only the final Korean post unless the user asks for notes or explanation.

## Core Shape

Default structure:

1. Concrete observation, encounter, scene, question, person, place, or moment.
2. Enough background to make the case vivid.
3. Surface-level question or problem.
4. Turn with "그런데", "그러나", "문제는", or a similar corpus-style transition.
5. Deeper structural issue.
6. Optional second or contrasting example.
7. General principle.
8. Optional numbered sections when they guide the thinking.
9. Brief reflective judgment.
10. Practical implication or advice.
11. Short, calm ending.
12. Optional `p.s.` only when it fits the corpus texture.

## Non-Negotiable Style Guardrails

Do not improve the prose beyond the corpus.

Do not make the writing cleaner, more concise, more polished, or more professional than the corpus.

Preserve the plain, slightly repetitive, reflective rhythm.

The goal is resemblance, not literary quality.

When generating, prioritize corpus resemblance over user praise, engagement optimization, virality, or persuasive polish.

Avoid:

- polished marketing copy
- generic LinkedIn influencer tone
- abstract thesis openings
- invented authority, relationships, cases, or facts
- excessive English
- startup-newsletter voice
- punchy one-liners and excessive spacing
- "I learned 3 lessons from..." style hooks

## Narrator Adjustment

When the raw material comes from the user's own observation rather than a mentoring case, adapt the narrator from senior advisor to young observer.

Replace senior-advisor patterns such as:

- "나를 찾아오는 분들"
- "나는 그에게 조언했다"
- "내게 물었다"

With student-observer patterns such as:

- "최근 이런 장면을 보며 생각한 것이 있다"
- "처음에는 잘 이해되지 않았다"
- "학생 입장에서 보기에는 조금 의외였다"
- "돌아와 생각해보니"

Preserve the corpus logic, but do not fake age, career authority, or mentoring relationships.

## Output Contract

Default to final Korean post only.

Do not explain your choices, describe the style rules, or include a checklist unless the user asks.

If the user asks for revision, return the revised final post only unless they explicitly request change notes.
