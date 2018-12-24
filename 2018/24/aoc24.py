#!/usr/bin/env python3


# this class is not needed, dont feel like refactoring
class Unit:
    def __init__(self, hp, immunes, weaknesses, attack, damage, initiative):
        self.hp = hp
        self.immunes = immunes
        self.weaknesses = weaknesses
        self.attack = attack
        self.damage = damage
        self.initiative = initiative

    def __repr__(self):
        return str(self.hp)


class Group:
    def __init__(self, units, nbr_units, unit_hp, attack, immunes, weaknesses, initiative):
        self.units = units
        self.nbr_units = nbr_units
        self.unit_hp = unit_hp
        self.attack = attack
        self.immunes = immunes
        self.weaknesses = weaknesses
        self.initiative = initiative

        self.selected_target = None
        self.selected = False

    def __repr__(self):
        return str(self.nbr_units)

    def hp(self):
        return self.unit_hp * self.nbr_units

    def effective_power(self):
        return self.nbr_units * self.units[0].damage

    def select_target(self, groups):
        if self.hp() == 0:
            return None

        best_damage = -1
        selected_group = None
        for group in groups:
            if group.hp() == 0 or group.selected:
                continue

            total_damage = self.effective_power()
            if self.attack in group.immunes:
                total_damage = 0
            elif self.attack in group.weaknesses:
                total_damage *= 2

            if total_damage > best_damage:
                selected_group = group
                best_damage = total_damage
            elif total_damage == best_damage:
                if selected_group:
                    if group.effective_power() > selected_group.effective_power():
                        selected_group = group
                    elif group.effective_power() == selected_group.effective_power() and group.initiative > selected_group.initiative:
                        selected_group = group
                else:
                    selected_group = group

                best_damage = total_damage

        self.selected_target = selected_group if best_damage > 0 else None
        if self.selected_target:
            self.selected_target.selected = True

    def attack_target(self):
        if not self.selected_target:
            return

        damage = self.effective_power()
        if self.attack in self.selected_target.immunes:
            damage = 0
        elif self.attack in self.selected_target.weaknesses:
            damage *= 2

        nbr_killed = int(damage / self.selected_target.unit_hp)
        self.selected_target.decrease_units(nbr_killed)

    def decrease_units(self, nbr_killed):
        self.nbr_units -= nbr_killed
        if self.nbr_units < 0:
            self.nbr_units = 0


# a bit of trial and error, it ended up in infinite loops on 41 and 42 due to ties - and 43 was the first round they won
for boost in range(0, 1): # part 1
# for boost in range(43, 10000): # part 2
    immunes = {}
    infections = {}
    groups = []
    with open('input.txt') as fp:
        curr_dict = None
        for line in fp:
            line = line.strip()

            if 'Immune System:' in line:
                curr_dict = immunes
                continue

            if 'Infection:' in line:
                curr_dict = infections
                continue

            if line == '':
                continue

            nbr_units = int(line.split(' ')[0])
            units = []
            for _ in range(nbr_units):
                hp = int(line.split(' ')[4])

                immunities = []
                weaknesses = []
                try:
                    abilities_start = line.index('(')
                    abilities_end = line.index(')')

                    abilities = line[abilities_start + 1:abilities_end].split(';')
                    for ability in abilities:
                        ability = ability.strip()
                        if ability.startswith('weak'):
                            ability = ability.replace('weak to ', '')
                            weaknesses += ability.split(', ')
                        elif ability.startswith('immune'):
                            ability = ability.replace('immune to ', '')
                            immunities += ability.split(', ')
                        else:
                            raise Exception('err')
                except ValueError:
                    pass

                attack = line.split(' ')[-5]
                damage = int(line.split(' ')[-6])
                initiative = int(line.split(' ')[-1])

                if curr_dict is immunes:
                    damage += boost

                unit = Unit(hp, immunities, weaknesses, attack, damage, initiative)

                units.append(unit)

            group = Group(units, nbr_units, hp, attack, immunities, weaknesses, initiative)
            curr_dict[initiative] = group
            groups.append(group)


    done = False
    while not done:

        all_dead = True
        for group in immunes.values():
            if group.hp() != 0:
                all_dead = False

        if all_dead:
            done = True
            break

        all_dead = True
        for group in infections.values():
            if group.hp() != 0:
                all_dead = False

        if all_dead:
            done = True
            break

        for group in groups:
            group.selected = False

        groups = sorted(groups, key=lambda group: (-group.effective_power(), -group.initiative))
        for group in groups:
            if group.initiative in immunes.keys():
                group.select_target(infections.values())
            else:
                group.select_target(immunes.values())

        groups = sorted(groups, key=lambda group: -group.initiative)

        for group in groups:
            if group.nbr_units > 0:
                group.attack_target()

    sum = 0
    for group in infections.values():
        sum += group.nbr_units

    if sum == 0:
        immune_sum = 0
        for group in immunes.values():
            immune_sum += group.nbr_units
        print()
        print(immune_sum)
        exit(0)

    print(str(boost) + ' ' + str(sum))
