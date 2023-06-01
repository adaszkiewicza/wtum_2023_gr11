import wget
import zipfile

print('Make sure you have all packages needed by main.py (and download automatically if needed) by running:')
print('\tpip install -r requirements.txt')
print('\n\nDownloading models now...')

models_diff_filename = wget.download('https://github.com/adaszkiewicza/wtum_2023_gr11/releases/download/downloading/models_diff.zip')
models_gan_filename = wget.download('https://github.com/adaszkiewicza/wtum_2023_gr11/releases/download/downloading/models_gan.zip')

print('Models downloaded. Unzipping...')

for file_to_untar in [models_diff_filename, models_gan_filename]:
    with zipfile.ZipFile(file_to_untar, 'r') as zip_ref:
        zip_ref.extractall()

print('Success!')
