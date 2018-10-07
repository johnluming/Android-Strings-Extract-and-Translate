from googletrans import Translator
import xml.etree.ElementTree as et
import os
import errno

FILE_TO_TRANSLATE = 'strings_app_name.xml'
create_new_dirs = False
res_folder = r'C:\Users\John\AndroidStudioProjects\musicalarm\app\src\main\res'
output_filename = 'strings_google_translate.xml'
test = False
append = False
print_content = False
default_lang_code = 'en'

android_code_to_translate_code = {'jv': 'jw', 'zh-rcn': 'zh-cn', 'zh-rtw': 'zh-tw'}
# within the iso-369-1 set
TRANSLATABLE_LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'hi': 'hindi',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
    'he': 'Hebrew'
}

iso_369_1 = (
"aa",
"ab",
"ae",
"af",
"ak",
"am",
"an",
"ar",
"as",
"av",
"ay",
"az",
"ba",
"be",
"bg",
"bh",
"bi",
"bm",
"bn",
"bo",
"br",
"bs",
"ca",
"ce",
"ch",
"co",
"cr",
"cs",
"cu",
"cv",
"cy",
"da",
"de",
"dv",
"dz",
"ee",
"el",
"en",
"eo",
"es",
"et",
"eu",
"fa",
"ff",
"fi",
"fj",
"fo",
"fr",
"fy",
"ga",
"gd",
"gl",
"gn",
"gu",
"gv",
"ha",
"he",
"hi",
"ho",
"hr",
"ht",
"hu",
"hy",
"hz",
"ia",
"id",
"ie",
"ig",
"ii",
"ik",
"io",
"is",
"it",
"iu",
"ja",
"jv",
"ka",
"kg",
"ki",
"kj",
"kk",
"kl",
"km",
"kn",
"ko",
"kr",
"ks",
"ku",
"kv",
"kw",
"ky",
"la",
"lb",
"lg",
"li",
"ln",
"lo",
"lt",
"lu",
"lv",
"mg",
"mh",
"mi",
"mk",
"ml",
"mn",
"mr",
"ms",
"mt",
"my",
"na",
"nb",
"nd",
"ne",
"ng",
"nl",
"nn",
"no",
"nr",
"nv",
"ny",
"oc",
"oj",
"om",
"or",
"os",
"pa",
"pi",
"pl",
"ps",
"pt",
"qu",
"rm",
"rn",
"ro",
"ru",
"rw",
"sa",
"sc",
"sd",
"se",
"sg",
"si",
"sk",
"sl",
"sm",
"sn",
"so",
"sq",
"sr",
"ss",
"st",
"su",
"sv",
"sw",
"ta",
"te",
"tg",
"th",
"ti",
"tk",
"tl",
"tn",
"to",
"tr",
"ts",
"tt",
"tw",
"ty",
"ug",
"uk",
"ur",
"uz",
"ve",
"vi",
"vo",
"wa",
"wo",
"xh",
"yi",
"yo",
"za",
"zh",
"zu"
)

def get_lang_codes_in_res(res_folder):
    lang_codes_in_res = set()
    for subfolder in os.listdir(res_folder):
        # len('values-') == 7, len('values-fr') == 9, len('values-zh-rCN') == 13
        if subfolder[:7] == 'values-':
            if len(subfolder) == 9 or (len(subfolder) > 9 and subfolder[9] == '-'):
                code = subfolder[7:9]
                if code in iso_369_1:
                    lang_codes_in_res.add(code)
            if len(subfolder) == 13 or (len(subfolder) > 13 and subfolder[13] == '-'):
                code = subfolder[7:13]
                if code.lower() in ('zh-rcn', 'zh-rtw', 'zh-rhk', 'zh-rsg', 'zh-rmo'):
                    lang_codes_in_res.add(code)
    if default_lang_code in lang_codes_in_res:
        lang_codes_in_res.remove(default_lang_code)
    return lang_codes_in_res

translator = Translator()

files_written = 0

def output_translated_strings(output_path, dest_lang_code):
    # tree tree and root of output
    if os.path.isfile(output_path) and append:
        tree_out = et.parse(output_path)
        resources_out = tree_out.getroot()
    else:
        resources_out = et.Element('resources')
        tree_out = et.ElementTree(resources_out)

    tree_in = et.parse(FILE_TO_TRANSLATE)
    resources_in = tree_in.getroot()
    for string in resources_in.findall('string'):
        text = string.text
        text_translated = translator.translate(text, src=default_lang_code, dest=dest_lang_code).text
        text_translated_back = translator.translate(text_translated, src=dest_lang_code, dest=default_lang_code).text

        # postfix = ''
        # if text_translated.lower() == text_translated_back.lower():
        #     postfix = '_stable'

        string_translated = et.SubElement(resources_out, 'string', attrib=string.attrib)
        string_translated.text = text_translated
        if text_translated.lower() != text_translated_back.lower():
            string_translated_back = et.SubElement(resources_out, 'string', attrib={'name': string.get('name') + '_translated_back'})
            string_translated_back.text = text_translated_back

    global files_written
    files_written += 1

    if append:
        print('Append to: ' + output_path)
    else:
        print('Write to: ' + output_path)

    if print_content:
        print(et.tostring(resources_out, encoding='utf-8'))

    if not test:
        # need to create intermediate directories if they don't exist, for how to, visit:
        # https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
        if not os.path.exists(os.path.dirname(output_path)):
            try:
                os.makedirs(os.path.dirname(output_path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        tree_out.write(output_path, encoding='utf-8', xml_declaration=True)



lang_codes_in_res = get_lang_codes_in_res(res_folder)
for code in lang_codes_in_res:
    if (code in TRANSLATABLE_LANGUAGES) or code.lower() in ('zh', 'zh-rcn', 'zh-rtw', 'zh-rhk', 'zh-rsg', 'zh-rmo', 'jv'):
        values_folder = 'values-' + code
        output_path = os.path.join(res_folder, values_folder, output_filename)

        if code.lower() in ('zh', 'zh-rcn', 'zh-rsg'):
            translate_code = 'zh-cn'
        elif code.lower() in ('zh-rtw', 'zh-rhk', 'zh-rmo'):
            translate_code = 'zh-tw'
        elif code.lower() == 'jv':
            translate_code = 'jw'
        else:
            translate_code = code

        output_translated_strings(output_path, translate_code)

if test:
    print('files written in test: ' + str(files_written))
else:
    print('files written: ' + str(files_written))