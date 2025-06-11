from utils import StrictModel


class Review(StrictModel):
    id: int
    text: str

    def to_dict(self) -> dict[str, int | str]:
        return self.model_dump()
