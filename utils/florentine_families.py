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
    adj_list[FlorentineFamilies.PERUZZI.value] = [
        FlorentineFamilies.BISCHERI.value,
        FlorentineFamilies.STROZZI.value,
        FlorentineFamilies.CASTELLANI.value
    ]

    adj_list[FlorentineFamilies.BISCHERI.value] = [
        FlorentineFamilies.PERUZZI.value,
        FlorentineFamilies.STROZZI.value,
        FlorentineFamilies.GUADAGNI.value
    ]

    adj_list[FlorentineFamilies.LAMBERTESCHI.value] = [
        FlorentineFamilies.GUADAGNI.value
    ]

    adj_list[FlorentineFamilies.STROZZI.value] = [
        FlorentineFamilies.PERUZZI.value,
        FlorentineFamilies.BISCHERI.value,
        FlorentineFamilies.CASTELLANI.value,
        FlorentineFamilies.RIDOLFI.value
    ]

    adj_list[FlorentineFamilies.GUADAGNI.value] = [
        FlorentineFamilies.BISCHERI.value,
        FlorentineFamilies.LAMBERTESCHI.value,
        FlorentineFamilies.TORNABUONI.value,
        FlorentineFamilies.ALBIZZI.value
    ]

    adj_list[FlorentineFamilies.CASTELLANI.value] = [
        FlorentineFamilies.PERUZZI.value,
        FlorentineFamilies.STROZZI.value,
        FlorentineFamilies.BARBADORI.value
    ]

    adj_list[FlorentineFamilies.RIDOLFI.value] = [
        FlorentineFamilies.STROZZI.value,
        FlorentineFamilies.TORNABUONI.value,
        FlorentineFamilies.MEDICI.value
    ]

    adj_list[FlorentineFamilies.TORNABUONI.value] = [
        FlorentineFamilies.MEDICI.value,
        FlorentineFamilies.GUADAGNI.value,
        FlorentineFamilies.RIDOLFI.value
    ]

    adj_list[FlorentineFamilies.BARBADORI.value] = [
        FlorentineFamilies.CASTELLANI.value,
        FlorentineFamilies.MEDICI.value
    ]

    adj_list[FlorentineFamilies.MEDICI.value] = [
        FlorentineFamilies.RIDOLFI.value,
        FlorentineFamilies.TORNABUONI.value,
        FlorentineFamilies.BARBADORI.value,
        FlorentineFamilies.ALBIZZI.value,
        FlorentineFamilies.ACCIAIUOLI.value,
        FlorentineFamilies.SALVIATI.value,
    ]

    adj_list[FlorentineFamilies.ALBIZZI.value] = [
        FlorentineFamilies.GUADAGNI.value,
        FlorentineFamilies.GINORI.value,
        FlorentineFamilies.MEDICI.value
    ]

    adj_list[FlorentineFamilies.ACCIAIUOLI.value] = [
        FlorentineFamilies.MEDICI.value
    ]

    adj_list[FlorentineFamilies.SALVIATI.value] = [
        FlorentineFamilies.MEDICI.value,
        FlorentineFamilies.PAZZI.value
    ]

    adj_list[FlorentineFamilies.GINORI.value] = [
        FlorentineFamilies.ALBIZZI.value
    ]

    adj_list[FlorentineFamilies.PUCCI.value] = [

    ]

    adj_list[FlorentineFamilies.PAZZI.value] = [
        FlorentineFamilies.SALVIATI.value
    ]

    return adj_list

