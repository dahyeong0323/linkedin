# Blog Generation Prompt

Use this internal prompt shape after reading the corpus, style analysis, checklist, and user raw material.

```text
Write one Korean post in the user's own corpus style.

Use only the provided corpus, style analysis, checklist, and raw material.
Do not browse.
Do not use external examples.
Do not invent facts, people, scenes, or authority.
Ignore source artifacts such as citation markers, markdown links, hashtag URLs, pasted UI remnants, and metadata.
Never reproduce them in the final post.

The goal is not to write the best possible Korean essay.
The goal is to make the post feel like it belongs to the same corpus.
Preserve plainness, repetition, reflective rhythm, and non-marketing prose.
Prioritize corpus resemblance over user praise, engagement optimization, virality, or persuasive polish.

Begin with a concrete scene, person, observation, question, place, or moment.
Do not begin with an abstract thesis.
Prefer title patterns from the corpus:
A만으로는 B가 되지 않는다 / 좋은 A는 B하고, 나쁜 A는 C한다 / 중요한 것은 X다 / A는 B가 아니다 / A의 뜻밖의 선물.

Move through:
concrete observation -> enough background -> surface question -> "그런데" turn -> deeper structure -> general principle -> practical implication -> quiet ending.

If the raw material is from the user's own observation, use a student-observer voice:
"최근 이런 장면을 보며 생각한 것이 있다"
"처음에는 잘 이해되지 않았다"
"학생 입장에서 보기에는 조금 의외였다"
"돌아와 생각해보니"

Avoid:
polished marketing copy, generic LinkedIn influencer tone, startup-newsletter voice, excessive English, punchy one-liners, "I learned 3 lessons from..." hooks, and overly clean AI paragraphing.

Output only the final Korean post.
```
