import os
import tempfile
import json
import pytest

from webdemo import va_asr_demo_web
import logging

logger = logging.getLogger()


@pytest.fixture
def client():

    va_asr_demo_web.app.config['TESTING'] = True
    va_asr_demo_web.app.config['DEBUG'] = True
    with va_asr_demo_web.app.test_client() as client:
        yield client

@pytest.fixture
def wake_word_clips():
    yield [
         ('tests/test_data/r094_s035_d004_maninka__taibou_camara__101_wake_word.wav', 'ma', 1)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__101_wake_word.wav', 'ma', 1)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__101_wake_word.wav', 'pu', 2)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__101_wake_word.wav', 'pu', 2)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__101_wake_word.wav', 'su', 3)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__101_wake_word.wav', 'su', 3)
    ]


@pytest.fixture
def add_contact_clips():
    yield [
         ('tests/test_data/r094_s035_d004_maninka__taibou_camara__201_add_contact.wav', 'ma', 5)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__201_add_contact.wav', 'ma', 5)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__201_add_contact.wav', 'pu', 6)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__201_add_contact.wav', 'pu', 6)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__201_add_contact.wav', 'su', 7)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__201_add_contact.wav', 'su', 7)
    ]


@pytest.fixture
def search_contact_clips():
    yield [
         ('tests/test_data/r094_s035_d004_maninka__taibou_camara__202_search_contact.wav', 'ma', 9)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__202_search_contact.wav', 'ma', 9)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__202_search_contact.wav', 'pu', 10)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__202_search_contact.wav', 'pu', 10)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__202_search_contact.wav', 'su', 11)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__202_search_contact.wav', 'su', 11)
    ]


@pytest.fixture
def contact_name_clips():
    yield [
         ('tests/test_data/r094_s035_d004_maninka__taibou_camara__501_fatoumata.wav',   'na', 80)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__502_mamadou.wav',     'na', 81)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__503_mariama.wav',     'na', 82)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__504_mohamed.wav',     'na', 83)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__505_kadiatou.wav',    'na', 84)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__506_ibrahima.wav',    'na', 85)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__507_aissatou.wav',    'na', 86)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__508_aminata.wav',     'na', 87)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__509_alpha.wav',       'na', 88)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__510_thierno.wav',     'na', 89)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__511_abdoulaye.wav',   'na', 90)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__512_aboubacar.wav',   'na', 91)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__513_amadou.wav',      'na', 92)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__514_fanta.wav',       'na', 93)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__515_mariame.wav',     'na', 94)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__516_oumou.wav',       'na', 95)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__517_ousmane.wav',     'na', 96)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__518_adama.wav',       'na', 97)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__519_marie.wav',       'na', 98)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__520_moussa.wav',      'na', 99)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__521_aissata.wav',     'na', 100)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__522_hawa.wav',        'na', 101)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__523_sekou.wav',       'na', 102)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__524_hadja.wav',       'na', 103)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__525_djenabou.wav',    'na', 104)

        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__501_fatoumata.wav',   'na', 80)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__502_mamadou.wav',     'na', 81)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__503_mariama.wav',     'na', 82)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__504_mohamed.wav',     'na', 83)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__505_kadiatou.wav',    'na', 84)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__506_ibrahima.wav',    'na', 85)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__507_aissatou.wav',    'na', 86)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__508_aminata.wav',     'na', 87)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__509_alpha.wav',       'na', 88)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__510_thierno.wav',     'na', 89)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__511_abdoulaye.wav',   'na', 90)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__512_aboubacar.wav',   'na', 91)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__513_amadou.wav',      'na', 92)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__514_fanta.wav',       'na', 93)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__515_mariame.wav',     'na', 94)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__516_oumou.wav',       'na', 95)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__517_ousmane.wav',     'na', 96)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__518_adama.wav',       'na', 97)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__519_marie.wav',       'na', 98)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__520_moussa.wav',      'na', 99)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__521_aissata.wav',     'na', 100)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__522_hawa.wav',        'na', 101)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__523_sekou.wav',       'na', 102)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__524_hadja.wav',       'na', 103)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__525_djenabou.wav',    'na', 104)

        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__401_mom.wav',         'ma', 73)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__401_mom.wav',         'ma', 73)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__401_mom.wav',           'pu', 74)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__401_mom.wav',           'pu', 74)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__401_mom.wav',            'su', 75)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__401_mom.wav',            'su', 75)

        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__402_dad.wav',         'ma', 77)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__402_dad.wav',         'ma', 77)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__402_dad.wav',           'pu', 78)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__402_dad.wav',           'pu', 78)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__402_dad.wav',            'su', 79)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__402_dad.wav',            'su', 79)
    ]

@pytest.fixture
def digit_clips():
    yield [
         ('tests/test_data/r094_s035_d004_maninka__taibou_camara__301_zero.wav',    'ma', 33)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__302_one.wav',     'ma', 37)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__303_two.wav',     'ma', 41)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__304_three.wav',   'ma', 45)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__305_four.wav',    'ma', 49)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__306_five.wav',    'ma', 53)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__307_six.wav',     'ma', 57)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__308_seven.wav',   'ma', 61)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__309_eight.wav',   'ma', 65)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__310_nine.wav',    'ma', 69)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__301_zero.wav',    'ma', 33)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__302_one.wav',     'ma', 37)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__303_two.wav',     'ma', 41)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__304_three.wav',   'ma', 45)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__305_four.wav',    'ma', 49)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__306_five.wav',    'ma', 53)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__307_six.wav',     'ma', 57)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__308_seven.wav',   'ma', 61)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__309_eight.wav',   'ma', 65)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__310_nine.wav',    'ma', 69)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__301_zero.wav',      'pu', 34)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__302_one.wav',       'pu', 38)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__303_two.wav',       'pu', 42)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__304_three.wav',     'pu', 46)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__305_four.wav',      'pu', 50)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__306_five.wav',      'pu', 54)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__307_six.wav',       'pu', 58)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__308_seven.wav',     'pu', 62)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__309_eight.wav',     'pu', 66)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__310_nine.wav',      'pu', 70)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__301_zero.wav',      'pu', 34)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__302_one.wav',       'pu', 38)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__303_two.wav',       'pu', 42)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__304_three.wav',     'pu', 46)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__305_four.wav',      'pu', 50)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__306_five.wav',      'pu', 54)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__307_six.wav',       'pu', 58)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__308_seven.wav',     'pu', 62)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__309_eight.wav',     'pu', 66)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__310_nine.wav',      'pu', 70)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__301_zero.wav',       'su', 35)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__302_one.wav',        'su', 39)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__303_two.wav',        'su', 43)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__304_three.wav',      'su', 47)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__305_four.wav',       'su', 51)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__306_five.wav',       'su', 55)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__307_six.wav',        'su', 59)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__308_seven.wav',      'su', 63)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__309_eight.wav',      'su', 67)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__310_nine.wav',       'su', 71)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__301_zero.wav',       'su', 35)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__302_one.wav',        'su', 39)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__303_two.wav',        'su', 43)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__304_three.wav',      'su', 47)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__305_four.wav',       'su', 51)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__306_five.wav',       'su', 55)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__307_six.wav',        'su', 59)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__308_seven.wav',      'su', 63)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__309_eight.wav',      'su', 67)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__310_nine.wav',       'su', 71)
    ]

@pytest.fixture
def yes_no_clips():
    yield [
         ('tests/test_data/r094_s035_d004_maninka__taibou_camara__206_yes.wav', 'ma', 25, True)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__206_yes.wav', 'ma', 25, True)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__206_yes.wav',   'pu', 26, True)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__206_yes.wav',   'pu', 26, True)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__206_yes.wav',    'su', 27, True)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__206_yes.wav',    'su', 27, True)
        ,('tests/test_data/r094_s035_d004_maninka__taibou_camara__207_no.wav',  'ma', 29, False)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__207_no.wav',  'ma', 29, False)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__207_no.wav',    'pu', 30, False)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__207_no.wav',    'pu', 30, False)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__207_no.wav',     'su', 31, False)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__207_no.wav',     'su', 31, False)
    ]

@pytest.fixture
def update_contact_clips():
    yield [
         ('tests/test_data/r094_s035_d004_maninka__taibou_camara__203_update_contact.wav',  'ma', 13)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__203_update_contact.wav',  'ma', 13)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__203_update_contact.wav',    'pu', 14)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__203_update_contact.wav',    'pu', 14)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__203_update_contact.wav',     'su', 15)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__203_update_contact.wav',     'su', 15)
    ]

@pytest.fixture
def call_contact_clips():
    yield [
         ('tests/test_data/r094_s035_d004_maninka__taibou_camara__205_call_contact.wav',    'ma', 21)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__205_call_contact.wav',    'ma', 21)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__205_call_contact.wav',      'pu', 22)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__205_call_contact.wav',      'pu', 22)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__205_call_contact.wav',       'su', 23)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__205_call_contact.wav',       'su', 23)
    ]

@pytest.fixture
def delete_contact_clips():
    yield [
         ('tests/test_data/r094_s035_d004_maninka__taibou_camara__204_delete_contact.wav'   ,'ma', 17)
        ,('tests/test_data/r094_s035_d005_maninka__taibou_camara__204_delete_contact.wav'   ,'ma', 17)
        ,('tests/test_data/r095_s035_d004_pular__taibou_camara__204_delete_contact.wav'     ,'pu', 18)
        ,('tests/test_data/r095_s035_d005_pular__taibou_camara__204_delete_contact.wav'     ,'pu', 18)
        ,('tests/test_data/r096_s035_d004_susu__taibou_camara__204_delete_contact.wav'      ,'su', 19)
        ,('tests/test_data/r096_s035_d005_susu__taibou_camara__204_delete_contact.wav'      ,'su', 19)
    ]






def test_home_page(client):
    response = client.get('/')
    assert "Appuiyez sur le boutton pour parler" in str(response.data)



def test_transition_0_1_wake_word(client, wake_word_clips):
    for wake_word_clip in wake_word_clips:
        clip_path, lang, class_id = wake_word_clip
        response = client.post('/asr', data={
            'current_state': 0,
            'current_language': 'none',
            'audiodata': open(clip_path, 'rb')        
        })

        response_json = json.loads(response.data)
        
        assert response_json['class_id'] == class_id
        assert response_json['new_state'] == 1
        assert response_json['new_language'] == lang


def test_transition_1_2_add_contact(client, add_contact_clips):
    for wake_word_clip in add_contact_clips:
        clip_path, lang, class_id = wake_word_clip
        response = client.post('/asr', data={
            'current_state': 1,
            'current_language': lang,
            'audiodata': open(clip_path, 'rb')        
        })

        response_json = json.loads(response.data)
        
        assert response_json['class_id'] == class_id
        assert response_json['new_state'] == 2
        assert response_json['new_language'] == lang


def test_transition_1_3_search_contact(client, search_contact_clips):
    for wake_word_clip in search_contact_clips:
        clip_path, lang, class_id = wake_word_clip
        response = client.post('/asr', data={
            'current_state': 1,
            'current_language': lang,
            'audiodata': open(clip_path, 'rb')        
        })

        response_json = json.loads(response.data)
        
        assert response_json['class_id'] == class_id
        assert response_json['new_state'] == 3
        assert response_json['new_language'] == lang


def test_transition_2_4_add_contact_name(client, contact_name_clips):
    for current_language in ['ma', 'pu', 'su']:
        for contact_name_clip in contact_name_clips:
            clip_path, clip_lang, class_id = contact_name_clip

            if clip_lang != 'na' and clip_lang != current_language:
                continue

            response = client.post('/asr', data={
                'current_state': 2,
                'current_language': current_language,
                'audiodata': open(clip_path, 'rb')        
            })

            response_json = json.loads(response.data)
            
            assert response_json['class_id'] == class_id
            assert response_json['new_state'] == 4
            assert response_json['new_language'] == current_language


def test_transition_3_7_search_contact_name(client, contact_name_clips):
    for current_language in ['ma', 'pu', 'su']:
        for contact_name_clip in contact_name_clips:
            clip_path, clip_lang, class_id = contact_name_clip

            if clip_lang != 'na' and clip_lang != current_language:
                continue

            response = client.post('/asr', data={
                'current_state': 3,
                'current_language': current_language,
                'audiodata': open(clip_path, 'rb')        
            })

            response_json = json.loads(response.data)
            
            assert response_json['class_id'] == class_id
            assert response_json['new_state'] == 7
            assert response_json['new_language'] == current_language


def test_transition_4_5_add_contact_number(client, digit_clips):
    for digit_clip in digit_clips:
        clip_path, clip_lang, class_id = digit_clip

        response = client.post('/asr', data={
            'current_state': 4,
            'current_language': clip_lang,
            'audiodata': open(clip_path, 'rb')        
        })

        response_json = json.loads(response.data)
        
        assert response_json['class_id'] == class_id
        assert response_json['new_state'] == 5
        assert response_json['new_language'] == clip_lang


def test_transition_confirm_6_9_11(client, yes_no_clips):
    for current_state, state_if_yes, state_if_no in [(5, 6, 0), (8, 9, 0), (10, 11, 0)]:
        for yes_no_clip in yes_no_clips:
            clip_path, clip_lang, class_id, confirm_yes = yes_no_clip

            response = client.post('/asr', data={
                'current_state': current_state,
                'current_language': clip_lang,
                'audiodata': open(clip_path, 'rb')        
            })

            response_json = json.loads(response.data)
            
            assert response_json['class_id'] == class_id
            assert response_json['new_state'] == (state_if_yes if confirm_yes else state_if_no)
            assert response_json['new_language'] == clip_lang


def test_transition_7_2_update_contact(client, update_contact_clips):
    for update_contact_clip in update_contact_clips:
        clip_path, clip_lang, class_id = update_contact_clip

        response = client.post('/asr', data={
            'current_state': 7,
            'current_language': clip_lang,
            'audiodata': open(clip_path, 'rb')        
        })

        response_json = json.loads(response.data)
        
        assert response_json['class_id'] == class_id
        assert response_json['new_state'] == 2
        assert response_json['new_language'] == clip_lang


def test_transition_7_8_call_contact(client, call_contact_clips):
    for call_contact_clip in call_contact_clips:
        clip_path, clip_lang, class_id = call_contact_clip

        response = client.post('/asr', data={
            'current_state': 7,
            'current_language': clip_lang,
            'audiodata': open(clip_path, 'rb')        
        })

        response_json = json.loads(response.data)
        
        assert response_json['class_id'] == class_id
        assert response_json['new_state'] == 8
        assert response_json['new_language'] == clip_lang


def test_transition_7_10_delete_contact(client, delete_contact_clips):
    for delete_contact_clip in delete_contact_clips:
        clip_path, clip_lang, class_id = delete_contact_clip

        response = client.post('/asr', data={
            'current_state': 7,
            'current_language': clip_lang,
            'audiodata': open(clip_path, 'rb')        
        })

        response_json = json.loads(response.data)
        
        assert response_json['class_id'] == class_id
        assert response_json['new_state'] == 10
        assert response_json['new_language'] == clip_lang
