from pauperformance_bot.client.pauperformance import Pauperformance


def update():
    pauperformance = Pauperformance()
    pauperformance.update_set_index()
    pauperformance.update_archetypes()


if __name__ == '__main__':
    update()
