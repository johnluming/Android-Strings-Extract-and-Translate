import xml.etree.ElementTree as et
import os
import errno

res_folder_in = r"C:\Users\John\Downloads\settings\res"
res_folder_out = r"C:\Users\John\AndroidStudioProjects\musicalarm\app\src\main\res"
OUTPUT_FILENAME = 'strings_04.xml'
STRINGS = (
"vpn_version")
STRING_ARRAYS = {
}
STRINGS_IN_STRING_ARRAY = {
}

test = False
append = False
print_content = False

et.register_namespace("xliff", "urn:oasis:names:tc:xliff:document:1.2")
files_written = 0

# scan for all values folders
for subfolder in os.listdir(res_folder_in):

    # discovered a values folder
    if subfolder[:6] == 'values':
        values_folder = subfolder

        output_path = os.path.join(res_folder_out, values_folder, OUTPUT_FILENAME)
        # get tree and root of output file
        if os.path.isfile(output_path) and append:
            tree_out = et.parse(output_path)
            resources_out = tree_out.getroot()
        else:
            resources_out = et.Element('resources')
            tree_out = et.ElementTree(resources_out)

        extraction_discovered = False

        # scan all files in the values folder
        path_values_folder_in = os.path.join(res_folder_in, values_folder)
        for filename_in in os.listdir(path_values_folder_in):

            # get root element of input file
            input_path = os.path.join(path_values_folder_in, filename_in)
            tree_in = et.parse(input_path)
            resources_in = tree_in.getroot()

            # scan all elements in the root element of the input file
            for child in resources_in:
                if child.tag == 'string':
                    if child.get('name') in STRINGS:
                        extraction_discovered = True
                        resources_out.append(child)
                elif child.tag == 'string-array':
                    if child.get('name') in STRING_ARRAYS:
                        extraction_discovered = True
                        string_array_out = et.SubElement(resources_out, child.tag, attrib=child.attrib)
                        for item_index in STRING_ARRAYS[child.get('name')]:
                            string_array_out.append(child[item_index])
                    if child.get('name') in STRINGS_IN_STRING_ARRAY:
                        extraction_discovered = True
                        for item_index in STRINGS_IN_STRING_ARRAY[child.get('name')]:
                            string_out = et.SubElement(resources_out, 'string',
                                                       attrib={'name': child.get('name') + '_' + str(item_index).zfill(2)})
                            string_out.text = child[item_index].text

        if extraction_discovered:
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

if test:
    print('files written in test: ' + str(files_written))
else:
    print('files written: ' + str(files_written))

