# Coding Standards & Agent Behavior Guidelines

## 1. Language Consistency
- Detect the user's input language and respond only in the same language.
- If the user uses Chinese, respond entirely in Chinese; if English, respond entirely in English; maintain consistency for other languages.
- Do not mix languages unless the user's input itself contains multiple languages.
- Language consistency takes priority over all other considerations.

## 2. Behavior Patterns Description

### 2.1 Overview
Behavior patterns refer to observable actions and responses in software systems. They reflect how modules, components, or systems behave when receiving input or undergoing state changes, commonly used to analyze interaction logic, predict outcomes, and verify implementation correctness.

### 2.2 Common Behavioral Scenarios & Examples

#### Event Handling
**Definition**: A series of actions taken by the system in response to externally or internally triggered events.  
**Examples**:
- Clicking a button in a GUI application triggers a data refresh.
- A web service receives an HTTP request, executes corresponding business logic, and returns a response.
- In a Streamlit app, selecting a file automatically runs analysis.

**Modeling Approaches**:
- Use event-driven architecture (Observer/Pub-Sub).
- Implement via callbacks, listeners, or middleware in code.

**Testing**:
- Simulate event triggering and check output state or returned data.
- Use unit testing frameworks (e.g., pytest) with mock objects.

**Documentation**:
```python
# Example: Button click event handler
import streamlit as st

def on_button_click():
    st.success("Button clicked, starting analysis...")

st.button("Start Analysis", on_click=on_button_click)
```

#### State Transitions
**Definition**: The process of moving between different states in a system, usually triggered by conditions.  
**Examples**:
- Order status: "Pending Payment" → "Paid" → "Shipped".
- Application interface: "Loading" → "Ready" → "Error".

**Modeling Approaches**:
- Finite State Machine (FSM) or State Pattern.
- Represent states and legal transitions using enums or class hierarchies.

**Testing**:
- Verify allowed events and next states for each state.
- Boundary testing: illegal transitions should be rejected or raise errors.

**Documentation**:
```python
# Example: Simple state machine
class OrderState:
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"

def transition(state, event):
    if state == OrderState.PENDING and event == "pay":
        return OrderState.PAID
    elif state == OrderState.PAID and event == "ship":
        return OrderState.SHIPPED
    else:
        raise ValueError("Invalid state transition")
```

#### User Interaction Flows
**Definition**: Interaction paths formed by a sequence of user actions and system feedback.  
**Examples**:
- User fills out a form → submits → system validates → displays success or error message.
- In a data analysis app: upload dataset → select analysis options → view report.

**Modeling Approaches**:
- Use case diagrams, flowcharts, or sequence diagrams to describe steps.
- Front-end switches views driven by state; back-end provides corresponding APIs.

**Testing**:
- End-to-end (E2E) tests simulate complete user operation flows.
- Verify outputs at each step match expectations.

**Documentation**:
```markdown
1. User opens the page
2. Uploads a CSV file
3. System parses and displays field preview
4. User clicks “Generate Report”
5. System runs ydata-profiling and shows results
```

### 2.3 Modeling, Testing & Documenting Behaviors

**Modeling**:
- Use UML state diagrams and activity diagrams to represent behavior-state relationships.
- Define states and events in code using classes, enums, or DSLs.

**Testing**:
- Unit tests validate individual behavior units.
- Integration tests validate behavior chains across modules.
- Property tests ensure state machines cover all legal paths.

**Documenting**:
- Describe trigger conditions, expected responses, and exception handling in code comments or standalone documents.
- Provide executable example code for reproducibility and verification.
- Use Behavior-Driven Development (BDD) format (Given-When-Then) for test case descriptions.

### 2.4 Summary
Identifying and standardizing behavior patterns in software systems helps:
- Clarify module responsibilities and interaction boundaries
- Improve testability and maintainability
- Enable new team members to quickly understand system operation

Include behavior description templates in project coding standards and verify completeness and executability during review processes.