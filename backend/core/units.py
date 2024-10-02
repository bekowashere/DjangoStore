class DistanceUnits:
    MM = "mm"
    CM = "cm"
    DM = "dm"
    M = "m"
    KM = "km"
    FT = "ft"
    YD = "yd"
    INCH = "inch"

    CHOICES = [
        (MM, "Millimeter"),
        (CM, "Centimeter"),
        (DM, "Decimeter"),
        (M, "Meter"),
        (KM, "Kilometers"),
        (FT, "Feet"),
        (YD, "Yard"),
        (INCH, "Inch"),
    ]

class WeightUnits:
    G = "g"
    LB = "lb"
    OZ = "oz"
    KG = "kg"
    TONNE = "tonne"

    CHOICES = [
        (G, "Gram"),
        (LB, "Pound"),
        (OZ, "Ounce"),
        (KG, "kg"),
        (TONNE, "Tonne"),
    ]


def prepare_all_units_dict():
    measurement_dict = {
        unit.upper(): unit
        for unit_choices in [
            DistanceUnits.CHOICES,
            WeightUnits.CHOICES,
        ]
        for unit, _ in unit_choices
    }
    return dict(measurement_dict, CHOICES=[(v, v) for v in measurement_dict.values()])


MeasurementUnits = type("MeasurementUnits", (object,), prepare_all_units_dict())