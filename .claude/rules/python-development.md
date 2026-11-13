---
paths:
  - "**/*.py"
---
- Use Python type annotations.
- Follow Ruff and Mypy conventions. You can challenge yourself with them by running mypy or ruff tools.
- Prefer descriptive, domain-specific type aliases.
- Use Pydantic for runtime validation at system boundaries.
- Prefer composition over unnecessary inheritance.
- Follow existing exception-handling conventions.
- Separate abstraction layers: there should be controller layer(business logic function), lower level functions, and atomic functions - each function should do only ONE thing. Avoid side effects.
- Recognize similar concepts to avoid code duplication.
- Single file should refer to single concept
- Code should be self-explanatory. Prefer typing tools, like aliases, Literals, and objects like dataclasses, NamedTuples, or Pyydantic objects instead using complex docstrings:
Example:
//Bad
```python
def build_house(s, n):
    """Return a house object with s square metre and n rooms.
    """
    if n > 10:
        msg = "House may has 10 rooms max."
        raise ValueError(msg)
    return House(s, n)
```
//Good
```python
from pydantic import NonNegativeInt
type SquareMeters = NonNegativeInt
type RoomsNumber = Annotated[int, Field(gt=0, le=10)]

adapter_rooms_number = TypeAdapter(RoomsNumber)


def build_house(size: SquareMeters, rooms: RoomsNumber) -> House:
    adapter_rooms_number.validate_python(rooms)
    return House(
        size=size,
        rooms=rooms,
    )
```
- Use comments mostly for explanation of business logic, or to explain logic which cannot be simply explained by code (example: why such solution was chosen). In such case those comments should be in docstrings of functions or better in docstring of a file.
- do not mix levels of abstraction in one function
Example:
//Bad
```python
def get_payments(db_name: str) -> DataFrame:
  # Conecting to database is resolved in the same function which run transformations of results. This is mixing levels of abstraction, and makes code less readable and testable.
    connection = DatabaseConnection(db_name)
    connection.connect()
    raw_payments = query_for_payments(connection)
    return transform_payments(raw_payments)
```

//Good
```python
def get_payments(db_name: str) -> DataFrame:
    raw_payments = select_payments(db_name)
    return transform_payments(raw_payments)

def select_payments(source: str) -> list[RawPayment]:
  with DatabaseConnection(source) as connection:
      return query_for_payments(connection)
```
