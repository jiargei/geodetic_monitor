DIMOSY_TACHY_MEASUREMENT_MAP = {
    "tachy_measurement": {
        "_timestamp": {
            "enabled": "true"
        },
        "properties": {
            "id": {"type": "string"},
            "created": {"type": "date",
                        "format": "yyyy-MM-ddTHH:mm:ss"},
            "position": {"type": "string"},
            "target": {"type": "string"},
            "slope_distance": {"type": "double"},
            "horizontal_angle": {"type": "double"},
            "vertical_angle": {"type": "double"},
            "face": {"type": "int"},
            "ppm": {"type": "double"},
            "cross_incline": {"type": "double"},
            "length_incline": {"type": "double"},
            "internal_temperature": {"type": "double"}
        }
    }
}

DIMOSY_TACHY_TEST_MAP = {
    "tachy_test": {
        "_timestamp": {"enabeld": "true"},
        "properties": {
            "id": {"type": "string"},
            "created": {"type": "date",
                        "format": "yyyy-MM-ddTHH:mm:ss"},
            "position": {"type": "string"},
            "target": {"type": "string"},
            "face": {"type": "integer"},
            "easting": {"type": "double"},
            "northing": {"type": "double"},
            "height": {"type": "double"},
        }
    }
}