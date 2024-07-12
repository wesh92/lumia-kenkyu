from pydantic import BaseModel, ConfigDict, Field, RootModel
from datetime import datetime
from typing import Optional


class KillData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    killed_by_id: int = Field(..., alias="killerUserNum")
    killed_by_type: str = Field(..., alias="killer")
    killed_by_name: str = Field(..., alias="killDetail")
    died_area: str = Field(..., alias="placeOfDeath")
    killed_by_character: str = Field(..., alias="killerCharacter")
    killed_by_character_weapon: str = Field(..., alias="killerWeapon")


class KillDataList(RootModel):
    root: list[KillData]


class UserGame(BaseModel):
    user_id: int = Field(..., alias="userNum")
    nickname: str = Field(..., alias="nickname")
    game_id: int = Field(..., alias="gameId")
    season_id: int = Field(..., alias="seasonId")
    match_mode: int = Field(..., alias="matchingMode")
    match_team_mode: int = Field(..., alias="matchingTeamMode")
    character_id: int = Field(..., alias="characterNum")
    level: int = Field(..., alias="characterLevel")
    game_place_result: int = Field(..., alias="gameRank")
    kills: int = Field(..., alias="playerKill")
    assists: int = Field(..., alias="playerAssistant")
    monster_kills: int = Field(..., alias="monsterKill")
    final_mastery_levels: dict[str, int] = Field(..., alias="masteryLevel")
    final_equipment: dict[str, int] = Field(..., alias="equipment")
    skill_order: dict[str, int] = Field(..., alias="skillOrderInfo")
    server: str = Field(..., alias="serverName")
    game_start_datetime: datetime = Field(..., alias="startDtm")
    duration: int = Field(..., alias="duration")
    mmr_change: Optional[int] = Field(alias="mmrGainInGame")
    mmr_before: Optional[int] = Field(None, alias='mmrBefore')
    mmr_gain: Optional[int] = Field(None, alias='mmrGain')
    mmr_after: Optional[int] = Field(None, alias='mmrAfter')
    total_player_played_time: int = Field(..., alias="playTime")
    bots_added: int = Field(..., alias="botAdded")
    team_id: int = Field(
        ..., alias="teamNumber"
    )  # Needed to group players in the same team later.
    pre_made: int = Field(..., alias="preMade")
    victory: bool = Field(..., alias="victory")
    damage_to_player: int = Field(..., alias="damageToPlayer")
    damage_to_player_basic: int = Field(..., alias="damageToPlayer_basic")
    damage_to_player_skill: int = Field(..., alias="damageToPlayer_skill")
    damage_to_player_item: int = Field(..., alias="damageToPlayer_itemSkill")
    damage_to_player_true: int = Field(..., alias="damageToPlayer_direct")
    damage_to_player_unique: int = Field(..., alias="damageToPlayer_uniqueSkill")
    tanked_damage: int = Field(..., alias="damageFromPlayer")
    tanked_damage_basic: int = Field(..., alias="damageFromPlayer_basic")
    tanked_damage_skill: int = Field(..., alias="damageFromPlayer_skill")
    tanked_damage_item: int = Field(..., alias="damageFromPlayer_itemSkill")
    tanked_damage_true: int = Field(..., alias="damageFromPlayer_direct")
    tanked_damage_unique: int = Field(..., alias="damageFromPlayer_uniqueSkill")
    damage_to_monster: int = Field(..., alias="damageToMonster")
    damage_to_monster_basic: int = Field(..., alias="damageToMonster_basic")
    damage_to_monster_skill: int = Field(..., alias="damageToMonster_skill")
    damage_to_monster_item: int = Field(..., alias="damageToMonster_itemSkill")
    damage_to_monster_true: int = Field(..., alias="damageToMonster_direct")
    damage_to_monster_unique: int = Field(..., alias="damageToMonster_uniqueSkill")
    damage_from_monster: int = Field(..., alias="damageFromMonster")
    healing: int = Field(..., alias="healAmount")
    starting_area: int = Field(..., alias="placeOfStart")  # Is an int, convert later...
    total_match_players: int = Field(..., alias="matchSize")
    team_kills: int = Field(..., alias="teamKill")
    killed_by_data: KillDataList = Field(..., alias="killerList")
    posessed_credits: int = Field(..., alias="sumTotalVFCredits")
    used_credits: int = Field(..., alias="sumUsedVFCredits")
    deaths: int = Field(..., alias="playerDeaths")
    early_kills: int = Field(..., alias="killsPhaseOne")
    midgame_kills: int = Field(..., alias="killsPhaseTwo")
    lategame_kills: int = Field(..., alias="killsPhaseThree")
    early_deaths: int = Field(..., alias="deathsPhaseOne")
    midgame_deaths: int = Field(..., alias="deathsPhaseTwo")
    lategame_deaths: int = Field(..., alias="deathsPhaseThree")
    items_purchased_from_console: list[int] = Field(..., alias="itemTransferredConsole")
    items_purchased_from_drone: list[int] = Field(..., alias="itemTransferredDrone")
    double_kills: int = Field(..., alias="totalDoubleKill")
    triple_kills: int = Field(..., alias="totalTripleKill")
    quadra_kills: int = Field(..., alias="totalQuadraKill")
    extra_kills: int = Field(..., alias="totalExtraKill")
    equipment_first_item: dict[str, list[int]] = Field(..., alias="equipFirstItemForLog")
    main_weather: Optional[int] = Field(None, alias="mainWeather")
    sub_weather: Optional[int] = Field(None, alias="subWeather")
