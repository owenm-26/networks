from enum import Enum
class FlorentineFamilies(Enum):
    PERUZZI="Peruzzi"
    BISCHERI="Bischeri"
    LAMBERTESCHI="Lambertesci"
    STROZZI="Strozzi"
    GUADAGNI="Guadagni"
    CASTELLANI="Castellani"
    RIDOLFI="Ridolfi"
    TORNABUONI="Tornabuoni"
    BARBADORI="Barbadori"
    MEDICI="Medici"
    ALBIZZI="Albizi"
    ACCIAIUOLI="Acciaiuoli"
    SALVIATI="Salviati"
    GINORI="Ginori"
    PUCCI="Pucci"
    PAZZI="Pazzi"

def create_florentine_adj_list():
    adj_list: FlorentineFamilies = {}
    adj_list[FlorentineFamilies.PERUZZI] = [
        FlorentineFamilies.BISCHERI,
        FlorentineFamilies.STROZZI,
        FlorentineFamilies.CASTELLANI
    ]

    adj_list[FlorentineFamilies.BISCHERI] = [
        FlorentineFamilies.PERUZZI,
        FlorentineFamilies.STROZZI,
        FlorentineFamilies.GUADAGNI
    ]

    adj_list[FlorentineFamilies.LAMBERTESCHI] = [
        FlorentineFamilies.GUADAGNI
    ]

    adj_list[FlorentineFamilies.STROZZI] = [
        FlorentineFamilies.PERUZZI,
        FlorentineFamilies.BISCHERI,
        FlorentineFamilies.CASTELLANI,
        FlorentineFamilies.RIDOLFI
    ]

    adj_list[FlorentineFamilies.GUADAGNI] = [
        FlorentineFamilies.BISCHERI,
        FlorentineFamilies.LAMBERTESCHI,
        FlorentineFamilies.TORNABUONI,
        FlorentineFamilies.ALBIZZI
    ]

    adj_list[FlorentineFamilies.CASTELLANI] = [
        FlorentineFamilies.PERUZZI,
        FlorentineFamilies.STROZZI,
        FlorentineFamilies.BARBADORI
    ]

    adj_list[FlorentineFamilies.RIDOLFI] = [
        FlorentineFamilies.STROZZI,
        FlorentineFamilies.TORNABUONI,
        FlorentineFamilies.MEDICI
    ]

    adj_list[FlorentineFamilies.TORNABUONI] = [
        FlorentineFamilies.MEDICI,
        FlorentineFamilies.GUADAGNI,
        FlorentineFamilies.RIDOLFI
    ]

    adj_list[FlorentineFamilies.BARBADORI] = [
        FlorentineFamilies.CASTELLANI,
        FlorentineFamilies.MEDICI
    ]

    adj_list[FlorentineFamilies.MEDICI] = [
        FlorentineFamilies.RIDOLFI,
        FlorentineFamilies.TORNABUONI,
        FlorentineFamilies.BARBADORI,
        FlorentineFamilies.ALBIZZI,
        FlorentineFamilies.ACCIAIUOLI,
        FlorentineFamilies.SALVIATI,
    ]

    adj_list[FlorentineFamilies.ALBIZZI] = [
        FlorentineFamilies.GUADAGNI,
        FlorentineFamilies.GINORI,
        FlorentineFamilies.MEDICI
    ]

    adj_list[FlorentineFamilies.ACCIAIUOLI] = [
        FlorentineFamilies.MEDICI
    ]

    adj_list[FlorentineFamilies.SALVIATI] = [
        FlorentineFamilies.MEDICI,
        FlorentineFamilies.PAZZI
    ]

    adj_list[FlorentineFamilies.GINORI] = [
        FlorentineFamilies.ALBIZZI
    ]

    adj_list[FlorentineFamilies.PUCCI] = [

    ]

    adj_list[FlorentineFamilies.PAZZI] = [
        FlorentineFamilies.SALVIATI
    ]

    return adj_list

