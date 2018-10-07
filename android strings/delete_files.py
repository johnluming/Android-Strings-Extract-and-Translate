import os
import shutil

res_folder = r"C:\Users\John\AndroidStudioProjects\musicalarm\app\src\main\res"

# for subfolder in os.listdir(res_folder):
#     subfolder_path = os.path.join(res_folder, subfolder)
#     if subfolder[:6] != 'values':
#         print('remove: ' + subfolder_path)
#         try:
#             shutil.rmtree(subfolder_path)
#         except OSError as e:
#             print("Error: %s - %s." % (e.filename, e.strerror))
#     else:
#         delete_subfolder = True
#         for filename in os.listdir(subfolder_path):
#             if filename in ('arrays.xml', 'plurals.xml', 'strings.xml'):
#                 delete_subfolder = False
#                 break
#
#         if delete_subfolder:
#             print('remove: ' + subfolder_path)
#             shutil.rmtree(subfolder_path)

for subfolder in os.listdir(res_folder):
    if subfolder[:6] == 'values':
        subfolder_path = os.path.join(res_folder, subfolder)
        for file in os.listdir(subfolder_path):
            if file in ('strings_00.xml', 'strings_01.xml'):
                file_path = os.path.join(subfolder_path, file)
                print('remove: ' + file_path)
                os.unlink(file_path)