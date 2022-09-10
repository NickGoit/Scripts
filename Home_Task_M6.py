from pathlib import Path
import sys
import os
import zipfile


def normilise(line):
    cyrilic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    latin_symbols = (
     "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
     "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~№ """
    translate_dict = {}
    for cyr, lat in zip(cyrilic_symbols, latin_symbols):
        translate_dict[ord(cyr)] = lat
        translate_dict[ord(cyr.upper())] = lat.upper()
    latin_line = line.translate(translate_dict)
    for char in latin_line:
        if char in punctuation:
            latin_line = latin_line.replace(char, '_')
    return latin_line


def sort_in_dir(dir_path):
    picture_files = []
    video_files = []
    doc_files = []
    music_files = []
    archive_files = []
    unknown_file = []
    unknow_suffix = []
    known_suffix = {'images': ['.JPEG', '.PNG', '.JPG', '.SVG'],
                    'video': ['.AVI', '.MP4', '.MOV', '.MKV'],
                    'documents': ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'],
                    'audio': ['.MP3', '.OGG', '.WAV', '.AMR'],
                    'archives': ['.ZIP', '.GZ', '.TAR']
                    }
    p = Path(dir_path)  # get path object to calling dir

    for file in p.iterdir():  # iterating under each file into directory

        file_path = Path.joinpath(p, file.name)  # make a path to file or dir

        if file.is_dir() and (file.name not in known_suffix.keys()):
            if os.listdir(file_path):  # dir has at least on file
                new_dir_name = normilise(file.name)  # make a new name for a dir
                renamed_dir_path = Path.joinpath(p, new_dir_name)  # create a path to renamed dir
                os.rename(file_path, renamed_dir_path)
                sort_in_dir(renamed_dir_path)
            else:
                os.rmdir(file_path)
        else:
            if file.suffix.upper() in known_suffix['images']:
                images_dir_path = os.path.join(p, 'images')  # create a path to a new dir
                Path(images_dir_path).mkdir(parents=True, exist_ok=True)  # make a new dir based on path to this dir

                file_path_in_new_dir = Path.joinpath(Path(images_dir_path),
                                                     file.name)  # create a file path into a new dir
                os.replace(file_path, file_path_in_new_dir)  # replace file to a new dir

                rename_file = normilise(file.name.replace(file.suffix, '')) + file.suffix  # make a new file name
                renamed_file_path_in_new_dir = Path.joinpath(Path(images_dir_path),
                                                             rename_file)   # create a path to renamed file
                os.rename(file_path_in_new_dir, renamed_file_path_in_new_dir)  # rename file into new dir

                picture_files.append(file.name)  # add to list
            elif file.suffix.upper() in known_suffix['video']:
                video_dir_path = Path.joinpath(p, 'video')
                Path(video_dir_path).mkdir(parents=True, exist_ok=True)

                file_path_in_new_dir = Path.joinpath(Path(video_dir_path), file.name)
                os.replace(file_path, file_path_in_new_dir)

                rename_file = normilise(file.name.replace(file.suffix, '')) + file.suffix
                renamed_file_path_in_new_dir = Path.joinpath(Path(video_dir_path), rename_file)
                os.rename(file_path_in_new_dir, renamed_file_path_in_new_dir)  # rename file into new dir

                video_files.append(file.name)
            elif file.suffix.upper() in known_suffix['documents']:
                document_dir_path = Path.joinpath(p, 'documents')  # create a path to a new dir
                Path(document_dir_path).mkdir(parents=True, exist_ok=True)  # make a new dir based on path to this dir

                file_path_in_new_dir = Path.joinpath(Path(document_dir_path),
                                                     file.name)  # create a file path into a new dir
                os.replace(file_path, file_path_in_new_dir)  # replace file to a new dir

                rename_file = normilise(file.name.replace(file.suffix, '')) + file.suffix  # make a new file name
                renamed_file_path_in_new_dir = Path.joinpath(Path(document_dir_path),
                                                             rename_file)  # create a path to renamed file
                os.rename(file_path_in_new_dir, renamed_file_path_in_new_dir)

                doc_files.append(file.name)
            elif file.suffix.upper() in known_suffix['audio']:
                audio_dir_path = Path.joinpath(p, 'audio')
                Path(audio_dir_path).mkdir(parents=True, exist_ok=True)

                file_path_in_new_dir = Path.joinpath(Path(audio_dir_path), file.name)
                os.replace(file_path, file_path_in_new_dir)

                rename_file = normilise(file.name.replace(file.suffix, '')) + file.suffix  # make a new file name
                renamed_file_path_in_new_dir = Path.joinpath(Path(audio_dir_path),
                                                             rename_file)  # create a path to renamed file
                os.rename(file_path_in_new_dir, renamed_file_path_in_new_dir)

                music_files.append(file.name)

            elif file.suffix.upper() in known_suffix['archives']:
                archive_dir_path = Path.joinpath(p, 'archives')
                Path(archive_dir_path).mkdir(parents=True, exist_ok=True)
                sub_archive_dir_path = Path.joinpath(Path(archive_dir_path), file.name.replace(file.suffix, ''))
                Path(sub_archive_dir_path).mkdir(parents=True, exist_ok=True)
                new_file_path = Path.joinpath(Path(archive_dir_path), file.name)
                os.replace(file_path, new_file_path)
                with zipfile.ZipFile(new_file_path, 'r') as zip_file:
                    zip_file.extractall(sub_archive_dir_path)
                archive_files.append(file.name)
            else:
                unknown_file.append(file.name)
                unknow_suffix.append(file.suffix)


if __name__ == '__main__':
    dir_0 = sys.argv[1]
    sort_in_dir(dir_0)
    print('Done!')
