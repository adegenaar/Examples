from pydantic import BaseModel


class Item(BaseModel):
    """Pydantic dataclass"""

    name: str = None
    price: float = None
    is_offer: bool = None


def main():
    data = {"name": "fred", "price": "10"}
    obj = Item.parse_obj(data)
    print(obj)


if __name__ == "__main__":
    main()
