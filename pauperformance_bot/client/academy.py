import glob
from pathlib import Path

from pauperformance_bot.client.deckstats import Deckstats
from pauperformance_bot.client.pauperformance import get_pauperformance_archetypes
from pauperformance_bot.constants import \
    SET_INDEX_TEMPLATE_FILE, SET_INDEX_OUTPUT_FILE, TEMPLATES_PAGES_DIR, \
    CONFIG_ARCHETYPES_DIR, TEMPLATES_ARCHETYPES_DIR, \
    PAUPERFORMANCE_ARCHETYPES_DIR, ARCHETYPE_TEMPLATE_FILE, \
    PAUPER_POOL_TEMPLATE_FILE, \
    PAUPER_POOL_OUTPUT_FILE, SET_INDEX_PAGE_NAME, \
    ARCHETYPES_INDEX_TEMPLATE_FILE, \
    ARCHETYPES_INDEX_OUTPUT_FILE, PAUPERFORMANCE_ARCHETYPES_DIR_RELATIVE_URL, \
    PAUPER_POOL_PAGE_NAME
from pauperformance_bot.util.config import read_archetype_config
from pauperformance_bot.util.log import get_application_logger
from pauperformance_bot.util.path import posix_path
from pauperformance_bot.util.template import render_template
from pauperformance_bot.util.time import pretty_str, now

logger = get_application_logger()


class Academy:
    def __init__(self, pauperformance):
        self.pauperformance = pauperformance
        self.scryfall = pauperformance.scryfall
        self.set_index = pauperformance.set_index

    def update_all(self):
        self.update_archetypes_index()
        self.update_set_index()
        self.update_pauper_pool()
        self.update_archetypes()

    def update_archetypes_index(
            self,
            config_pages_dir=CONFIG_ARCHETYPES_DIR,
            templates_pages_dir=TEMPLATES_PAGES_DIR,
            archetypes_dir=PAUPERFORMANCE_ARCHETYPES_DIR_RELATIVE_URL,
            archetypes_index_template_file=ARCHETYPES_INDEX_TEMPLATE_FILE,
            archetypes_index_output_file=ARCHETYPES_INDEX_OUTPUT_FILE,
    ):
        logger.info(
            f"Rendering archetype index in {templates_pages_dir} from "
            f"{archetypes_index_template_file}..."
        )
        archetypes = []
        for archetype_config_file in glob.glob(f"{config_pages_dir}/*.ini"):
            logger.info(f"Processing {archetype_config_file}")
            values = read_archetype_config(archetype_config_file)
            archetypes.append({
                "name": values["name"],
                "mana": values["mana"],
                "type": ', '.join(values["type"]),
            })
        archetypes.sort(key=lambda a: a['name'])
        render_template(
            templates_pages_dir,
            archetypes_index_template_file,
            archetypes_index_output_file,
            {
                "archetypes": archetypes,
                "last_update_date": pretty_str(now()),
                "archetypes_dir": archetypes_dir,
            }
        )
        logger.info(
            f"Rendered archetypes index to {archetypes_index_output_file}."
        )

    def update_set_index(
            self,
            templates_pages_dir=TEMPLATES_PAGES_DIR,
            set_index_template_file=SET_INDEX_TEMPLATE_FILE,
            set_index_output_file=SET_INDEX_OUTPUT_FILE,
    ):
        logger.info(
            f"Rendering set index in {templates_pages_dir} from {set_index_template_file}..."
        )
        bolded_set_index = self._boldify_sets_with_new_cards()
        render_template(
            templates_pages_dir,
            set_index_template_file,
            set_index_output_file,
            {
                "index": bolded_set_index,
                "last_update_date": pretty_str(now()),
                "pauper_pool_page": PAUPER_POOL_PAGE_NAME.as_html(),
            }
        )
        logger.info(f"Rendered set index to {set_index_output_file}.")

    def update_archetypes(
            self,
            config_pages_dir=CONFIG_ARCHETYPES_DIR,
            templates_archetypes_dir=TEMPLATES_ARCHETYPES_DIR,
            archetype_template_file=ARCHETYPE_TEMPLATE_FILE,
            pauperformance_archetypes_dir=PAUPERFORMANCE_ARCHETYPES_DIR,
    ):
        logger.info(f"Generating archetypes...")
        all_decks = self.pauperformance.get_pauperformance_decks()
        for archetype_config_file in glob.glob(f"{config_pages_dir}/*.ini"):
            logger.info(f"Processing {archetype_config_file}")
            values = read_archetype_config(archetype_config_file)
            archetype_name = values['name']
            archetype_decks = [
                deck
                for deck in all_decks
                if deck.archetype == archetype_name
            ]
            staples, frequents = self.pauperformance.analyze_cards_frequency(archetype_decks)
            if len(archetype_decks) < 2:
                logger.warn(
                    f"{archetype_name} doesn't have at least 2 decks to generate staples and frequent cards."
                )
            values['staples'] = self._get_rendered_card_info(staples)
            values['frequents'] = self._get_rendered_card_info(frequents)
            values['decks'] = archetype_decks
            archetype_file_name = Path(archetype_config_file).name
            if archetype_name != archetype_file_name.replace(".ini", ""):
                logger.warn(
                    f"Archetype config mismatch: {archetype_name} vs "
                    f"{archetype_file_name}"
                )

            archetype_output_file = posix_path(
                pauperformance_archetypes_dir,
                archetype_file_name.replace('.ini', '.md'),
            )
            logger.info(
                f"Rendering {archetype_name} in {templates_archetypes_dir} "
                f"from {archetype_template_file}..."
            )
            render_template(
                templates_archetypes_dir,
                archetype_template_file,
                archetype_output_file,
                values,
            )
        logger.info(f"Generated archetypes.")

    def update_pauper_pool(
            self,
            templates_pages_dir=TEMPLATES_PAGES_DIR,
            pauper_pool_template_file=PAUPER_POOL_TEMPLATE_FILE,
            pauper_pool_output_file=PAUPER_POOL_OUTPUT_FILE,
    ):
        logger.info(
            f"Rendering pauper pool in {templates_pages_dir} from "
            f"{pauper_pool_template_file}..."
        )
        card_index = self.pauperformance.get_pauper_cards_incremental_index()
        render_template(
            templates_pages_dir,
            pauper_pool_template_file,
            pauper_pool_output_file,
            {
                "tot_cards_number": sum(len(i) for i in card_index.values()),
                "set_index": list(self.set_index.values()),
                "card_index": card_index,
                "last_update_date": pretty_str(now()),
                "set_index_page": SET_INDEX_PAGE_NAME.as_html(),
            }
        )
        logger.info(f"Rendered pauper pool to {pauper_pool_template_file}.")

    def _get_rendered_card_info(self, cards):
        rendered_cards = []
        for card in sorted(cards):
            scryfall_card = self.scryfall.get_card_named(card)
            if "image_uris" not in scryfall_card:  # e.g. Delver of Secrets
                image_uris = scryfall_card["card_faces"][0]["image_uris"]
            else:
                image_uris = scryfall_card["image_uris"]
            rendered_cards.append({
                'name': card,
                "image_url": image_uris["normal"],
                "page_url": scryfall_card["scryfall_uri"].replace('?utm_source=api', ''),
            })
        return rendered_cards

    def _boldify_sets_with_new_cards(self):
        card_index = self.pauperformance.get_pauper_cards_incremental_index()
        bolded_index = []
        for item in self.set_index.values():
            p12e_code = item['p12e_code']
            if len(card_index[p12e_code]) == 0:
                bolded_index.append(item)
            else:
                bolded_index.append({
                    k: f"**{v}**"
                    for k, v in item.items()
                })
        return bolded_index