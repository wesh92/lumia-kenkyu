import requests
import tomli
from abc import ABC, abstractmethod
from typing import Type, List, Dict, Any
from models.er_api_metadata_model import (
    Armor,
    Area,
    BaseModel,
    Character,
    Collectible,
    Consumables,
    DropGroup,
    Monster,
    MiscItem,
    MonsterDropGroup,
    SpawnItem,
    SpecialItem,
    Weapon,
    WeaponType,
)

BASE_URL = "https://open-api.bser.io"

API_KEY = tomli.load(open("./models/.secrets.toml", "rb"))["er"]["api_key"]


class ModelBuilder(ABC):
    @abstractmethod
    def fetch_data(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def process_data(self, data: List[Dict[str, Any]]) -> list[BaseModel]:
        pass

    def build(self) -> list[BaseModel]:
        raw_data = self.fetch_data()
        return self.process_data(raw_data)


class ERApiModelBuilder(ModelBuilder):
    def __init__(self, model_class: BaseModel, endpoint: str):
        self.model_class = model_class
        self.endpoint = endpoint

    def fetch_data(self) -> list[dict[str, Any]]:
        headers = {"accept": "application/json", "x-api-key": API_KEY}
        response = requests.get(f"{BASE_URL}{self.endpoint}", headers=headers)
        response.raise_for_status()
        return response.json().get("data", [])

    def process_data(self, data: list[dict[str, Any]]) -> list[BaseModel]:
        return [self.model_class(**item) for item in data]


class ERApiDirector:
    def __init__(self):
        self.builders: Dict[str, ERApiModelBuilder] = {
            "armor": ERApiModelBuilder(Armor, "/v2/data/ItemArmor"),
            "area": ERApiModelBuilder(Area, "/v2/data/Area"),
            "character": ERApiModelBuilder(Character, "/v2/data/Character"),
            "collectible": ERApiModelBuilder(Collectible, "/v2/data/Collectible"),
            "consumables": ERApiModelBuilder(Consumables, "/v2/data/ItemConsumable"),
            "drop_group": ERApiModelBuilder(DropGroup, "/v2/data/DropGroup"),
            "monster": ERApiModelBuilder(Monster, "/v2/data/Monster"),
            "misc_item": ERApiModelBuilder(MiscItem, "/v2/data/ItemMisc"),
            "monster_drop_group": ERApiModelBuilder(
                MonsterDropGroup, "/v2/data/MonsterDropGroup"
            ),
            "spawn_item": ERApiModelBuilder(SpawnItem, "/v2/data/ItemSpawn"),
            "special_item": ERApiModelBuilder(SpecialItem, "/v2/data/ItemSpecial"),
            "weapon": ERApiModelBuilder(Weapon, "/v2/data/ItemWeapon"),
            "weapon_type": ERApiModelBuilder(WeaponType, "/v2/data/WeaponTypeInfo"),
        }

    def build_all(self) -> dict[str, list[BaseModel]]:
        return {name: builder.build() for name, builder in self.builders.items()}
    def build_specific(self, model_names: List[str]) -> dict[str, list[BaseModel]]:
        return {name: self.builders[name].build() for name in model_names}

