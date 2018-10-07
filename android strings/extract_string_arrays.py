# import lxml.etree as et
import xml.etree.ElementTree as et
import copy
import os


snooze_duration_entries_keep_items = (
"7668553664977446797",
"4482596794620161030",
"8478276201849960314",
"4038456474851212478",
"6298175579152122770",
"9021860177999278496",
"7224689200902680256",
"4610012663985162123",
"1717028898015659426",
"8058492636464337699",
"2192100038569306041",
"2334964289857921073",
"1573685398431466364",
"2898212818965905529"
)

crescendo_entries_keep_items = (
"7435149932182641128",
"7195451681426992018",
"592917601923801901",
"6997726466563948756",
"248014374051498284",
"8010211657612404516",
"623829984393124488",
"7668553664977446797",
"4482596794620161030",
"8478276201849960314",
"4038456474851212478",
"6298175579152122770",
"8058492636464337699",
"2192100038569306041",
"2334964289857921073",
"1573685398431466364",
"2898212818965905529"
)


AUTO_SILENCE_ENTRIES_TEMPLATE = 'auto_silence_entries_template.xml'

et.register_namespace("xliff", "urn:oasis:names:tc:xliff:document:1.2")


def extract_string_arrays(input_xml, output_xml):
    tree_input = et.parse(input_xml)
    resources_input = tree_input.getroot()

    resources_output = et.Element('resources')
    tree_output = et.ElementTree(resources_output)

    for string_array in resources_input.findall('string-array'):
        if string_array.get('name') == 'snooze_duration_entries':
            string_array_snooze_duration_entries_my_app = copy.deepcopy(string_array)

            string_array_snooze_duration_entries_my_app.set('name', 'snooze_duration_entries_my_app')
            for item in string_array_snooze_duration_entries_my_app.findall('item'):
                if item.get('msgid') not in snooze_duration_entries_keep_items:
                    string_array_snooze_duration_entries_my_app.remove(item)
            resources_output.append(string_array_snooze_duration_entries_my_app)

            string_array_auto_silence_entries_my_app = copy.deepcopy(string_array_snooze_duration_entries_my_app)
            string_array_auto_silence_entries_my_app.set('name', 'auto_silence_entries_my_app')
            item_auto_silence_never = et.Element('item')
            item_auto_silence_never.text = '@string/auto_silence_never'
            string_array_auto_silence_entries_my_app.append(item_auto_silence_never)
            resources_output.append(string_array_auto_silence_entries_my_app)

            string_array_auto_silence_entries_for_music = et.parse(AUTO_SILENCE_ENTRIES_TEMPLATE).getroot()
            for item in string_array_auto_silence_entries_my_app.findall('item'):
                string_array_auto_silence_entries_for_music.append(item)
            resources_output.append(string_array_auto_silence_entries_for_music)

        if string_array.get('name') == 'crescendo_entries':
            string_array_crescendo_entries_my_app = copy.deepcopy(string_array)
            string_array_crescendo_entries_my_app.set('name', 'crescendo_entries_my_app')

            for element in resources_input.findall('string-array'):
                if element.get('name') == 'snooze_duration_entries':
                    for item in element.findall('item'):
                        string_array_crescendo_entries_my_app.append(item)

            for item in string_array_crescendo_entries_my_app.findall('item'):
                if item.get('msgid') not in crescendo_entries_keep_items:
                    string_array_crescendo_entries_my_app.remove(item)

            resources_output.append(string_array_crescendo_entries_my_app)

    tree_output.write(output_xml, encoding='utf-8', xml_declaration=True, method='xml')


res_folder = r'C:\Users\John\AndroidStudioProjects\musicalarm\app\src\main\res'

for subfolder in os.listdir(res_folder):
    if subfolder[:6] == 'values':
        subfolder_path = os.path.join(res_folder, subfolder)
        for file in os.listdir(subfolder_path):
            if file == 'strings.xml':
                input_xml = os.path.join(subfolder_path, file)
                output_xml = os.path.join(subfolder_path, 'strings_arrays.xml')
                extract_string_arrays(input_xml, output_xml)
                print('output: ' + output_xml)