import json
import pytest

from stokercloud.controller_data import ControllerData, PowerState, NotConnectedException, Unit, Value, State


def test_controller_data():
    test_data = """
    {
        "weatherdata": [
            {
                "id": "weather-city",
                "value": "Sample Kommune",
                "unit": "",
                "name": "",
                "selection": ""
            },
            {
                "id": 1,
                "value": "0.8",
                "unit": "LNG_DEGREE",
                "name": "lng_weather_1",
                "selection": ""
            },
            {
                "id": "2",
                "value": "1.96",
                "unit": "LNG_METERSEC",
                "name": "lng_weather_2",
                "selection": "weather1"
            },
            {
                "id": "3",
                "value": "E",
                "unit": "",
                "name": "lng_weather_3",
                "selection": "weather2"
            },
            {
                "id": "9",
                "value": "100",
                "unit": "LNG_PERCENT",
                "name": "lng_weather_9",
                "selection": "weather3"
            }
        ],
        "boilerdata": [
            {
                "id": "3",
                "value": 0,
                "unit": "LNG_DEGREE",
                "name": "lng_boil_3",
                "selection": "boiler1"
            },
            {
                "id": "5",
                "value": "3.8",
                "unit": "LNG_KW",
                "name": "lng_boil_5",
                "selection": "boiler2"
            },
            {
                "id": "4",
                "value": "14",
                "unit": "LNG_PERCENT",
                "name": "lng_boil_4",
                "selection": "boiler3"
            },
            {
                "id": "6",
                "value": "100",
                "unit": "",
                "name": "lng_boil_6",
                "selection": "boiler4"
            },
            {
                "id": "12",
                "value": "17.6",
                "unit": "LNG_PERCENT",
                "name": "lng_boil_12",
                "selection": "boiler5"
            },
            {
                "id": "14",
                "value": "100",
                "unit": "LNG_PERCENT",
                "name": "lng_boil_14",
                "selection": "boiler6"
            },
            {
                "id": "15",
                "value": "100",
                "unit": "LNG_PERCENT",
                "name": "lng_boil_15",
                "selection": "boiler7"
            },
            {
                "id": "16",
                "value": "100",
                "unit": "LNG_PERCENT",
                "name": "lng_boil_16",
                "selection": "boiler8"
            },
            {
                "id": "9",
                "value": "99.8",
                "unit": "LNG_PERCENT",
                "name": "lng_boil_9",
                "selection": "boiler9"
            }
        ],
        "hopperdata": [
            {
                "id": "2",
                "value": "1300",
                "unit": "LNG_GRAM",
                "name": "lng_hopper_2",
                "selection": "hopper1"
            },
            {
                "id": "3",
                "value": "27.7",
                "unit": "LNG_KG",
                "name": "lng_hopper_3",
                "selection": "hopper2"
            },
            {
                "id": "4",
                "value": "1499",
                "unit": "LNG_KG",
                "name": "lng_hopper_4",
                "selection": "hopper3"
            },
            {
                "id": "7",
                "value": "3.0",
                "unit": "LNG_KW",
                "name": "lng_hopper_7",
                "selection": "hopper4"
            },
            {
                "id": "8",
                "value": "20",
                "unit": "LNG_KW",
                "name": "lng_hopper_8",
                "selection": "hopper5"
            }
        ],
        "dhwdata": [
            {
                "id": "3",
                "value": "6",
                "unit": "LNG_DEGREE",
                "name": "lng_dhw_3",
                "selection": "dhw1"
            },
            {
                "id": "4",
                "value": "N/A",
                "unit": "LNG_PERCENT",
                "name": "lng_dhw_4",
                "selection": "dhw2"
            }
        ],
        "frontdata": [
            {
                "id": "hoppercontent",
                "value": "-1493",
                "unit": "LNG_KG",
                "name": "lng_hopper_1",
                "selection": ""
            },
            {
                "id": "boilertemp",
                "value": "59.9",
                "unit": "LNG_DEGREE",
                "name": "lng_boil_1",
                "selection": ""
            },
            {
                "id": "-wantedboilertemp",
                "value": "62.0",
                "unit": "LNG_DEGREE",
                "name": "lng_boil_2",
                "selection": ""
            },
            {
                "id": "dhw",
                "value": 54.9,
                "unit": "LNG_DEGREE",
                "name": "lng_dhw_1",
                "selection": ""
            },
            {
                "id": "dhwwanted",
                "value": "57",
                "unit": "LNG_DEGREE",
                "name": "lng_dhw_2",
                "selection": ""
            },
            {
                "id": "refoxygen",
                "value": "20.9",
                "unit": "LNG_PERCENT",
                "name": "lng_boil_13",
                "selection": ""
            },
            {
                "id": "refair",
                "value": "0",
                "unit": "LNG_M3HOUR",
                "name": "lng_boil_13",
                "selection": ""
            }
        ],
        "miscdata": {
            "state": {
                "id": "state",
                "value": "state_5",
                "unit": "LNG_KW",
                "name": "",
                "selection": ""
            },
            "clock": {
                "id": "clock",
                "value": "22:30",
                "unit": "",
                "name": "",
                "selection": ""
            },
            "substate": {
                "id": "substate",
                "value": "",
                "unit": "",
                "name": "",
                "selection": ""
            },
            "substatesecs": {
                "id": "substatesecs",
                "value": 0,
                "unit": "",
                "name": "",
                "selection": ""
            },
            "alarm": 0,
            "running": 1,
            "output": 3.8,
            "outputpct": "14",
            "hopper.distance_max": "50",
            "vacuum.min_distance": null,
            "vacuum.max_distance": null,
            "vacuum.output_auger": "0",
            "backpressure": null,
            "hopperdistance": 999
        },
        "leftoutput": {
            "output-1": {
                "val": "OFF",
                "unit": "",
                "image": "1-dhw.png"
            },
            "output-2": {
                "val": "disabled",
                "unit": "",
                "image": "2-pump.png"
            },
            "output-3": {
                "val": "disabled",
                "unit": "",
                "image": "3-weathervalve.png"
            },
            "output-4": {
                "val": "disabled",
                "unit": "",
                "image": "4-weatherpump.png"
            },
            "output-5": {
                "val": "disabled",
                "unit": "%",
                "image": "5-exhaustfan.png"
            },
            "output-6": {
                "val": "disabled",
                "unit": "LNG_KG",
                "image": "6-ashauger.png"
            },
            "output-7": {
                "val": "disabled",
                "unit": "",
                "image": "7-compressor.png"
            },
            "output-8": {
                "val": "disabled",
                "unit": "%",
                "image": "8-weathervalve2.png"
            },
            "output-9": {
                "val": "disabled",
                "unit": "",
                "image": "9-weatherpump2.png"
            }
        },
        "rightoutput": {
            "sunoutput-1": {
                "val": "disabled",
                "unit": "",
                "image": "output-sun-pump.png"
            },
            "sunoutput-2": {
                "val": "disabled",
                "unit": "",
                "image": "output-sun-valve.png"
            }
        },
        "infomessages": [],
        "model": "1",
        "weathercomp": {
            "zone1active": 0,
            "zone2active": 0,
            "zone1-wanted": {
                "val": 0,
                "unit": "LNG_DEGREE"
            },
            "zone1-actual": {
                "val": 999.9,
                "unit": "LNG_DEGREE"
            },
            "zone1-valve": {
                "val": "0",
                "unit": "LNG_PERCENT"
            },
            "zone1-actualref": {
                "val": "0.8",
                "unit": "LNG_DEGREE"
            },
            "zone1-calc": {
                "val": 0.3,
                "unit": "LNG_DEGREE"
            },
            "zone2-wanted": {
                "val": "0.0",
                "unit": "LNG_DEGREE"
            },
            "zone2-actual": {
                "val": "999.9",
                "unit": "LNG_DEGREE"
            },
            "zone2-valve": {
                "val": "0",
                "unit": "LNG_PERCENT"
            },
            "zone2-actualref": {
                "val": "0.8",
                "unit": "LNG_DEGREE"
            },
            "zone2-calc": {
                "val": "0.3",
                "unit": "LNG_DEGREE"
            }
        },
        "notconnected": 0,
        "newuser": 0,
        "serial": "12345",
        "metrics": "EUR"
    }
    """
    cd = ControllerData(json.loads(test_data))

    assert cd.running == PowerState.ON
    assert cd.alarm == PowerState.OFF
    assert cd.serial_number == "12345"
    assert cd.boiler_kwh == Value("3.8", Unit.KWH)
    assert cd.boiler_temperature_current == Value("59.9", Unit.DEGREE)
    assert cd.boiler_temperature_requested == Value("62.0", Unit.DEGREE)
    assert cd.state == State.POWER
    assert cd.consumption_total == Value("1499", Unit.KILO_GRAM)


def test_controller_data_connected():
    test_data = '{"notconnected": 1}'
    with pytest.raises(NotConnectedException):
        ControllerData(json.loads(test_data))