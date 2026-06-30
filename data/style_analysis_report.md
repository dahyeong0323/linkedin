# 한국어 블로그 문체 칼카피 엔진 설계 보고서

## 코퍼스 개요와 분석 범위

이번 분석은 사용자가 제공한 마크다운 코퍼스만을 대상으로 했다. 핵심 코퍼스는 번호가 붙은 장문 블로그 글 25편으로 이루어져 있고, 주제는 조직생활, 상사, 승진, 창업, 독립, 커리어 정체성, AI 시대의 일, 평가, 투자, 리더십, 퇴임 이후 삶, 선한 뜻과 이익 구조, 웰니스 관찰까지 폭넓게 분포한다. 다만 글의 외형이 다양해 보여도 실제 작동 방식은 매우 일관적이다. 대부분의 글은 “실제 사례 또는 관찰로 시작 → 표면 문제 제시 → 더 깊은 구조 해석 → 일반 원리 도출 → 조용한 결론”의 틀을 반복한다. 별도로 제공된 Olive Better 자료는 리테일 관찰형 글을 실험할 수 있는 입력 재료 문서로, 본 코퍼스에서 추출한 문체 규칙이 실제 새 주제에도 이식 가능한지 점검하는 데 유용하다.  

화자의 위치도 매우 선명하다. 이 글들의 화자는 단순한 에세이스트가 아니라, 오랜 조직 경험을 가진 조언자·관찰자·멘토·상담자에 가깝다. “한 분이 찾아왔다”, “내게 물었다”, “다양한 분들을 만나면서 느끼는 것이 있다”, “예전에 한 직장인을 만난 적이 있다” 같은 출발점이 반복되고, 글쓴이는 자신의 생각을 정답처럼 던지기보다 사례를 충분히 거친 뒤 일반론을 제시한다. 그러나 그 일반론은 결코 중립적인 보고서 톤이 아니라, 실제 사람을 많이 만나며 얻은 판단이 응축된 조용한 권고문에 가깝다. 

감정 온도는 낮거나 중간 정도다. 억지 감탄, 과장된 자기 드러냄, 지나치게 세련된 마케팅 카피는 거의 없고, 대신 담담함 속에 권위와 확신이 있다. 특히 누군가를 비난하기보다 “문제는 사람 자체가 아니라 구조와 맥락에 있다”는 식으로 재해석하는 습관이 강하게 보인다. 이 점 때문에 글은 차갑지 않으면서도 건조하게 읽히고, 조언문이지만 도덕 교훈처럼 들리지 않는다. 

이 코퍼스가 전제하는 독자는 “현재 조직 안에서 고민하는 사람”, “독립이나 제2 커리어를 고민하는 사람”, “리더십과 일의 구조를 배우고 싶은 사람”, “삶의 사건을 행동 원리로 바꾸고 싶은 사람”이다. 그래서 글은 단순 회상이 아니라 늘 적용 가능성을 향한다. 독자에게 전달되는 메시지는 늘 비슷하다. “이 사례를 남의 일로 보지 말고 당신의 구조를 다시 보라.” 이 독자 전제가 문체 전체를 지탱한다. 

## 문체의 핵심 DNA

이 코퍼스의 중심 문장 구조를 한 줄로 압축하면 이렇다.

**실제 사람과 사건을 통해 보이는 문제를 더 깊은 구조 문제로 재정의하고, 그 구조를 독자의 커리어와 행동 원리로 번역한 뒤, 짧고 단정한 결론으로 닫는다.** 

이 문체는 단순히 사례를 소개하는 것이 아니다. 핵심은 “처음 보기에는 A였는데, 조금 더 들여다보니 사실 B였다”라는 재해석의 리듬이다. 예를 들어 상사 문제는 성격 충돌처럼 보이지만 커리어 방향의 전환점으로 재해석되고, 묵묵히 일하는 태도는 미덕처럼 보이지만 실제로는 커뮤니케이션 부재의 문제로 이동하며, 좋은 커리어는 독립의 증거처럼 보이지만 실제 시장에서는 상품화 구조와 신뢰 노출의 문제로 전환된다. 즉 이 문체는 언제나 표면을 벗겨 구조를 보여준다. 

이 문체의 중요한 특징은 “사람”으로 시작하지만 “사람 평가”로 끝내지 않는다는 점이다. 글은 늘 어떤 인물이나 사례에서 출발하지만, 특정 인물의 성격을 낙인찍지 않는다. 대신 그 사람을 둘러싼 조직의 룰, 시장의 구조, 소비자의 행동, 사업의 수익 모델, 개인의 해석 습관 같은 상위 레벨 프레임으로 이동한다. 그래서 코퍼스 전체가 조언문처럼 보이면서도 심리학, 경영학, 조직론, 커리어론의 중간 지점을 차지하게 된다. 

또 하나의 핵심 DNA는 “권고의 방향성이 현실적”이라는 점이다. 추상적으로 “꿈을 가져라” “용기를 내라” 하고 끝나지 않고, “먼저 배경을 충분히 들어라”, “회사와 상사의 게임의 룰을 파악하라”, “경험을 상품화하라”, “기여와 기대를 표현하라”, “AI를 피드백 장치로 써라”, “무엇을 더할지가 아니라 무엇을 뺄지를 기록하라”처럼 구체적인 행동 단위로 떨어진다. 이것이 문체 복제를 위해 반드시 보존해야 하는 부분이다. 이 코퍼스는 감성형 글이 아니라, 관찰에서 행동 규칙을 뽑아내는 실전형 글쓰기 시스템이다. 

## 제목과 도입의 반복 공식

제목은 대체로 짧고 단정하며, 설명보다는 판단이나 역설을 앞세운다. 가장 빈번한 패턴은 “A만으로는 B가 되지 않는다”, “좋은 A는 B하고 나쁜 A는 C한다”, “중요한 것은 X다”, “A는 B가 아니다”, “A를 이해하라”, “A는 주어지는 것이 아니라 설계하는 것이다”, “A의 뜻밖의 선물” 같은 형태다. 제목만 읽어도 글이 단순 정보가 아니라 원리 제시형 글이라는 점을 알 수 있게 설계되어 있다. 끝에 `--` 또는 `---`가 붙는 경우도 반복적으로 나타나는데, 이는 시각적 습관이자 블로그/링크드인 업로드 시의 고유 질감을 만든다. 

| 제목 패턴 | 작동 방식 | 코퍼스 예시 유형 |
|---|---|---|
| A만으로는 B가 되지 않는다 | 독자가 믿는 단순 인과를 깨뜨림 | 좋은 커리어만으로는 사업이 되지 않는다 |
| 좋은 A는 B하고, 나쁜 A는 C한다 | 대비를 통해 교훈을 압축 | 좋은 상사는 성장시키고, 나쁜 상사는 움직이게 한다 |
| 중요한 것은 X다 | 결론을 제목 단계에서 선점 | 중요한 것은 다음 수다 |
| A를 이해하라 | 실천적 조언을 직설적으로 제시 | 당신의 조직의 게임의 룰을 이해하라 |
| A는 주어지는 것이 아니라 설계하는 것이다 | 정체성·커리어 글에 적합 | 자신의 정체성은 주어지는 것이 아니라 설계하는 것이다 |
| A의 뜻밖의 선물 | 부정적 사건을 재해석 | 극단의 경험이 주는 뜻밖의 선물 |

이 제목들의 공통점은 두 가지다. 첫째, “세련된 브랜드 카피”가 아니라 “오랜 경험에서 건져 올린 말”처럼 들린다. 둘째, 제목 자체가 이미 결론이지만, 글을 다 읽어야 그 판단이 설득되는 구조를 가진다. 즉 제목은 클릭 유도용 자극이 아니라, 글의 사고 방향을 선선언하는 장치다. 

도입은 더 정교하다. 거의 모든 글이 아래 몇 가지 오프닝 중 하나로 시작한다.

- “얼마 전 한 분을 만났다”
- “예전에 한 직장인을 만난 적이 있다”
- “최근 어떤 분의 글을 읽었다”
- “다양한 분들을 만나면서 느끼는 것이 있다”
- “한 사업가 분이 연락하셨다”
- “최근 만난 한 분이 이런 말씀을 하셨다” 

이 출발점의 핵심은 **추상 명제보다 구체 장면이 먼저 온다**는 것이다. “현대 조직에서 가장 중요한 것은…” 식으로 바로 들어가지 않는다. 먼저 사람, 질문, 대화, 사건, 혹은 관찰 장면 하나를 깐다. 그리고 그 장면을 2~4문장 정도 더 풀어 현실감을 준 뒤, “그런데”, “흥미롭게도”, “문제는”, “처음에는” 같은 신호어를 통해 깊은 문제로 이동한다. 따라서 Codex Skill은 절대 추상 명제로 시작하면 안 된다. 반드시 사례 또는 관찰 장면으로 시작해야 한다. 

다만 사용자의 경우 화자 연령과 위치가 다르므로, 코퍼스의 뼈대를 유지하되 주체만 변형하는 것이 중요하다. 원본 코퍼스의 화자가 “조언을 받으러 오는 사람을 만나는 사람”이라면, 사용자는 “관찰하고 배우는 학생 화자”에 가깝다. 따라서 시작 문장은 다음처럼 이식하는 편이 자연스럽다.

- “최근 이런 장면을 보며 생각한 것이 있다.”
- “며칠 전 한국에서 한 매장을 우연히 들어갔는데…”
- “처음에는 단순히 A처럼 보였다.”
- “학생 입장에서 보기에는 조금 의외였다.”
- “처음에는 잘 이해되지 않았는데, 돌아와 생각해보니…” 

## 본문 전개와 논리 설계

이 코퍼스의 본문은 겉보기에는 번호 나열형이지만, 실제로는 매우 정교한 계단식 논리 구조를 갖는다. 기본 골격은 다음과 같다.

첫째, 사례를 제시한다.  
둘째, 사례 속 인물 또는 상황의 배경을 준다.  
셋째, 독자가 바로 떠올릴 표면 문제를 제시한다.  
넷째, “그런데”를 사용해 더 깊은 문제로 전환한다.  
다섯째, 비슷한 사례나 반대 사례를 하나 더 붙인다.  
여섯째, 여기서 일반 원리를 추출한다.  
일곱째, 필요하면 “첫째, 둘째, 셋째”로 구조화한다.  
여덟째, 자신의 경험이나 판단을 짧게 끼워 넣는다.  
아홉째, 독자에게 적용 가능한 행동 조언으로 확장한다.  
열째, 짧고 단정한 문장으로 결론을 닫는다. 

이 구성은 글마다 다르게 보이지만, 핵심 템포는 놀라울 정도로 일정하다. 예를 들어 사례형 글은 초반 30~40%를 사례 설명에 쓰고, 중반에서 구조적 원리를 뽑고, 후반 20~30%에서 독자 적용과 결론으로 닫는다. 반면 관찰형 글은 사례가 하나가 아니라 “여러 사람에게서 반복적으로 본 장면”으로 바뀌지만, 결국 같은 구조를 따른다. “이런 분들을 자주 만난다 → 같은 고민이 반복된다 → 그런데 문제는 표면이 아니다 → 따라서 이렇게 봐야 한다”는 식이다. 

번호는 보고서의 차가운 질서가 아니라, 사고의 진행을 보조하는 손잡이처럼 쓰인다. 중요한 점은 번호를 붙였다고 각 번호가 꼭 한 문단으로 끝나지 않는다는 것이다. 하나의 번호 안에서 짧은 문단 여러 개로 나뉘기도 하고, 반대로 번호 없이 일반 문단만으로 밀어붙이는 글도 일부 존재한다. 그러나 번호가 붙을 때 공통적으로 일어나는 효과는 **독자가 “지금 논리가 하나씩 정리되고 있다”는 안도감**을 느끼게 만든다는 점이다. 이 점 때문에 Skill에서 번호 사용은 선택이 아니라 핵심 옵션으로 두는 것이 좋다. 특히 사례를 원리화할 때 번호는 매우 효과적이다. 

Olive Better 같은 리테일 관찰형 입력 재료를 이 구조에 넣을 때는 다음과 같은 재배치가 가능하다. 먼저 매장 방문 장면을 깔고, Olive Young과 Olive Better의 표면 차이를 묘사한 뒤, “그런데 더 중요한 질문은 왜 굳이 별도 브랜드를 만들었는가”로 전환한다. 이후 목적형 구매와 탐색형 소비의 차이, 뷰티 리테일과 웰니스 리테일의 차이, 오프라인 매장의 정당성, 선물용 편집샵으로서의 가능성을 क्रम차적으로 전개하면 코퍼스에 매우 가까운 논리 리듬이 형성된다. 즉 새 주제에서도 핵심은 관찰이 아니라 **관찰을 구조로 바꾸는 능력**이다. 

## 문장 리듬과 어투 장치

문장 수준에서 가장 중요한 특징은 “단정하지만 과열되지 않는다”는 점이다. 종결은 대개 `~다`, `~이다`, `~했다`, `~한다`를 기본으로 하고, 판단을 약간 유연하게 만들 때 `~일 수 있다`, `~에 가깝다`, `~처럼 보인다`, `~라고 생각한다`, `~할 필요가 있다`, `~기 쉽다`, `~라고 볼 수 있다`가 반복된다. 반대로 `~인 것 같다`, `~느껴졌다`, `~인 듯하다`, `~할 수도 있을 것 같다` 같은 망설임형 어미는 상대적으로 적다. 따라서 이 문체의 힘은 모호함이 아니라 **절제된 확신**에서 나온다. 

리듬도 중요하다. 짧은 문장으로 장면을 찍고, 그 다음 2~3문장으로 의미를 풀고, 다시 짧은 결론 문장으로 압축한다. 예를 들어 “처음에는 A처럼 보였다. 그런데 이야기를 더 들어보니 문제는 B였다.” 같은 2연타 구조가 많이 쓰이고, 그 뒤에 2~4문장짜리 설명 블록이 이어진다. 즉 아주 짧은 문장만으로 질주하지도 않고, 장황한 문단만으로 밀지도 않는다. 한 문단 안에서 장단을 섞으며 독자의 호흡을 조절한다. 

가장 핵심적인 연결어는 아래 묶음이다.

| 전환어 | 기능 |
|---|---|
| 그런데 / 그러나 / 다만 | 표면 문제에서 더 깊은 문제로 이동 |
| 반면 / 오히려 / 흥미롭게도 | 직관을 뒤집거나 비교 구조 형성 |
| 사실 / 생각해보니 / 이야기를 들으며 생각했다 | 판단을 부드럽게 삽입 |
| 결국 / 그러므로 / 이 지점에서 / 중요한 것은 | 일반 원리 도출과 결론 압축 |
| 다시 말해 / 이는 | 앞 문장을 구조적으로 재정리 |

이 연결어들은 단지 접속 부사가 아니라, 글의 사고 전환 표시등 역할을 한다. Codex Skill이 문체를 잘 흉내 내려면 이 표현들을 “많이”가 아니라 “정확한 위치에” 써야 한다. 특히 “그런데”는 본문 초중반에서 구조 전환을 여는 핵심 스위치이고, “중요한 것은”은 결론에 도달하는 신호어이며, “흥미롭게도”는 단순 정보가 아닌 관찰자의 시선을 드러내는 장치다. 

반복적으로 등장하는 문장 골격도 명확하다.  
“처음에는 A처럼 보였다.”  
“그런데 이야기를 더 들어보니 문제는 B였다.”  
“이것은 단순히 A의 문제가 아니다.”  
“오히려 B의 문제에 가깝다.”  
“이 사례는 중요한 사실을 보여준다.”  
“결국 중요한 것은 A가 아니라 B다.”  
“A는 좋은 태도다. 그러나 B라는 믿음은 위험하다.”  
“그러므로 A를 하려면 먼저 B를 이해할 필요가 있다.” 

이 문장 골격은 거의 템플릿 수준이다. 따라서 “칼카피” 목적의 Skill이라면 이를 노골적으로 규칙화해도 된다. 다만 중요한 것은 이 골격이 뜬금없이 나오면 안 되고, 반드시 사례 뒤에 붙어야 자연스럽다는 점이다. 이 문체는 추상 문장에서 힘이 생기는 것이 아니라, 사례를 밟고 올라갔을 때 힘이 생긴다. 

## 사례 처리 방식과 비유 시스템

사례는 실명보다 익명성이 기본이다. “한 직장인”, “한 사업가 분”, “예전에 만난 한 40대 직장인”, “최근 찾아온 분”, “한 리더”, “한 창업가”처럼 소개하고, 필요한 경우 업계·이력·상황·고민만 짧게 제공한다. 이 정보량은 매우 중요하다. 지나치게 세세하면 르포가 되고, 지나치게 추상적이면 설득력이 약해진다. 이 코퍼스는 그 중간을 잘 지킨다. “어떤 위치의 어떤 사람이 어떤 전환점에서 어떤 고민을 하고 있었는가” 정도만 선명하면 충분하다. 

또한 사례는 거의 항상 “한 사람의 특수성”에서 “많은 사람의 반복 구조”로 이동한다. 즉 개별 사례는 증거가 아니라 입구다. 글쓴이는 단 한 사람을 말하면서도 사실은 더 큰 패턴을 설명하고 있다. 그래서 사례 뒤에는 곧장 “이 사례는 중요한 사실을 보여준다”, “이는 많은 직장인이 오해하는 지점이다”, “흥미롭게도 이런 경우가 많다”, “결국 여기서 중요한 것은…” 같은 패턴이 이어진다. Skill은 이 이동을 반드시 포함해야 한다. 그렇지 않으면 단순 후기·회고·감상이 되고 만다. 

비유도 이 문체의 핵심이다. 다만 문학적 비유가 아니라 구조 설명용 비유다. 조직은 게임이고, 대기업은 축구, 스타트업은 농구이며, 일하는 방식은 운전이고, 안 쓰던 역량은 근육이다. 사업은 뜻이 아니라 이익 구조로 버티는 일이고, 독립은 경험을 시장이 사는 언어로 번역하는 일이다. 이런 비유들은 “있어 보이게” 하기 위한 장식이 아니라, 복잡한 구조를 한 번에 이해시키기 위한 도해 역할을 한다. 

Olive Better 입력 자료에도 같은 방식의 비유가 이미 잠재되어 있다. 예를 들어 Olive Young은 목적형 구매를 훈련한 플랫폼이고, Olive Better는 탐색형 소비를 설계하려는 실험 공간이며, 뷰티 리테일은 보이는 변화를 파는 곳이고, 웰니스 리테일은 보이지 않는 신뢰와 설명을 파는 곳이다. 또 기능성 본인 소비보다 선물용 편집샵으로 포지셔닝될 수 있다는 가설은, 이 코퍼스의 비유 시스템과 매우 잘 맞는다. “리테일은 제품을 놓는 공간이 아니라 소비 행동을 만드는 장치”라는 문장으로 압축하면 원 코퍼스의 어법에 가깝다. 

## 드리프트를 막는 재현 규칙

이 코퍼스를 어설프게 모방하면 쉽게 두 방향으로 무너진다. 하나는 지나치게 세련되고 깔끔한 AI 글로 가는 방향이고, 다른 하나는 감정 과잉의 개인 에세이로 가는 방향이다. 원 코퍼스는 둘 다 아니다. 문장은 약간 투박할 수 있고, 같은 표현이 반복될 수 있으며, 정리되지 않은 듯한 말맛이 남아 있을 수 있다. 그런데 그 반복과 투박함 속에 실제 경험에서 나온 확신이 녹아 있다. 따라서 Codex는 **문체를 다듬으려는 본능을 억제해야 한다.** 이것이 가장 중요하다. 

또한 절대 금지해야 할 것이 있다. 지나치게 “인사이트”, “브랜딩”, “전략적”, “큐레이션의 미학”, “경험의 전환점이었다”, “많은 것을 배웠다”, “값진 경험이었다” 같은 흔한 AI·링크드인 표현이다. 원 코퍼스는 훨씬 더 담백하고 생활어에 가깝다. 전문 개념이 나오더라도 바로 생활 언어로 풀고, 과시형 영어 남발도 거의 없다. 즉 이 문체의 세련됨은 “유행어를 잘 쓰는 세련됨”이 아니라, “복잡한 것을 쉽게 말하는 세련됨”이다. 

비판의 방식도 중요하다. 원 코퍼스는 “틀렸다”, “망한다”, “형편없다” 같은 공격적 판단을 피하고, 대신 “위험하다”, “아쉬움이 있었다”, “이 방식만으로는 부족하다”, “쉽지 않을 수 있다”, “아직 인식이 충분하지 않다” 같은 표현으로 비판을 구조화한다. 그리고 거의 항상 대안을 붙인다. 예컨대 “홍보가 부족하다”에서 끝내지 않고, “그보다 오프라인으로 갈 이유가 약하다”, “선물용 웰니스 편집샵으로 포지셔닝하는 편이 더 자연스럽다”는 식의 구조적 대안을 제시하는 편이 코퍼스 문체와 훨씬 가깝다. 

마지막으로, 사용자의 실제 위치를 고려한 미세 조정이 필요하다. 원 코퍼스의 화자는 다수의 직장인이 찾아오는 멘토 화자이므로, 그대로 복제하면 18세 학생의 화자로는 어색해질 수 있다. 그러나 사용자는 “관찰하는 학생”으로서 같은 문체를 이식할 수 있다. 핵심은 권위의 स्रोत을 바꾸는 것이다. 조언을 많이 해봐서 아는 사람이 아니라, 장면을 보고 구조를 읽어내는 사람으로 서면 된다. 즉 “나를 찾아오는 분들” 대신 “최근 이런 장면을 보며”, “학생 입장에서 보면”, “처음에는 잘 이해되지 않았는데”로 조정하면, 구조는 유지하면서 화자 위화감을 줄일 수 있다. 

## Codex용 단일 프롬프트

아래 프롬프트는 사용자의 요청대로 **오직 제공된 코퍼스만 사용해**, 사용자의 기존 블로그 글 문체를 최대한 가깝게 재현하도록 설계한 **단일 붙여넣기용 프롬프트**다. 이 프롬프트는 분석과 생성 지시를 한 번에 포함한다.

```text
You are Codex. Build and use a Korean blog writing Skill that precisely imitates my own writing style from the provided markdown corpus.

VERY IMPORTANT:
These texts are my own blog posts.
The goal is exact stylistic mimicry.
Do NOT generalize the style.
Do NOT modernize the style.
Do NOT polish the style.
Do NOT make it more professional, more elegant, more concise, or more AI-like.
Do NOT browse the internet.
Do NOT use external examples.
Do NOT use public references.
Use ONLY the markdown corpus and raw material I provide.

YOUR JOB HAS TWO PHASES:
Phase 1) Reverse-engineer the corpus.
Phase 2) Generate a Korean blog/LinkedIn-style post that sounds as close as possible to the corpus.

You must extract and reproduce the corpus at the following levels:

[1] TITLE STYLE
- Keep the title short, declarative, and slightly weighty.
- Strongly prefer these title mechanics:
  - “A만으로는 B가 되지 않는다”
  - “좋은 A는 B하고, 나쁜 A는 C한다”
  - “중요한 것은 X다”
  - “A를 이해하라”
  - “A는 주어지는 것이 아니라 설계하는 것이다”
  - contrast, warning, metaphor, or quiet conclusion in title form
- If appropriate, allow a trailing “--” or “---” like in the corpus.

[2] OPENING STYLE
- Never start with an abstract thesis.
- Start from a concrete encounter, scene, observation, question, person, place, or moment.
- Preferred openings:
  - “얼마 전…”
  - “최근…”
  - “예전에…”
  - “다양한 분들을 만나면서 느끼는 것이 있다.”
  - “한 분이…”
  - “며칠 전 …을 보며 생각한 것이 있다.”
- Because I am younger than the narrator in some corpus texts, adapt authority naturally when needed:
  - “학생 입장에서 보기에는…”
  - “처음에는 잘 이해되지 않았다.”
  - “처음에는 단순히 A처럼 보였다.”
  - “그런데 돌아와 생각해보니…”

[3] NARRATOR POSITION
- Write as an observer-thinker, not as a flashy content creator.
- Sound calm, firm, reflective, practical.
- Do not sound like a marketer.
- Do not sound like a generic LinkedIn influencer.
- Do not sound overly emotional.
- Do not attack people directly.
- Explain structures, incentives, behavior, positioning, context.

[4] CORE LOGIC
Default logic flow:
1. Start from one real observation / encounter / case / event.
2. Give just enough background.
3. Present the surface-level question or problem.
4. Turn with “그런데 / 그러나 / 문제는”.
5. Reveal a deeper structural issue.
6. If useful, add a second or contrasting example.
7. Extract the general principle.
8. If useful, structure with “첫째, 둘째, 셋째”.
9. Briefly insert my own reflective judgment.
10. Extend toward advice, implication, or broader interpretation.
11. End with a short, calm, memorable conclusion.
12. If it suits the context, add a short p.s. line.

[5] NUMBERING
- Use numbered sections often when the logic benefits from it.
- Numbering should feel like guided thinking, not a stiff report.
- Each numbered point may contain multiple paragraphs.
- Within a numbered section, you may also use “첫째, 둘째, 셋째”.

[6] SENTENCE RHYTHM
- Mix short and medium-length sentences.
- Use short transition sentences for turning points.
- Use 2–4 sentence explanatory clusters.
- Avoid literary flourish.
- Avoid hyper-clean AI paragraphing.
- Allow some slight repetition if that matches the corpus texture.
- End paragraphs with compressed judgment, not over-explanation.

[7] CONNECTIVE EXPRESSIONS
Use these naturally and frequently when appropriate:
- 그런데
- 그러나
- 다만
- 반면
- 오히려
- 흥미롭게도
- 사실
- 결국
- 그러므로
- 이 지점에서
- 문제는
- 중요한 것은
- 다시 말해
- 생각해보니
- 이야기를 들으며 생각했다

[8] RECURRING SENTENCE SKELETONS
Use these structures often, adapted to the topic:
- 처음에는 A처럼 보였다.
- 그런데 조금 더 들여다보니 문제는 B였다.
- 이것은 단순히 A의 문제가 아니다.
- 오히려 B의 문제에 가깝다.
- 이 사례는 중요한 사실을 보여준다.
- 결국 중요한 것은 A가 아니라 B다.
- A는 좋은 태도다. 그러나 B라는 믿음은 위험하다.
- A만으로는 부족하다. B가 필요하다.
- 사람들은 대개 A라고 생각한다. 그러나 현실에서는 B인 경우가 많다.
- 그러므로 A를 하려면 먼저 B를 이해할 필요가 있다.
- 나는 이 지점이 중요하다고 생각한다.
- 한번 생각해볼 필요가 있다.
- 기억할 필요가 있다.
- 주의할 필요가 있다.

[9] ENDING TONE
Prefer endings such as:
- ~다
- ~이다
- ~했다
- ~한다
- ~할 필요가 있다
- ~일 수 있다
- ~에 가깝다
- ~처럼 보인다
- ~라고 생각한다
- ~기 쉽다
- ~라고 볼 수 있다

Avoid overusing:
- ~인 것 같다
- ~느껴졌다
- ~인 듯하다
- ~할 수도 있을 것 같다

[10] CASE-HANDLING RULES
- Introduce people anonymously and functionally.
- Give only enough detail to make the case vivid.
- Do not over-narrate.
- Do not gossip.
- Move from “one person / one place / one event” to a broader repeated pattern.
- Always extract the structural significance of the case.

[11] METAPHOR SYSTEM
Use practical metaphors, not poetic ones.
Metaphors should clarify structure.
Preferred metaphor directions seen in the corpus:
- 조직 = 게임
- 일하는 방식 = 운전
- 역량 = 근육
- 사업 = 구조
- 독립 = 경험을 시장 언어로 번역하는 일
- 커리어 = 선택과 훈련의 누적
- 리테일 = 소비 행동을 만드는 장치
If the topic is retail / wellness / consumer behavior, use one concrete structural metaphor if it helps.

[12] CRITICISM STYLE
Critique sharply but calmly.
Prefer:
- “위험하다”
- “아쉬움이 있었다”
- “이 방식만으로는 부족하다”
- “쉽지 않을 수 있다”
- “아직 인식이 충분하지 않다”
Do NOT sound hostile.
After critique, offer a structural alternative.

[13] FORBIDDEN STYLE DRIFT
Never do the following:
- no polished marketing-copy voice
- no startup-newsletter tone
- no excessive English
- no exaggerated inspiration talk
- no “값진 경험이었다”
- no “많은 것을 배웠다”
- no generic LinkedIn self-branding language
- no excessive jargon like “인사이트 / 브랜딩 / 전략적으로” unless absolutely needed
- no overly neat AI smoothing
- do not erase the plain, slightly repetitive, lived-in texture

[14] SELF-CHECK BEFORE OUTPUT
Before finalizing, silently verify:
- Does the piece begin with a concrete observation or case?
- Does it avoid beginning with abstract thesis?
- Does it move from surface issue to deeper structure?
- Does it use the connective rhythm of the corpus?
- Does it sound like the same writerly world as the corpus?
- Does it avoid generic AI polish?
- Does it end quietly but memorably?

NOW DO THE FOLLOWING:
A) Read and internalize the corpus.
B) Extract the style rules silently.
C) Use the raw material below.
D) Write one full Korean post in the corpus style.
E) Do not explain your choices.
F) Output only the final post.

[CORPUS]
<<<PASTE MY MARKDOWN CORPUS HERE>>>

[RAW MATERIAL]
<<<PASTE MY NEW MATERIAL HERE>>>
```

이 프롬프트의 강점은 세 가지다. 첫째, 코퍼스를 단순 “참고”가 아니라 **절대적 스타일 기준**으로 고정한다는 점이다. 둘째, 제목·오프닝·문장 리듬·논리 전개·비판 방식·금지 드리프트를 모두 명시해서 Codex가 중간에 일반적인 AI 문체로 도망가지 못하게 막는다. 셋째, 새 주제가 사람 사례이든, 리테일 관찰이든, 투자든, 학교 생활이든, 결국 **“구체 사례 → 구조 해석 → 일반 원리 → 짧은 결론”**으로 압축되도록 설계했다는 점이다. 이 구조가 바로 이번 코퍼스의 가장 중요한 재현 단위다. 

Olive Better 자료처럼 관찰형 리테일 입력을 넣을 경우에도 이 프롬프트는 잘 작동한다. 그 이유는 원 코퍼스가 본질적으로 특정 산업 전문 글이 아니라 **사건을 구조로 읽어내는 글쓰기 시스템**이기 때문이다. 따라서 새 입력이 “한국에서 우연히 본 매장”이어도, Codex는 이를 “브랜드 확장 전략”, “목적형 구매와 탐색형 소비의 차이”, “오프라인 리테일의 정당성”, “선물용 웰니스 편집샵 가설”로 해석하며 코퍼스 문체 안에 집어넣을 수 있다. 

결국 이 코퍼스의 복제 포인트는 화려한 문장이 아니다. **사례를 열고, 구조를 드러내고, 원리를 정리하고, 조용히 닫는 방식**이다. 제목은 단정해야 하고, 도입은 장면에서 시작해야 하며, 본문은 “그런데” 이후 깊어져야 하고, 결론은 짧아야 한다. 이 규칙만 정확히 보존하면, 새 주제도 높은 확률로 같은 블로그 세계관 안에 들어오게 된다. 