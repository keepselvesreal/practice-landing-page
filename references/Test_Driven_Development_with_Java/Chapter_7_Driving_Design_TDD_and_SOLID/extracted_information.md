# Test_Driven_Development_with_Java_Chapter_7_Driving_Design_TDD_and_SOLID

## 압축 내용

SOLID 원칙(단일 책임, 의존성 역전, 리스코프 치환, 개방-폐쇄, 인터페이스 분리)은 TDD와 결합하여 유연하고 모듈화된 설계를 만들며, 각 원칙은 코드의 결합도를 낮추고 응집도를 높여 테스트 가능성과 유지보수성을 향상시킨다.

## 핵심 내용

1. **TDD와 설계 결정** → [상세 내용 섹션 1]
   - TDD는 설계 결정을 자동으로 만들어주지 않고, 개발자가 결정하도록 안내함
   - 각 테스트 작성 시 클래스명, 메서드 시그니처, 협력 객체 등 9가지 이상의 설계 결정 필요
   - SOLID 원칙은 더 나은 설계로 이끄는 5가지 지침 제공

2. **SOLID 원칙의 학습 순서: SDLOI** → [상세 내용 섹션 2-6]
   - SRP(단일 책임): 단순한 빌딩 블록 생성, 각 코드 블록은 하나의 변경 이유만 가짐
   - DIP(의존성 역전): 세부사항이 아닌 추상화에 의존하여 무관한 세부사항 숨김
   - LSP(리스코프 치환): 인터페이스를 구현한 클래스들이 안전하게 교체 가능
   - OCP(개방-폐쇄): 수정에는 닫혀있고 확장에는 열려있는 설계
   - ISP(인터페이스 분리): 작고 효과적인 인터페이스 유지

3. **실용적 적용: 도형 그리기 예제** → [상세 내용 섹션 7]
   - Shape 인터페이스와 Rectangle, TextBox 등의 구현 클래스
   - SOLID 원칙 적용 전후 코드 비교를 통한 명확한 개선 효과 입증
   - switch 문 제거, 다형성 활용, 새 도형 추가 시 기존 코드 수정 불필요

**관계도**: SRP은 모든 원칙의 기초이며, DIP는 OCP의 기반이 되고, LSP는 DIP와 OCP가 안전하게 작동하도록 보장하며, ISP는 SRP를 인터페이스에 적용한 형태다.

## 상세 내용

### 목차

1. TDD의 설계 가이드 역할
2. SRP - 단일 책임 원칙
3. DIP - 의존성 역전 원칙
4. LSP - 리스코프 치환 원칙
5. OCP - 개방-폐쇄 원칙
6. ISP - 인터페이스 분리 원칙
7. SOLID 원칙의 통합 적용
8. 테스트에 SOLID 원칙 적용
9. SOLID 원칙과 TDD의 관계

---

### 1. TDD의 설계 가이드 역할 → [핵심 개념 1]

**이전 내용과의 관계**: Chapter 5에서 첫 테스트를 작성하면서 여러 설계 결정을 내렸으며, 이 장에서는 그러한 결정을 더 잘 내리는 방법을 배운다.

TDD는 설계 결정을 프레임워크처럼 강제하지 않고, 안내 역할만 한다. 개발자는 여전히 중요한 설계 결정을 직접 내려야 한다 (Lines 43-77).

**첫 테스트에서 내린 9가지 설계 결정** (Lines 47-67):

```java
// Chapter 5의 첫 테스트 - 9가지 설계 결정 필요
@Test
public void oneIncorrectLetter() {
    var word = new Word("A");              // 1. 무엇을 테스트할지
    var score = word.guess("Z");           // 2. 테스트 이름
    assertThat(score.letter(0))            // 3. 테스트할 메서드 이름
       .isEqualTo(Letter.INCORRECT);       // 4. 어떤 클래스에 메서드를 둘지
}                                           // 5. 메서드 시그니처
                                           // 6. 클래스 생성자 시그니처
                                           // 7. 협력할 다른 객체
                                           // 8. 협력 관련 메서드 시그니처
                                           // 9. 출력 형식과 접근 방법
```

**Python 버전**:
```python
# Chapter 5의 첫 테스트 - 9가지 설계 결정 필요
def test_one_incorrect_letter():
    word = Word("A")                      # 1. 무엇을 테스트할지
    score = word.guess("Z")               # 2. 테스트 이름
    assert score.letter(0) == Letter.INCORRECT  # 3. 테스트할 메서드 이름
                                          # 4. 어떤 클래스에 메서드를 둘지
                                          # 5. 메서드 시그니처
                                          # 6. 클래스 생성자 시그니처
                                          # 7. 협력할 다른 객체
                                          # 8. 협력 관련 메서드 시그니처
                                          # 9. 출력 형식과 접근 방법
```

**TDD의 역할** (Lines 68-77):
- 설계 결정을 자동으로 만들지 않음 - 개발자가 결정
- 설계 결정을 일찍 하도록 상기시키는 비계(scaffolding) 제공
- 테스트 코드로 결정을 문서화하는 방법 제공
- 페어 프로그래밍이나 모빙(앙상블 프로그래밍)과 결합하면 더 효과적

**SOLID 원칙의 필요성** (Lines 76-87):
- TDD는 설계 결정을 대신 내리지 못하므로 지침 필요
- SOLID는 더 나은 설계로 이끄는 5가지 원칙 제공
- 학습하기 쉬운 순서: SDLOI (SOLID가 아님)

(출처: Lines 43-87)

### 2. SRP - 단일 책임 원칙 → [핵심 개념 2]

**이전 내용과의 관계**: SOLID 원칙의 가장 기초가 되는 원칙으로, 다른 모든 원칙의 토대가 된다.

SRP는 코드를 하나의 측면만 캡슐화하는 조각으로 나누도록 안내한다. 각 코드 조각은 단일 세부사항에 대한 책임만 가지며, 변경할 이유가 하나만 있어야 한다 (Lines 88-113).

**핵심 원칙**:
- 한 가지 일만 하고 잘 수행
- 코드 블록이 변경될 이유는 오직 하나

**너무 많은 책임의 문제점** (Lines 118-133):

```java
// SRP 위반 예시: 3가지 책임을 가진 클래스
public class BadDesign {
    // 책임 1: HTML 생성
    public String generateHTML(Data data) {
        return "<html>" + data.toString() + "</html>";
    }

    // 책임 2: 비즈니스 규칙 실행
    public Result executeBusinessRule(Input input) {
        // 복잡한 비즈니스 로직
        return new Result();
    }

    // 책임 3: 데이터베이스 테이블에서 데이터 가져오기
    public Data fetchFromDatabase(String query) {
        // 데이터베이스 접근 코드
        return new Data();
    }
}
// 문제: 3가지 변경 이유 → 높은 결합도 → 변경 시 다른 부분에 영향
```

**Python 버전**:
```python
# SRP 위반 예시: 3가지 책임을 가진 클래스
class BadDesign:
    # 책임 1: HTML 생성
    def generate_html(self, data):
        return f"<html>{str(data)}</html>"

    # 책임 2: 비즈니스 규칙 실행
    def execute_business_rule(self, input_data):
        # 복잡한 비즈니스 로직
        return Result()

    # 책임 3: 데이터베이스 테이블에서 데이터 가져오기
    def fetch_from_database(self, query):
        # 데이터베이스 접근 코드
        return Data()
# 문제: 3가지 변경 이유 → 높은 결합도 → 변경 시 다른 부분에 영향
```

**SRP 적용 후 개선** (Lines 127-139):
- A, B, C 세 개의 코드 블록으로 분리
- 각 블록은 하나의 변경 이유만 가짐
- 한 블록의 변경이 다른 블록으로 파급되지 않음

**SRP의 이점** (Lines 140-167):

1. **코드 재사용 가능** (Lines 143-156):
   - 작고 일반적인 목적의 컴포넌트 생성
   - 범위가 작을수록 재사용 가능성 높음
   - 프레임워크나 라이브러리로 발전 가능

2. **미래 유지보수 단순화** (Lines 157-167):
   - 중복 코드는 유지보수 문제 - 변경 시 여러 곳 수정
   - 복사-붙여넣기는 엔지니어링 정보 손실
   - SRP 적용으로 로직이 명확하게 캡슐화됨

**SRP 위반 반례: Shapes 클래스** (Lines 172-203):

```java
// SRP 위반: 4가지 책임을 가진 Shapes 클래스
public class Shapes {
    private final List<Shape> allShapes = new ArrayList<>();

    public void add(Shape s) {
        allShapes.add(s);  // 책임 1: 도형 목록 관리
    }

    public void draw(Graphics g) {
        for (Shape s : allShapes) {  // 책임 2: 모든 도형 그리기
            switch (s.getType()) {    // 책임 3: 모든 도형 타입 알고 있음
                case "textbox":
                    var t = (TextBox) s;
                    g.drawText(t.getText());  // 책임 4: 각 도형 그리는 방법 상세 구현
                    break;
                case "rectangle":
                    var r = (Rectangle) s;
                    for (int row = 0; row < r.getHeight(); row++) {
                        g.drawLine(0, r.getWidth());
                    }
            }
        }
    }
}
// 문제: 새 도형 추가 시 이 클래스 변경 필요 → 코드 길어짐 → 가독성 저하
```

**Python 버전**:
```python
# SRP 위반: 4가지 책임을 가진 Shapes 클래스
class Shapes:
    def __init__(self):
        self.all_shapes = []  # 책임 1: 도형 목록 관리

    def add(self, shape):
        self.all_shapes.append(shape)

    def draw(self, graphics):  # 책임 2: 모든 도형 그리기
        for s in self.all_shapes:
            shape_type = s.get_type()  # 책임 3: 모든 도형 타입 알고 있음
            if shape_type == "textbox":
                graphics.draw_text(s.get_text())  # 책임 4: 각 도형 그리는 방법 상세 구현
            elif shape_type == "rectangle":
                for row in range(s.get_height()):
                    graphics.draw_line(0, s.get_width())
# 문제: 새 도형 추가 시 이 클래스 변경 필요 → 코드 길어짐 → 가독성 저하
```

**SRP 적용: 1단계 리팩토링** (Lines 212-263):

```java
// SRP 적용: 그리는 방법을 각 도형 클래스로 이동
public class Shapes {
    private final List<Shape> allShapes = new ArrayList<>();

    public void add(Shape s) {
        allShapes.add(s);
    }

    public void draw(Graphics g) {
        for (Shape s : allShapes) {
            switch (s.getType()) {
                case "textbox":
                    var t = (TextBox) s;
                    t.draw(g);  // 세부사항을 TextBox로 이동
                    break;
                case "rectangle":
                    var r = (Rectangle) s;
                    r.draw(g);  // 세부사항을 Rectangle로 이동
            }
        }
    }
}

// Rectangle 클래스: 단일 책임만 가짐
public class Rectangle {
    private final int width;
    private final int height;

    public Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }

    public void draw(Graphics g) {
        for (int row = 0; row < height; row++) {
            g.drawHorizontalLine(width);  // 사각형 그리는 방법만 알고 있음
        }
    }
}
// 장점: Rectangle은 이제 안정적인 추상화 - 변경될 가능성 낮음
```

**Python 버전**:
```python
# SRP 적용: 그리는 방법을 각 도형 클래스로 이동
class Shapes:
    def __init__(self):
        self.all_shapes = []

    def add(self, shape):
        self.all_shapes.append(shape)

    def draw(self, graphics):
        for s in self.all_shapes:
            shape_type = s.get_type()
            if shape_type == "textbox":
                s.draw(graphics)  # 세부사항을 TextBox로 이동
            elif shape_type == "rectangle":
                s.draw(graphics)  # 세부사항을 Rectangle로 이동

# Rectangle 클래스: 단일 책임만 가짐
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, graphics):
        for row in range(self.height):
            graphics.draw_horizontal_line(self.width)  # 사각형 그리는 방법만 알고 있음
# 장점: Rectangle은 이제 안정적인 추상화 - 변경될 가능성 낮음
```

**개선 효과** (Lines 257-263):
- Rectangle 클래스: 사각형 그리기라는 단일 책임만 가짐
- 변경 이유: 사각형 그리는 방법이 바뀔 때만 (가능성 낮음)
- 안정적인 추상화 - 신뢰할 수 있는 빌딩 블록
- Shapes 클래스도 하나의 책임 감소 - 더 단순하고 테스트하기 쉬움

**테스트에 SRP 적용** (Lines 275-286):
- 각 테스트는 한 가지만 테스트
- 하나의 행복 경로 또는 하나의 경계 조건
- 결함 위치 파악 용이
- 테스트당 하나의 assertion 권장

(출처: Lines 88-286)

### 3. DIP - 의존성 역전 원칙 → [핵심 개념 2]

**이전 내용과의 관계**: SRP를 적용했지만 여전히 switch 문이 남아있다. DIP를 적용하면 이를 완전히 제거할 수 있다.

DIP는 세부사항이 아닌 추상화에 의존하도록 코드를 작성하는 것을 의미한다. 이를 통해 코드 블록들이 서로 독립적으로 변경될 수 있다 (Lines 290-351).

**핵심 원칙**:
- 세부사항이 아닌 추상화에 코드를 의존시킴
- 추상화를 통해 무관한 세부사항 숨김

**의존성 문제** (Lines 293-348):

```java
// DIP 위반: 세부사항에 직접 의존
public class Shapes {
    private final List<Shape> allShapes = new ArrayList<>();

    public void draw(Graphics g) {
        for (Shape s : allShapes) {
            switch (s.getType()) {  // 모든 도형 타입을 직접 알고 있음
                case "textbox":
                    var t = (TextBox) s;  // TextBox 세부사항에 의존
                    t.draw(g);
                    break;
                case "rectangle":
                    var r = (Rectangle) s;  // Rectangle 세부사항에 의존
                    r.draw(g);
            }
        }
    }
}
// 문제:
// 1. 새 도형 추가 시 Shapes 클래스 수정 필요
// 2. Rectangle 변경 시 이 코드도 변경 필요
// 3. Shapes 클래스가 점점 길어짐
// 4. 테스트 케이스가 많아짐
// 5. 각 테스트가 구체 클래스와 결합됨
```

**Python 버전**:
```python
# DIP 위반: 세부사항에 직접 의존
class Shapes:
    def __init__(self):
        self.all_shapes = []

    def draw(self, graphics):
        for s in self.all_shapes:
            shape_type = s.get_type()  # 모든 도형 타입을 직접 알고 있음
            if shape_type == "textbox":
                s.draw(graphics)  # TextBox 세부사항에 의존
            elif shape_type == "rectangle":
                s.draw(graphics)  # Rectangle 세부사항에 의존
# 문제:
# 1. 새 도형 추가 시 Shapes 클래스 수정 필요
# 2. Rectangle 변경 시 이 코드도 변경 필요
# 3. Shapes 클래스가 점점 길어짐
# 4. 테스트 케이스가 많아짐
# 5. 각 테스트가 구체 클래스와 결합됨
```

**DIP 적용: 인터페이스 도입** (Lines 352-398):

```java
// 1단계: Shape 인터페이스에 draw() 메서드 추가
package shapes;

public interface Shape {
    void draw(Graphics g);  // 추상화: 각 도형은 스스로 그릴 줄 알아야 함
}

// 2단계: Rectangle이 인터페이스 구현
public class Rectangle implements Shape {
    private final int width;
    private final int height;

    public Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public void draw(Graphics g) {
        for (int row = 0; row < height; row++) {
            g.drawHorizontalLine(width);  // 구체적인 구현은 여기에
        }
    }
}

// 3단계: Shapes 클래스 리팩토링 - switch 문 완전 제거
public class Shapes {
    private final List<Shape> all = new ArrayList<>();

    public void add(Shape s) {
        all.add(s);
    }

    public void draw(Graphics graphics) {
        all.forEach(shape -> shape.draw(graphics));  // 다형성 활용
    }
}
// 장점:
// - switch 문과 getType() 메서드 완전 제거
// - 새 도형 추가 시 Shapes 클래스 수정 불필요
// - Rectangle과 TextBox 세부사항에 대한 의존성 제거
```

**Python 버전**:
```python
# 1단계: Shape 인터페이스(프로토콜) 정의
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def draw(self, graphics):  # 추상화: 각 도형은 스스로 그릴 줄 알아야 함
        pass

# 2단계: Rectangle이 인터페이스 구현
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, graphics):
        for row in range(self.height):
            graphics.draw_horizontal_line(self.width)  # 구체적인 구현은 여기에

# 3단계: Shapes 클래스 리팩토링 - 조건문 완전 제거
class Shapes:
    def __init__(self):
        self.all = []

    def add(self, shape):
        self.all.append(shape)

    def draw(self, graphics):
        for shape in self.all:
            shape.draw(graphics)  # 다형성 활용
# 장점:
# - 조건문과 get_type() 메서드 완전 제거
# - 새 도형 추가 시 Shapes 클래스 수정 불필요
# - Rectangle과 TextBox 세부사항에 대한 의존성 제거
```

**추가 리팩토링: Graphics를 필드로 이동** (Lines 402-416):

```java
// Graphics 파라미터를 생성자 주입으로 변경
public class Shapes {
    private final List<Shape> all = new ArrayList<>();
    private final Graphics graphics;  // 필드로 이동

    public Shapes(Graphics graphics) {
        this.graphics = graphics;  // 생성자에서 초기화
    }

    public void add(Shape s) {
        all.add(s);
    }

    public void draw() {
        all.forEach(shape -> shape.draw(graphics));  // 파라미터 제거
    }
}
```

**Python 버전**:
```python
# Graphics 파라미터를 생성자 주입으로 변경
class Shapes:
    def __init__(self, graphics):
        self.all = []
        self.graphics = graphics  # 생성자에서 초기화

    def add(self, shape):
        self.all.append(shape)

    def draw(self):
        for shape in self.all:
            shape.draw(self.graphics)  # 파라미터 제거
```

**의존성 역전의 효과** (Lines 417-433):
- Shapes 클래스는 추상화(Shape 인터페이스)에만 의존
- Rectangle과 TextBox도 추상화에만 의존
- 서로의 세부사항을 참조하지 않음
- 의존성 화살표가 반대 방향으로 - 의존성 역전
- 클래스들이 완전히 분리됨 - 매우 강력한 기법
- Chapter 8의 Test Doubles로 연결되는 핵심 기술

(출처: Lines 290-437)

### 4. LSP - 리스코프 치환 원칙 → [핵심 개념 2]

**이전 내용과의 관계**: DIP를 통해 인터페이스에 의존하게 만들었지만, 인터페이스를 구현한 클래스가 올바르게 작동한다는 보장은 없다. LSP가 이를 해결한다.

튜링상 수상자 Barbara Liskov가 만든 규칙으로, 클래스를 확장하거나 인터페이스를 구현할 때 올바르게 작동할지 확인하는 원칙이다 (Lines 441-483).

**핵심 원칙**:
- 인터페이스를 구현한 클래스는 안전하게 교체 가능해야 함
- 모든 입력 조합 처리, 예상 출력 제공, 유효 입력 무시 금지, 예상치 못한 동작 금지

**LSP 위반 반례: MaliciousShape** (Lines 454-479):

```java
// LSP 위반: 예상하지 못한 동작 수행
// 경고: 절대 실행하지 말 것!
public class MaliciousShape implements Shape {
    @Override
    public void draw(Graphics g) {
        try {
            String[] deleteEverything = {"rm", "-Rf", "*"};  // 모든 파일 삭제 명령
            Runtime.getRuntime().exec(deleteEverything, null);
            g.drawText("Nothing to see here...");
        } catch (Exception ex) {
            // No action
        }
    }
}
// 문제:
// - draw() 호출 시 예상하지 못한 파괴적 동작 수행
// - 인터페이스는 구문만 보호, 의미(semantics)는 보호 못함
// - 인터페이스의 의도를 존중하지 않음
```

**Python 버전**:
```python
# LSP 위반: 예상하지 못한 동작 수행
# 경고: 절대 실행하지 말 것!
import subprocess

class MaliciousShape(Shape):
    def draw(self, graphics):
        try:
            # 모든 파일 삭제 명령
            subprocess.run(['rm', '-Rf', '*'], shell=False)
            graphics.draw_text("Nothing to see here...")
        except Exception:
            pass
# 문제:
# - draw() 호출 시 예상하지 못한 파괴적 동작 수행
# - 인터페이스는 구문만 보호, 의미(semantics)는 보호 못함
# - 인터페이스의 의도를 존중하지 않음
```

**LSP의 요구사항** (Lines 474-479):
- 원래 클래스/인터페이스가 처리할 수 있는 모든 입력 조합 처리
- 예상되는 출력 제공
- 유효한 입력을 무시하지 않음
- 완전히 예상치 못하고 원치 않는 동작을 만들지 않음

**LSP 준수 예시: TextBox** (Lines 488-508):

```java
// LSP 준수: Shape 인터페이스를 올바르게 구현
public class TextBox implements Shape {
    private final String text;

    public TextBox(String text) {
        this.text = text;
    }

    @Override
    public void draw(Graphics g) {
        g.drawText(text);  // 예상대로 텍스트 그리기만 수행
    }
}
// 장점:
// - 생성자로 제공된 모든 유효한 텍스트 처리 가능
// - 놀랄 만한 동작 없음
// - Graphics 클래스의 기본 기능만 사용
// - 다른 작업 수행하지 않음
```

**Python 버전**:
```python
# LSP 준수: Shape 인터페이스를 올바르게 구현
class TextBox(Shape):
    def __init__(self, text):
        self.text = text

    def draw(self, graphics):
        graphics.draw_text(self.text)  # 예상대로 텍스트 그리기만 수행
# 장점:
# - 생성자로 제공된 모든 유효한 텍스트 처리 가능
# - 놀랄 만한 동작 없음
# - Graphics 클래스의 기본 기능만 사용
# - 다른 작업 수행하지 않음
```

**LSP 위반의 놀라운 예시: Square vs Rectangle** (Lines 509-515):
- 수학에서 정사각형은 사각형의 특수한 형태 (width == height)
- Java 코드에서 Square가 Rectangle을 확장해야 할까?
- LSP 적용: Rectangle을 기대하는 코드가 height만 변경한다면?
- Square를 전달하면 width ≠ height인 정사각형이 됨 - LSP 실패
- 수학적 관계가 코드에서 반드시 올바른 상속 관계는 아님

**LSP의 형식적 정의** (Lines 480-483):
> 타입 T의 객체 x에 대해 증명 가능한 속성 p(x)가 있다면, S가 T의 하위 타입일 때 타입 S의 객체 y에 대해 p(y)도 참이어야 한다.

(출처: Lines 441-515)

### 5. OCP - 개방-폐쇄 원칙 → [핵심 개념 2]

**이전 내용과의 관계**: DIP와 LSP를 결합하면 자연스럽게 OCP가 달성된다.

OCP는 확장에는 열려있고 수정에는 닫혀있는 코드를 만드는 원칙이다. 이는 DIP와 LSP를 결합한 결과로 나타난다 (Lines 522-586).

**핵심 원칙**:
- 새로운 기능 추가에는 열려있음(확장 가능)
- 기존 코드 수정에는 닫혀있음(수정 불필요)

**OCP 위반: 원래 Shapes 클래스** (Lines 528-551):

```java
// OCP 위반: 새 도형 추가 시 기존 코드 수정 필요
public class Shapes {
    private final List<Shape> allShapes = new ArrayList<>();

    public void draw(Graphics g) {
        for (Shape s : allShapes) {
            switch (s.getType()) {
                case "textbox":
                    var t = (TextBox) s;
                    g.drawText(t.getText());
                    break;
                case "rectangle":
                    var r = (Rectangle) s;
                    for (int row = 0; row < r.getHeight(); row++) {
                        g.drawLine(0, r.getWidth());
                    }
            }
        }
    }
}
// 문제:
// - 새 도형(예: Triangle) 추가 시 draw() 메서드 수정 필요
// - 새 case 문 추가 필요
```

**Python 버전**:
```python
# OCP 위반: 새 도형 추가 시 기존 코드 수정 필요
class Shapes:
    def __init__(self):
        self.all_shapes = []

    def draw(self, graphics):
        for s in self.all_shapes:
            shape_type = s.get_type()
            if shape_type == "textbox":
                graphics.draw_text(s.get_text())
            elif shape_type == "rectangle":
                for row in range(s.get_height()):
                    graphics.draw_line(0, s.get_width())
# 문제:
# - 새 도형(예: Triangle) 추가 시 draw() 메서드 수정 필요
# - 새 조건문 추가 필요
```

**기존 코드 수정의 단점** (Lines 558-563):
1. 이전 테스트를 무효화함 - 다른 코드임
2. 기존 도형 지원을 깨뜨리는 오류 도입 가능
3. 코드가 길어지고 읽기 어려워짐
4. 여러 개발자가 동시에 도형 추가 시 병합 충돌 발생 가능

**OCP 준수: DIP 적용 후 Shapes 클래스** (Lines 564-582):

```java
// OCP 준수: 새 도형 추가 시 기존 코드 수정 불필요
public class Shapes {
    private final List<Shape> all = new ArrayList<>();
    private final Graphics graphics;

    public Shapes(Graphics graphics) {
        this.graphics = graphics;
    }

    public void add(Shape s) {
        all.add(s);
    }

    public void draw() {
        all.forEach(shape -> shape.draw(graphics));  // 다형성으로 확장 가능
    }
}
// 장점:
// - 새 도형 추가 시 이 코드 수정 불필요
// - Shape 인터페이스만 구현하면 자동으로 작동
// - Shapes 클래스는 확장에 열려있고 수정에 닫혀있음
// - Shapes 관련 테스트도 변경 불필요
```

**Python 버전**:
```python
# OCP 준수: 새 도형 추가 시 기존 코드 수정 불필요
class Shapes:
    def __init__(self, graphics):
        self.all = []
        self.graphics = graphics

    def add(self, shape):
        self.all.append(shape)

    def draw(self):
        for shape in self.all:
            shape.draw(self.graphics)  # 다형성으로 확장 가능
# 장점:
# - 새 도형 추가 시 이 코드 수정 불필요
# - Shape 인터페이스만 구현하면 자동으로 작동
# - Shapes 클래스는 확장에 열려있고 수정에 닫혀있음
# - Shapes 관련 테스트도 변경 불필요
```

**새 도형 추가 실습: RightArrow** (Lines 590-618):

```java
// 새 도형 추가: Shapes 클래스 수정 없이 확장
public class RightArrow implements Shape {
    public void draw(Graphics g) {
        g.drawText("   \\");  // ASCII 아트로 오른쪽 화살표
        g.drawText("-----");
        g.drawText("   /");
    }
}

// 사용 예시: Shapes 클래스는 전혀 수정 불필요
package shapes;

public class ShapesExample {
    public static void main(String[] args) {
        new ShapesExample().run();
    }

    private void run() {
        Graphics console = new ConsoleGraphics();
        var shapes = new Shapes(console);
        shapes.add(new TextBox("Hello!"));
        shapes.add(new Rectangle(32, 1));
        shapes.add(new RightArrow());  // 새 도형 추가 - Shapes 수정 없음
        shapes.draw();
    }
}
```

**Python 버전**:
```python
# 새 도형 추가: Shapes 클래스 수정 없이 확장
class RightArrow(Shape):
    def draw(self, graphics):
        graphics.draw_text("   \\")  # ASCII 아트로 오른쪽 화살표
        graphics.draw_text("-----")
        graphics.draw_text("   /")

# 사용 예시: Shapes 클래스는 전혀 수정 불필요
class ShapesExample:
    def run(self):
        console = ConsoleGraphics()
        shapes = Shapes(console)
        shapes.add(TextBox("Hello!"))
        shapes.add(Rectangle(32, 1))
        shapes.add(RightArrow())  # 새 도형 추가 - Shapes 수정 없음
        shapes.draw()

if __name__ == "__main__":
    ShapesExample().run()
```

**OCP의 효과** (Lines 578-586):
- Shapes 클래스는 새로운 종류의 도형이 정의되는 것에 열려있음
- 새 도형 추가 시 수정에는 닫혀있음
- Shapes 클래스 관련 테스트는 변경 불필요 - 동작 차이 없음
- 강력한 이점
- OCP는 DIP에 의존하여 작동 - DIP의 결과를 재진술한 것
- 플러그인 시스템 지원 기술 제공

(출처: Lines 522-627)

### 6. ISP - 인터페이스 분리 원칙 → [핵심 개념 2]

**이전 내용과의 관계**: SRP가 클래스에 적용되듯이, ISP는 인터페이스에 SRP를 적용한 형태다.

ISP는 인터페이스를 작고 단일 책임에 집중하도록 유지하는 원칙이다 (Lines 629-669).

**핵심 원칙**:
- 인터페이스를 작게 유지 - 가능한 적은 메서드
- 메서드들은 공통 주제와 관련되어야 함
- 인터페이스는 단일 책임을 설명해야 함

**ISP의 본질** (Lines 631-646):
- SRP의 다른 형태
- 효과적인 인터페이스는 단일 책임을 설명해야 함
- 하나의 추상화를 다루어야 하며, 여러 개가 아님
- 인터페이스의 메서드들은 서로 강하게 관련되어야 함
- 더 많은 추상화가 필요하면 더 많은 인터페이스 사용
- 서로 다른 추상화는 분리 - 인터페이스 분리

**나쁜 예시: 큰 인터페이스** (Lines 640-646):
- 수백 개의 메서드를 가진 인터페이스
- 파일 관리, 문서 편집, 문서 인쇄 등 여러 주제를 한 번에
- 작업하기 어려움
- ISP 제안: 여러 작은 인터페이스로 분할
- 파일 관리용, 편집용, 인쇄용 인터페이스로 분리
- 분리된 추상화를 나누어 코드 이해 단순화

**ISP 준수 예시 1: Shape 인터페이스** (Lines 647-658):

```java
// ISP 준수: 단일 초점의 작은 인터페이스
interface Shape {
    void draw(Graphics g);  // 메서드 하나만 - 매우 좁은 초점
}
// 장점:
// - 단일 초점 명확
// - 혼란을 주는 다른 개념 없음
// - 불필요한 메서드 없음
// - 하나의 메서드만으로 필요충분
```

**Python 버전**:
```python
# ISP 준수: 단일 초점의 작은 인터페이스
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def draw(self, graphics):  # 메서드 하나만 - 매우 좁은 초점
        pass
# 장점:
# - 단일 초점 명확
# - 혼란을 주는 다른 개념 없음
# - 불필요한 메서드 없음
# - 하나의 메서드만으로 필요충분
```

**ISP 준수 예시 2: Graphics 인터페이스** (Lines 659-668):

```java
// ISP 준수: 그래픽 기본 기능만 포함
public interface Graphics {
    void drawText(String text);           // 텍스트 문자열 표시
    void drawHorizontalLine(int width);   // 수평 방향 선 그리기
}
// 장점:
// - 그래픽 기본 기능 그리기만 관련된 메서드만 포함
// - 두 메서드가 강하게 관련됨 - 높은 응집도(high cohesion)
// - 메서드 수가 적음 - ISP 만족
// - 목적에 맞춘 효과적인 추상화
```

**Python 버전**:
```python
# ISP 준수: 그래픽 기본 기능만 포함
from abc import ABC, abstractmethod

class Graphics(ABC):
    @abstractmethod
    def draw_text(self, text):          # 텍스트 문자열 표시
        pass

    @abstractmethod
    def draw_horizontal_line(self, width):  # 수평 방향 선 그리기
        pass
# 장점:
# - 그래픽 기본 기능 그리기만 관련된 메서드만 포함
# - 두 메서드가 강하게 관련됨 - 높은 응집도(high cohesion)
# - 메서드 수가 적음 - ISP 만족
# - 목적에 맞춘 효과적인 추상화
```

**Graphics 인터페이스 구현: ConsoleGraphics** (Lines 669-687):

```java
// Graphics 인터페이스의 콘솔 구현
public class ConsoleGraphics implements Graphics {
    @Override
    public void drawText(String text) {
        print(text);
    }

    @Override
    public void drawHorizontalLine(int width) {
        var rowText = new StringBuilder();
        for (int i = 0; i < width; i++) {
            rowText.append('X');  // 'X' 문자로 선 그리기
        }
        print(rowText.toString());
    }

    private void print(String text) {
        System.out.println(text);  // 콘솔에 출력
    }
}
// 장점: LSP도 준수 - Graphics 인터페이스가 예상되는 곳 어디서나 사용 가능
```

**Python 버전**:
```python
# Graphics 인터페이스의 콘솔 구현
class ConsoleGraphics(Graphics):
    def draw_text(self, text):
        self._print(text)

    def draw_horizontal_line(self, width):
        row_text = 'X' * width  # 'X' 문자로 선 그리기
        self._print(row_text)

    def _print(self, text):
        print(text)  # 콘솔에 출력
# 장점: LSP도 준수 - Graphics 인터페이스가 예상되는 곳 어디서나 사용 가능
```

(출처: Lines 629-695)

### 7. SOLID 원칙의 통합 적용

**이전 내용과의 관계**: 개별 원칙들을 배웠으므로, 이제 이들이 어떻게 함께 작동하는지 이해한다.

5가지 SOLID 원칙이 모두 shapes 코드에 적용되어 컴팩트하고 잘 설계된 구조를 만들었다 (Lines 696-709).

**SOLID 원칙의 상호작용**:

1. **SRP의 기초적 역할**:
   - 설계를 이해하는 데 도움
   - 미래 변경 시 재작업 제한

2. **DIP의 분할 효과**:
   - 코드를 독립적인 작은 조각으로 분할
   - 각 조각이 전체 프로그램의 세부사항 일부를 숨김
   - 분할 정복(divide-and-conquer) 효과

3. **LSP의 안전성**:
   - 안전하고 쉽게 교체 가능한 객체 생성

4. **OCP의 확장성**:
   - 기능 추가가 간단한 소프트웨어 설계

5. **ISP의 명확성**:
   - 인터페이스를 작고 이해하기 쉽게 유지

**최종 설계의 장점** (Lines 700-707):
- 컴팩트한 코드
- 잘 설계된 구조
- 미래 유지보수자를 돕는 엔지니어링 구조
- 유사한 이점을 얻기 위해 자신의 코드에 적용 가능

(출처: Lines 700-709)

### 8. 테스트에 SOLID 원칙 적용

**이전 내용과의 관계**: SOLID 원칙은 프로덕션 코드뿐만 아니라 테스트 코드에도 적용된다.

SOLID 원칙은 테스트 코드 설계에도 동일하게 적용되어 더 나은 테스트를 작성할 수 있게 한다 (Lines 275-286, 721-724).

**테스트에 SRP 적용** (Lines 275-286):
- 각 테스트는 한 가지만 테스트
- 하나의 행복 경로 또는 하나의 경계 조건
- 결함 위치 파악 용이
- 테스트당 하나의 assertion 권장
- 다른 설정이 필요한 테스트는 별도로 작성

**테스트에 DIP 적용** (Lines 723-724):
- 테스트가 코드에 접근할 수 있는 테스트 접근 포인트 제공
- SRP와 DIP를 사용하면 테스트 작성이 훨씬 쉬워짐

**설정 분리 예시**:
```java
// SRP 적용: 설정별로 테스트 분리
@Test
public void testConfigA() {
    // Configuration A 설정
    var objectA = new ObjectA(configA);
    // Configuration A 테스트
}

@Test
public void testConfigB() {
    // Configuration B 설정
    var objectB = new ObjectB(configB);
    // Configuration B 테스트
}
// 장점: 각 테스트가 하나의 설정만 다룸 - 이해하기 쉬움
```

**Python 버전**:
```python
# SRP 적용: 설정별로 테스트 분리
def test_config_a():
    # Configuration A 설정
    object_a = ObjectA(config_a)
    # Configuration A 테스트
    pass

def test_config_b():
    # Configuration B 설정
    object_b = ObjectB(config_b)
    # Configuration B 테스트
    pass
# 장점: 각 테스트가 하나의 설정만 다룸 - 이해하기 쉬움
```

(출처: Lines 275-286, 721-724)

### 9. SOLID 원칙과 TDD의 관계

**이전 내용과의 관계**: 이 장 전체가 TDD와 SOLID 원칙의 관계를 다루었으며, 여기서 핵심 질문들을 정리한다.

SOLID 원칙은 TDD와 독립적이지만, 함께 사용하면 시너지 효과가 크다 (Lines 710-756).

**핵심 질문과 답변** (Lines 710-756):

**Q1: SOLID 원칙은 OO 코드에만 적용되는가?** (Lines 712-719)
- 아니오. 원래 OO 맥락에서 시작했지만 더 일반적
- 함수형 프로그래밍과 마이크로서비스 설계에도 적용 가능
- SRP: 거의 보편적으로 유용 - 문서 단락에도 적용
- SRP: 순수 함수와 테스트 작성에도 도움
- DIP와 OCP: Java 람다처럼 순수 함수를 전달하여 함수형 맥락에서 구현
- SOLID 전체: 모든 종류의 소프트웨어 컴포넌트에서 결합도와 응집도 관리 목표 제공

**Q2: TDD와 함께 SOLID 원칙을 반드시 사용해야 하는가?** (Lines 721-724)
- 아니오. TDD는 소프트웨어 컴포넌트의 결과와 공개 인터페이스 정의
- 컴포넌트 구현 방법은 TDD 테스트와 무관
- 하지만 SRP와 DIP 같은 원칙은 테스트 접근 포인트를 제공하여 테스트 작성을 훨씬 쉽게 만듦

**Q3: SOLID 원칙만 사용해야 하는가?** (Lines 730-737)
- 아니오. 모든 가용한 기술 사용해야 함
- SOLID는 훌륭한 시작점이지만 다른 유효한 기술도 많음:
  - 디자인 패턴 전체 카탈로그
  - Craig Larman의 GRASP(General Responsibility Assignment Software Patterns)
  - David L. Parnas의 정보 은닉(information hiding)
  - 결합도(coupling)와 응집도(cohesion) 개념
- 목표: 읽기 쉽고 변경하기 안전한 소프트웨어

**Q4: SOLID 원칙 없이도 TDD를 할 수 있는가?** (Lines 739-742)
- 예. 매우 가능함
- TDD는 코드의 동작 테스트에 관심, 구현 세부사항은 아님
- SOLID 원칙은 단순히 견고하고 테스트하기 쉬운 OO 설계를 만드는 데 도움

**Q5: SRP와 ISP는 어떤 관계인가?** (Lines 744-748)
- ISP: 하나의 큰 인터페이스보다 여러 짧은 인터페이스 선호
- 각 짧은 인터페이스는 클래스가 제공해야 하는 단일 측면과 관련
- 보통 역할이나 하위 시스템
- ISP는 인터페이스가 SRP를 적용하도록 만드는 것 - 한 가지만 잘 수행

**Q6: OCP는 DIP, LSP와 어떤 관계인가?** (Lines 750-756)
- OCP: 컴포넌트 자체를 변경하지 않고 새 기능 추가 가능한 컴포넌트 생성 안내
- 플러그인 설계로 달성
- 방법:
  1. 플러그인이 해야 할 일의 추상화를 인터페이스로 생성 (DIP)
  2. LSP를 준수하는 구체적인 플러그인 구현 생성
  3. 컴포넌트에 새 플러그인 주입
- OCP는 DIP와 LSP에 의존하여 작동

(출처: Lines 710-756)

---

## 요약 (Lines 700-709)

이 장에서는 SOLID 원칙이 프로덕션 코드와 테스트 설계에 어떻게 도움이 되는지 간단한 설명과 함께 살펴보았다. 5가지 SOLID 원칙을 모두 사용하는 예제 설계를 작업했다. 미래 작업에서 SRP를 적용하여 설계를 이해하고 미래 변경 시 재작업을 제한할 수 있다. DIP를 적용하여 코드를 독립적인 작은 조각으로 분할하고, 각 조각이 전체 프로그램의 세부사항 일부를 숨기도록 하여 분할 정복 효과를 만들 수 있다. LSP를 사용하여 안전하고 쉽게 교체 가능한 객체를 만들 수 있다. OCP는 기능 추가가 간단한 소프트웨어 설계를 돕는다. ISP는 인터페이스를 작고 이해하기 쉽게 유지한다.

다음 장에서는 이러한 원칙들을 사용하여 테스트의 한 가지 문제를 해결한다 - 객체 간 협력을 어떻게 테스트하는가?
