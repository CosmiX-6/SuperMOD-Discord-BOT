#!/usr/bin/env python3
import os
from .assets import tr_asset_store
from deep_translator import GoogleTranslator
import detectlanguage
from dotenv import load_dotenv

detectlanguage.configuration.api_key = os.getenv('detectlanguage_api_key')

def tr_setup(alias):
    if alias in tr_asset_store.LANGUAGES or alias in tr_asset_store.LANGUAGES.values():
        with open('super_mod/assets/tr_asset_store.py')as read_config:
            confdata = read_config.readlines()
            read_config.close()
        with open('super_mod/assets/tr_asset_store.py','w')as write_config:
            for line in confdata:
                if 'default_lang =' in line:
                    line = line.replace(line,'default_lang = \''+alias+'\'')
                write_config.write(line)
            write_config.close()
        return True
    else:
        return False

def tr_detector(arg):
    return detectlanguage.detect(arg)

def detectors_status():
    return detectlanguage.user_status()

def tr_translate_to(alias,arg):
    if alias in tr_asset_store.LANGUAGES or alias in tr_asset_store.LANGUAGES.values():
        translation = GoogleTranslator(source='auto', target=alias).translate(arg)
        return translation
    else:
        return False

def tr_translate(arg):
    translation = GoogleTranslator(source='auto', target=tr_asset_store.default_lang).translate(arg)
    return translation