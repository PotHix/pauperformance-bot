from pauperformance_bot.constant.discord import (
    DISCORD_USER_MREVILEYE_ID,
    DISCORD_USER_SHIKA93_ID,
)
from pauperformance_bot.credentials import (
    TELEGRAM_MREVILEYE_ID,
    TELEGRAM_PAUPERFORMANCE_ID,
    TELEGRAM_SHIKA93_ID,
)
from pauperformance_bot.entity.phd import PhD

PAUPERFORMANCE = PhD(
    name="Pauperformance",
    mtgo_name="Pauperformance",
    deckstats_name="Pauperformance",
    deckstats_id="181430",
    telegram_id=TELEGRAM_PAUPERFORMANCE_ID,
    twitch_login_name="Pauperformance",
    youtube_channel_id="UCDUiIskNnmuJ3XJ1SdQqs0A",
    default_youtube_language="en",
    discord_id=None,
)

SHIKA93 = PhD(
    name="Shika93",
    mtgo_name="Shika93",
    deckstats_name="Shika93",
    deckstats_id="78813",
    telegram_id=TELEGRAM_SHIKA93_ID,
    twitch_login_name=None,
    youtube_channel_id=None,
    default_youtube_language="en",
    discord_id=DISCORD_USER_SHIKA93_ID,
)

MREVILEYE = PhD(
    name="MrEvilEye",
    mtgo_name="MrEvilEye",
    deckstats_name="MrEvilEye",
    deckstats_id="72056",
    telegram_id=TELEGRAM_MREVILEYE_ID,
    twitch_login_name=None,
    youtube_channel_id=None,
    default_youtube_language="en",
    discord_id=DISCORD_USER_MREVILEYE_ID,
)

PAUPERGANDA = PhD(
    name="PAUPERGANDA",
    mtgo_name="deluxeicoff",
    deckstats_name=None,
    deckstats_id=None,
    telegram_id=None,
    twitch_login_name="pauperganda",
    youtube_channel_id="UCqJ0E420KX9_3lFNJjDoKDA",
    default_youtube_language="en",
    discord_id=None,
)

TARMOGOYF_ITA = PhD(
    name="tarmogoyf_ita",
    mtgo_name="tarmogoyf_ita",
    deckstats_name="tarmogoyf_ita",
    deckstats_id="161568",
    telegram_id=None,
    twitch_login_name="lega_pauper_online",
    youtube_channel_id="UCAERb1O0w07LQ2ORO-N6V_Q",
    default_youtube_language="it",
    discord_id=None,
)

PAUPERFORMANCE_PHDS = [
    PAUPERFORMANCE,
    SHIKA93,
    MREVILEYE,
    PAUPERGANDA,
    TARMOGOYF_ITA,
]
