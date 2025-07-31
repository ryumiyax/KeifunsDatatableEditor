from __future__ import annotations
import re
from dataclasses import dataclass, fields, field
from typing import List, Dict, Set
import json
import os
from src import encryption, config
from src import constants
from dataclasses import dataclass, field, asdict
from typing import List, Tuple

"""
When adding a new attribute:
    1. If new file: 
        create dataclass, variable in class, parser function,
        add index attribute to indices class, add search function in get_indices(), create index mapping dict
        *also double check if update_uid() is affected
    2. Add attribute to Song class
    3. Update get_song_info()
    4. Update set_song_info()
    5. Update export_datatable() (if new file)
"""


@dataclass
class Song:
    id: str = ""
    uniqueId: int = 0
    songNameList: List[tuple[str, int]] = field(default_factory=lambda: [('', 0), ('', 1), ('', 2), ('', 3), ('', 4)])
    songSubList: List[tuple[str, int]] = field(default_factory=lambda: [('', 0), ('', 1), ('', 2), ('', 3), ('', 4)])
    songDetailList: List[tuple[str, int]] = field(default_factory=lambda: [('', 0), ('', 0), ('', 0), ('', 0), ('', 0)])
    genreNo: int = 0
    songFileName: str = ""
    new: bool = False
    doublePlay: bool = False
    papamama: bool = False
    dancer: str = "000_default"
    branch: List[bool] = field(default_factory=lambda: [False, False, False, False, False])
    star: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    shinuti: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    shinuti_score: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    shinuti_duet: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    shinuti_score_duet: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    onpu_num: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    renda_time: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0, 0.0])
    fuusen_total: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    spike_on: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    music_ai_section: List[int] = field(default_factory=lambda: [5, 5, 5, 5, 5])
    aiOniLevel11: str = ""
    aiUraLevel11: str = ""
    musicOrder: List[tuple[int, int]] = field(
        default_factory=lambda: [(0, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0)])


@dataclass
class DatatableIndices:
    """For keeping track of where each song is"""
    wordlist_name: int = -1
    wordlist_sub: int = -1
    wordlist_detail: int = -1
    musicinfo: int = -1
    music_attribute: int = -1
    music_ai_section: int = -1
    music_usbsetting: int = -1


@dataclass
class MusicinfoItem:
    id: str = ""
    uniqueId: int = 0
    genreNo: int = 0
    songFileName: str = ""
    papamama: bool = False
    branchEasy: bool = False
    branchNormal: bool = False
    branchHard: bool = False
    branchMania: bool = False
    branchUra: bool = False
    starEasy: int = 0
    starNormal: int = 0
    starHard: int = 0
    starMania: int = 0
    starUra: int = 0
    shinutiEasy: int = 0
    shinutiNormal: int = 0
    shinutiHard: int = 0
    shinutiMania: int = 0
    shinutiUra: int = 0
    shinutiEasyDuet: int = 0
    shinutiNormalDuet: int = 0
    shinutiHardDuet: int = 0
    shinutiManiaDuet: int = 0
    shinutiUraDuet: int = 0
    shinutiScoreEasy: int = 0
    shinutiScoreNormal: int = 0
    shinutiScoreHard: int = 0
    shinutiScoreMania: int = 0
    shinutiScoreUra: int = 0
    shinutiScoreEasyDuet: int = 0
    shinutiScoreNormalDuet: int = 0
    shinutiScoreHardDuet: int = 0
    shinutiScoreManiaDuet: int = 0
    shinutiScoreUraDuet: int = 0
    easyOnpuNum: int = 0
    normalOnpuNum: int = 0
    hardOnpuNum: int = 0
    maniaOnpuNum: int = 0
    uraOnpuNum: int = 0
    rendaTimeEasy: float = 0.0
    rendaTimeNormal: float = 0.0
    rendaTimeHard: float = 0.0
    rendaTimeMania: float = 0.0
    rendaTimeUra: float = 0.0
    fuusenTotalEasy: int = 0
    fuusenTotalNormal: int = 0
    fuusenTotalHard: int = 0
    fuusenTotalMania: int = 0
    fuusenTotalUra: int = 0
    spikeOnEasy: int = 0
    spikeOnNormal: int = 0
    spikeOnHard: int = 0
    spikeOnOni: int = 0
    spikeOnUra: int = 0


@dataclass
class MusicAttributeItem:
    id: str = ""
    uniqueId: int = 0
    new: bool = False
    doublePlay: bool = False
    tag1: str = ""
    tag2: str = ""
    tag3: str = ""
    tag4: str = ""
    tag5: str = ""
    tag6: str = ""
    tag7: str = ""
    tag8: str = ""
    tag9: str = ""
    tag10: str = ""
    ensoPartsID1: int = 0
    ensoPartsID2: int = 0
    donBg1p: str = ""
    donBg2p: str = ""
    dancerDai: str = ""
    dancer: str = ""
    danceNormalBg: str = ""
    danceFeverBg: str = ""
    rendaEffect: str = ""
    fever: str = ""
    donBg1p1: str = ""
    donBg2p1: str = ""
    dancerDai1: str = ""
    dancer1: str = ""
    danceNormalBg1: str = ""
    danceFeverBg1: str = ""
    rendaEffect1: str = ""
    fever1: str = ""


@dataclass
class MusicOrderItem:
    genreNo: int = 0
    id: str = ""
    uniqueId: int = 0
    closeDispType: int = 0


@dataclass
class MusicAISectionItem:
    id: str = ""
    uniqueId: int = 0
    easy: int = 5
    normal: int = 5
    hard: int = 5
    oni: int = 5
    ura: int = 5
    oniLevel11: str = ""
    uraLevel11: str = ""


@dataclass
class MusicUsbsettingItem:
    id: str = ""
    uniqueId: int = 0
    usbVer: str = ""


@dataclass
class WordlistItem:
    key: str = ""
    japaneseText: str = ""
    japaneseFontType: int = 0
    englishUsText: str = ""
    englishUsFontType: int = 1
    chineseTText: str = ""
    chineseTFontType: int = 2
    koreanText: str = ""
    koreanFontType: int = 3
    chineseSText: str = ""
    chineseSFontType: int = 4


@dataclass
class SongListItem:
    musicOrderIndex: int = 0
    id: str = ""
    uniqueId: int = 0
    new: bool = False
    closeDispType: int = 0
    title: Tuple[str, str, str, str, str] = "", "", "", "", ""
    sub: Tuple[str, str, str, str, str] = "", "", "", "", ""
    mainGenre: int = 0


MUSIC_ORDER_EXPORT_ORDER = [0, 1, 2, 3, 4, 6, 7, 5]


class Datatable:
    """Datatable class"""
    filepath: str
    uid_musicinfo_index_mapping: Dict[int, int]
    wordlist_indices: Dict[str, Tuple[int, int, int]]
    musicinfo_indices: Dict[str, int]
    music_attribute_indices: Dict[str, int]
    music_ai_section_indices: Dict[str, int]
    music_usbsetting_indices: Dict[str, int]
    wordlist: List[WordlistItem]
    musicinfo: List[MusicinfoItem]
    music_attribute: List[MusicAttributeItem]
    music_order: List[List[MusicOrderItem]]
    music_ai_section: List[MusicAISectionItem]
    music_usbsetting: List[MusicUsbsettingItem]
    songs_not_in_main_genre: Set[str]

    def __init__(self, import_path: str):
        self.filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datatable')
        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)
        files_to_find = ['musicinfo.bin', 'wordlist.bin', 'music_attribute.bin', 'music_ai_section.bin',
                         'music_usbsetting.bin', 'music_order.bin']
        for path, subdirs, files in os.walk(import_path):
            for name in files:
                if name not in files_to_find:
                    continue
                full_path = os.path.join(path, name)
                if os.path.isfile(full_path):
                    encryption.save_file(
                        file=full_path,  # type: ignore
                        outdir=os.path.join(self.filepath, name),
                        encrypt=False
                    )
                files_to_find.remove(name)
        if len(files_to_find) > 0:
            raise Exception(f"Couldn't find: {files_to_find}")
        self.indices = dict()
        self.uid_musicinfo_index_mapping = dict()
        self.wordlist_indices = dict()
        self.songs_not_in_main_genre = set()
        self.parse_musicinfo()
        self.parse_wordlist()
        self.parse_music_attribute()
        self.parse_music_order()
        self.parse_music_AI_section()
        self.parse_music_usbsetting()

    def create_and_append_default_item(self, field_name: str, song_id: str, unique_id: int) -> int:
        if field_name == 'musicinfo':
            self.musicinfo.append(MusicinfoItem(id=song_id, uniqueId=unique_id))
            idx = len(self.musicinfo) - 1
            self.musicinfo_indices[song_id] = idx
            return idx
        elif field_name == 'music_attribute':
            self.music_attribute.append(MusicAttributeItem(id=song_id, uniqueId=unique_id))
            idx = len(self.music_attribute) - 1
            self.music_attribute_indices[song_id] = idx
            return idx
        elif field_name == 'music_ai_section':
            self.music_ai_section.append(MusicAISectionItem(id=song_id, uniqueId=unique_id))
            idx = len(self.music_ai_section) - 1
            self.music_ai_section_indices[song_id] = idx
            return idx
        elif field_name == 'music_usbsetting':
            self.music_usbsetting.append(MusicUsbsettingItem(id=song_id, uniqueId=unique_id))
            idx = len(self.music_usbsetting) - 1
            self.music_usbsetting_indices[song_id] = idx
            return idx
        else:
            raise ValueError(f"Unknown field name: {field_name}")

    def set_index(self, field_name: str, song_id: str):
        if field_name == 'musicinfo':
            self.musicinfo_indices[song_id] = len(self.musicinfo)
        elif field_name == 'music_attribute':
            self.music_attribute_indices[song_id] = len(self.music_attribute)
        elif field_name == 'music_ai_section' or field_name == 'music_usbsetting':
            return
        else:
            raise ValueError(f"Unknown field name: {field_name}")

    def get_wordlist_indices(self, id: str) -> Tuple[int, int, int]:
        if id in self.wordlist_indices:
            return self.wordlist_indices[id]
        wordlist_name_index = -1
        wordlist_sub_index = -1
        wordlist_detail_index = -1
        for i, e in enumerate(self.wordlist):
            if e.key == f"song_{id}":  # You can't use f strings in switch statement?
                if wordlist_name_index == -1: wordlist_name_index = i
            elif e.key == f"song_sub_{id}":
                if wordlist_sub_index == -1: wordlist_sub_index = i
            elif e.key == f"song_detail_{id}":
                if wordlist_detail_index == -1: wordlist_detail_index = i
            else:
                continue  # No point in checking if condition below if current element isn't a match
            if wordlist_detail_index != -1 and wordlist_sub_index != -1 and wordlist_name_index != -1:
                break
        self.wordlist_indices[id] = wordlist_name_index, wordlist_sub_index, wordlist_detail_index
        return wordlist_name_index, wordlist_sub_index, wordlist_detail_index

    def get_musicinfo_index(self, id: str):
        if id not in self.musicinfo_indices:
            raise KeyError(f"song {id} not found")
        return self.musicinfo_indices[id]

    def get_music_attribute_index(self, id: str):
        if id not in self.music_attribute_indices:
            return -1
        return self.music_attribute_indices[id]

    def get_music_ai_section_index(self, id: str):
        if id not in self.music_ai_section_indices:
            return -1
        return self.music_ai_section_indices[id]

    def get_music_usbsetting_index(self, id: str):
        if id not in self.music_usbsetting_indices:
            return -1
        return self.music_usbsetting_indices[id]

    def get_indices(self, id: str) -> DatatableIndices:
        musicinfo_index = self.get_musicinfo_index(id)

        wordlist_name_index, wordlist_sub_index, wordlist_detail_index = self.get_wordlist_indices(id)

        music_attribute_index = self.get_music_attribute_index(id)

        music_ai_section_index = self.get_music_ai_section_index(id)

        music_usbsetting_index = self.get_music_usbsetting_index(id)

        indices = DatatableIndices(
            wordlist_name_index,
            wordlist_sub_index,
            wordlist_detail_index,
            musicinfo_index,
            music_attribute_index,
            music_ai_section_index,
            music_usbsetting_index
        )

        for field in fields(indices):
            if getattr(indices, field.name) == -1:
                if field.name.startswith('wordlist'):
                    new_index = len(self.wordlist)
                    parts = field.name.split('_')
                    if parts[1] == "detail":
                        key = f"song_detail_{id}"
                        self.wordlist_indices[id] = (
                        self.wordlist_indices[id][0], self.wordlist_indices[id][1], new_index)
                    elif parts[1] == "sub":
                        key = f"song_sub_{id}"
                        self.wordlist_indices[id] = (
                        self.wordlist_indices[id][0], new_index, self.wordlist_indices[id][2])
                    else:
                        key = f"song_{id}"
                        self.wordlist_indices[id] = (
                        new_index, self.wordlist_indices[id][1], self.wordlist_indices[id][2])
                    self.wordlist.append(WordlistItem(key=key))
                else:
                    new_index = self.create_and_append_default_item(field.name, id,
                                                                    self.musicinfo[musicinfo_index].uniqueId)
                setattr(indices, field.name, new_index)

        return indices

    def is_song_new(self, id):
        music_attribute_index = self.get_music_attribute_index(id)
        if music_attribute_index == -1:
            return False
        else:
            return self.music_attribute[music_attribute_index].new

    def toggle_song_new(self, id):
        music_attribute_index = self.get_music_attribute_index(id)
        if music_attribute_index == -1:
            return
        self.music_attribute[music_attribute_index].new = not self.music_attribute[music_attribute_index].new

    def select_song_list(self, unique_id_list: List[int]):
        ret = []
        for unique_id in unique_id_list:
            musicinfo_item = self.musicinfo[self.uid_musicinfo_index_mapping[unique_id]]
            song_id = musicinfo_item.id
            title_index, sub_index, _ = self.get_wordlist_indices(song_id)
            title_item = self.wordlist[title_index] if title_index != -1 else WordlistItem()
            sub_item = self.wordlist[sub_index] if sub_index != -1 else WordlistItem()
            ret.append(
                SongListItem(
                    id=song_id,
                    uniqueId=unique_id,
                    title=(title_item.japaneseText,
                           title_item.englishUsText,
                           title_item.chineseTText,
                           title_item.koreanText,
                           title_item.chineseSText),
                    sub=(sub_item.japaneseText,
                         sub_item.englishUsText,
                         sub_item.chineseTText,
                         sub_item.koreanText,
                         sub_item.chineseSText
                         ),
                    mainGenre=musicinfo_item.genreNo
                )
            )
        return ret

    def get_song_list(self, main_genre_only: bool) -> List[List[SongListItem]]:
        ret = [[] for _ in range(8)]
        for genre, genre_order in enumerate(self.music_order):
            for i, e in enumerate(genre_order):
                try:
                    musicinfo = self.musicinfo[self.get_musicinfo_index(e.id)]
                    if musicinfo.genreNo != genre and main_genre_only:
                        continue
                except KeyError:
                    continue

                title_index, sub_index, _ = self.get_wordlist_indices(e.id)
                title_item = self.wordlist[title_index] if title_index != -1 else WordlistItem()
                sub_item = self.wordlist[sub_index] if sub_index != -1 else WordlistItem()
                new = self.is_song_new(e.id)
                ret[genre].append(SongListItem(
                    musicOrderIndex=i,
                    id=e.id,
                    uniqueId=e.uniqueId,
                    new=new,
                    title=(title_item.japaneseText,
                           title_item.englishUsText,
                           title_item.chineseTText,
                           title_item.koreanText,
                           title_item.chineseSText),
                    sub=(sub_item.japaneseText,
                         sub_item.englishUsText,
                         sub_item.chineseTText,
                         sub_item.koreanText,
                         sub_item.chineseSText
                         )
                ))
        if main_genre_only:
            songs_not_in_main_genre = []
            for i, song_id in enumerate(self.songs_not_in_main_genre):
                title_index, sub_index, _ = self.get_wordlist_indices(song_id)
                title_item = self.wordlist[title_index] if title_index != -1 else WordlistItem()
                sub_item = self.wordlist[sub_index] if sub_index != -1 else WordlistItem()
                new = self.is_song_new(song_id)
                unique_id = self.musicinfo[self.musicinfo_indices[song_id]].uniqueId
                songs_not_in_main_genre.append(SongListItem(
                    musicOrderIndex=i,
                    id=song_id,
                    uniqueId=unique_id,
                    new=new,
                    title=(title_item.japaneseText,
                           title_item.englishUsText,
                           title_item.chineseTText,
                           title_item.koreanText,
                           title_item.chineseSText),
                    sub=(sub_item.japaneseText,
                         sub_item.englishUsText,
                         sub_item.chineseTText,
                         sub_item.koreanText,
                         sub_item.chineseSText
                         )
                ))
            ret.append(songs_not_in_main_genre)
        return ret

    def get_song_music_order(self, id: str):
        music_order_indices = [(-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0)]
        for genre_no, genre_list in enumerate(self.music_order):
            for i, e in enumerate(genre_list):
                if e.id == id:
                    music_order_indices[genre_no] = (i, e.closeDispType)
                    break
        return music_order_indices

    def get_song_info(self, id: str) -> Song:
        indices = self.get_indices(id)
        wordlist_name_item = self.wordlist[indices.wordlist_name]
        wordlist_sub_item = self.wordlist[indices.wordlist_sub]
        wordlist_detail_item = self.wordlist[indices.wordlist_detail]
        musicinfo_item = self.musicinfo[indices.musicinfo]
        music_attribute_item = self.music_attribute[indices.music_attribute]
        music_ai_section_item = self.music_ai_section[indices.music_ai_section]

        music_order_indices = self.get_song_music_order(id)

        dancer = "000_default"
        for dancer_key, dancer_data in config.config.dancers.items():
            if (music_attribute_item.ensoPartsID1 == dancer_data['ensoPartsID1'] and
                    music_attribute_item.ensoPartsID2 == dancer_data['ensoPartsID2']):
                dancer = dancer_key
                break

        return Song(
            id=id,
            uniqueId=musicinfo_item.uniqueId,
            songNameList=[
                (wordlist_name_item.japaneseText, wordlist_name_item.japaneseFontType),
                (wordlist_name_item.englishUsText, wordlist_name_item.englishUsFontType),
                (wordlist_name_item.chineseTText, wordlist_name_item.chineseTFontType),
                (wordlist_name_item.koreanText, wordlist_name_item.koreanFontType),
                (wordlist_name_item.chineseSText, wordlist_name_item.chineseSFontType)
            ],
            songSubList=[
                (wordlist_sub_item.japaneseText, wordlist_sub_item.japaneseFontType),
                (wordlist_sub_item.englishUsText, wordlist_sub_item.englishUsFontType),
                (wordlist_sub_item.chineseTText, wordlist_sub_item.chineseTFontType),
                (wordlist_sub_item.koreanText, wordlist_sub_item.koreanFontType),
                (wordlist_sub_item.chineseSText, wordlist_sub_item.chineseSFontType)
            ],
            songDetailList=[
                (wordlist_detail_item.japaneseText, wordlist_detail_item.japaneseFontType),
                (wordlist_detail_item.englishUsText, wordlist_detail_item.englishUsFontType),
                (wordlist_detail_item.chineseTText, wordlist_detail_item.chineseTFontType),
                (wordlist_detail_item.koreanText, wordlist_detail_item.koreanFontType),
                (wordlist_detail_item.chineseSText, wordlist_detail_item.chineseSFontType)
            ],
            genreNo=musicinfo_item.genreNo,
            songFileName=musicinfo_item.songFileName,
            new=music_attribute_item.new,
            doublePlay=music_attribute_item.doublePlay,
            papamama=musicinfo_item.papamama,
            dancer=dancer,
            branch=[
                musicinfo_item.branchEasy,
                musicinfo_item.branchNormal,
                musicinfo_item.branchHard,
                musicinfo_item.branchMania,
                musicinfo_item.branchUra
            ],
            star=[
                musicinfo_item.starEasy,
                musicinfo_item.starNormal,
                musicinfo_item.starHard,
                musicinfo_item.starMania,
                musicinfo_item.starUra
            ],
            shinuti=[
                musicinfo_item.shinutiEasy,
                musicinfo_item.shinutiNormal,
                musicinfo_item.shinutiHard,
                musicinfo_item.shinutiMania,
                musicinfo_item.shinutiUra
            ],
            shinuti_score=[
                musicinfo_item.shinutiScoreEasy,
                musicinfo_item.shinutiScoreNormal,
                musicinfo_item.shinutiScoreHard,
                musicinfo_item.shinutiScoreMania,
                musicinfo_item.shinutiScoreUra
            ],
            shinuti_duet=[
                musicinfo_item.shinutiEasyDuet,
                musicinfo_item.shinutiNormalDuet,
                musicinfo_item.shinutiHardDuet,
                musicinfo_item.shinutiManiaDuet,
                musicinfo_item.shinutiUraDuet
            ],
            shinuti_score_duet=[
                musicinfo_item.shinutiScoreEasyDuet,
                musicinfo_item.shinutiScoreNormalDuet,
                musicinfo_item.shinutiScoreHardDuet,
                musicinfo_item.shinutiScoreManiaDuet,
                musicinfo_item.shinutiScoreUraDuet
            ],

            onpu_num=[
                musicinfo_item.easyOnpuNum,
                musicinfo_item.normalOnpuNum,
                musicinfo_item.hardOnpuNum,
                musicinfo_item.maniaOnpuNum,
                musicinfo_item.uraOnpuNum
            ],
            renda_time=[
                musicinfo_item.rendaTimeEasy,
                musicinfo_item.rendaTimeNormal,
                musicinfo_item.rendaTimeHard,
                musicinfo_item.rendaTimeMania,
                musicinfo_item.rendaTimeUra
            ],
            fuusen_total=[
                musicinfo_item.fuusenTotalEasy,
                musicinfo_item.fuusenTotalNormal,
                musicinfo_item.fuusenTotalHard,
                musicinfo_item.fuusenTotalMania,
                musicinfo_item.fuusenTotalUra
            ],
            spike_on=[
                musicinfo_item.spikeOnEasy,
                musicinfo_item.spikeOnNormal,
                musicinfo_item.spikeOnHard,
                musicinfo_item.spikeOnOni,
                musicinfo_item.spikeOnUra
            ],
            music_ai_section=[
                music_ai_section_item.easy,
                music_ai_section_item.normal,
                music_ai_section_item.hard,
                music_ai_section_item.oni,
                music_ai_section_item.ura
            ],
            aiOniLevel11=music_ai_section_item.oniLevel11,
            aiUraLevel11=music_ai_section_item.uraLevel11,
            musicOrder=music_order_indices
        )

    def get_all_unique_ids(self) -> Set[int]:
        return set(self.uid_musicinfo_index_mapping.keys())

    def set_song_info(self, song_info: Song) -> None:
        indices: DatatableIndices
        try:
            indices = self.get_indices(song_info.id)
        except KeyError:
            # New song
            self.musicinfo_indices[song_info.id] = len(self.musicinfo)
            self.musicinfo.append(MusicinfoItem(id=song_info.id, uniqueId=song_info.uniqueId))
            indices = self.get_indices(song_info.id)

        languages = [
            ('japaneseText', 'japaneseFontType'),
            ('englishUsText', 'englishUsFontType'),
            ('chineseTText', 'chineseTFontType'),
            ('koreanText', 'koreanFontType'),
            ('chineseSText', 'chineseSFontType')
        ]

        # Updating songNameList
        for i, (text_attr, font_attr) in enumerate(languages):
            text, font_type = song_info.songNameList[i]  # Extract both text and font type from the tuple
            setattr(self.wordlist[indices.wordlist_name], text_attr, text)
            setattr(self.wordlist[indices.wordlist_name], font_attr, font_type)

        # Updating songSubList
        for i, (text_attr, font_attr) in enumerate(languages):
            text, font_type = song_info.songSubList[i]  # Extract both text and font type from the tuple
            setattr(self.wordlist[indices.wordlist_sub], text_attr, text)
            setattr(self.wordlist[indices.wordlist_sub], font_attr, font_type)

        # Updating songDetailList
        for i, (text_attr, font_attr) in enumerate(languages):
            text, font_type = song_info.songDetailList[i]  # Extract both text and font type from the tuple
            setattr(self.wordlist[indices.wordlist_detail], text_attr, text)
            setattr(self.wordlist[indices.wordlist_detail], font_attr, font_type)

        if song_info.uniqueId != self.musicinfo[indices.musicinfo].uniqueId:
            self.update_uid(self.musicinfo[indices.musicinfo].uniqueId, song_info.uniqueId)

        self.musicinfo[indices.musicinfo].genreNo = song_info.genreNo
        self.musicinfo[indices.musicinfo].songFileName = song_info.songFileName
        self.musicinfo[indices.musicinfo].papamama = song_info.papamama

        self.music_attribute[indices.music_attribute].new = song_info.new
        self.music_attribute[indices.music_attribute].doublePlay = song_info.doublePlay

        dancer_key = song_info.dancer
        if dancer_key != "000_default":
            # Get the dancer data from the config
            if dancer_key in config.config.dancers:
                dancer_data = config.config.dancers[dancer_key]
            else:
                print(f"Dancer {dancer_key} not found in config.")
                return
            for field, value in dancer_data.items():
                if hasattr(self.music_attribute[indices.music_attribute], field):
                    setattr(self.music_attribute[indices.music_attribute], field, value)
                else:
                    raise Exception(f'MusicAttribute class has no attribute {field}. Check config.json')

        # For branch
        for i, attribute in enumerate(['branchEasy', 'branchNormal', 'branchHard', 'branchMania', 'branchUra']):
            setattr(self.musicinfo[indices.musicinfo], attribute, song_info.branch[i])

        # For star
        for i, attribute in enumerate(['starEasy', 'starNormal', 'starHard', 'starMania', 'starUra']):
            setattr(self.musicinfo[indices.musicinfo], attribute, song_info.star[i])

        # For shinuti
        for i, attribute in enumerate(['shinutiEasy', 'shinutiNormal', 'shinutiHard', 'shinutiMania', 'shinutiUra']):
            setattr(self.musicinfo[indices.musicinfo], attribute, song_info.shinuti[i])

        # For shinuti_score
        for i, attribute in enumerate(
                ['shinutiScoreEasy', 'shinutiScoreNormal', 'shinutiScoreHard', 'shinutiScoreMania', 'shinutiScoreUra']):
            setattr(self.musicinfo[indices.musicinfo], attribute, song_info.shinuti_score[i])

        # For Duet
        for i, attribute in enumerate(
                ['shinutiEasyDuet', 'shinutiNormalDuet', 'shinutiHardDuet', 'shinutiManiaDuet', 'shinutiUraDuet']):
            setattr(self.musicinfo[indices.musicinfo], attribute, (song_info.shinuti_duet)[i])

        for i, attribute in enumerate(
                ['shinutiScoreEasyDuet', 'shinutiScoreNormalDuet', 'shinutiScoreHardDuet', 'shinutiScoreManiaDuet',
                 'shinutiScoreUraDuet']):
            setattr(self.musicinfo[indices.musicinfo], attribute, (song_info.shinuti_score_duet)[i])

        # For onpu_num
        for i, attribute in enumerate(['easyOnpuNum', 'normalOnpuNum', 'hardOnpuNum', 'maniaOnpuNum', 'uraOnpuNum']):
            setattr(self.musicinfo[indices.musicinfo], attribute, song_info.onpu_num[i])

        # For renda_time
        for i, attribute in enumerate(
                ['rendaTimeEasy', 'rendaTimeNormal', 'rendaTimeHard', 'rendaTimeMania', 'rendaTimeUra']):
            setattr(self.musicinfo[indices.musicinfo], attribute, song_info.renda_time[i])

        # For fuusen_total
        for i, attribute in enumerate(
                ['fuusenTotalEasy', 'fuusenTotalNormal', 'fuusenTotalHard', 'fuusenTotalMania', 'fuusenTotalUra']):
            setattr(self.musicinfo[indices.musicinfo], attribute, song_info.fuusen_total[i])

        # For spike_on
        for i, attribute in enumerate(['spikeOnEasy', 'spikeOnNormal', 'spikeOnHard', 'spikeOnOni', 'spikeOnUra']):
            setattr(self.musicinfo[indices.musicinfo], attribute, song_info.spike_on[i])

        # For ai section
        for i, attribute in enumerate(['easy', 'normal', 'hard', 'oni', 'ura']):
            setattr(self.music_ai_section[indices.music_ai_section], attribute, song_info.music_ai_section[i])

        self.music_ai_section[indices.music_ai_section].oniLevel11 = song_info.aiOniLevel11
        self.music_ai_section[indices.music_ai_section].uraLevel11 = song_info.aiUraLevel11

        ### Music Order

        in_main_genre = False
        # Delete from music order
        for genre_list in self.music_order:
            genre_list[:] = [item for item in genre_list if item.id != song_info.id]

        for genre_no, (new_position, close_disp_type) in enumerate(song_info.musicOrder):
            if new_position > -1:
                # Create a new MusicOrderItem for this genre if not already present
                song_item = MusicOrderItem(genreNo=genre_no, id=song_info.id, uniqueId=song_info.uniqueId,
                                           closeDispType=close_disp_type)

                # Insert into the genre list at the specified position
                genre_list = self.music_order[genre_no]
                if new_position >= len(genre_list):
                    # If the new position is beyond the current length of the list, append it
                    genre_list.append(song_item)
                else:
                    # Otherwise, insert at the specific position
                    genre_list.insert(new_position, song_item)
                if genre_no == song_info.genreNo:
                    in_main_genre = True

        if in_main_genre:
            self.songs_not_in_main_genre.discard(song_info.id)
        else:
            self.songs_not_in_main_genre.add(song_info.id)

    def delete_song(self, id: str):
        deleted_indices = self.get_indices(id)

        ## Musicinfo
        del self.musicinfo[deleted_indices.musicinfo]
        del self.musicinfo_indices[id]
        self.songs_not_in_main_genre.discard(id)

        for k, v in self.musicinfo_indices.items():
            if v > deleted_indices.musicinfo:
                self.musicinfo_indices[k] -= 1

        ## Music Attribute
        del self.music_attribute[deleted_indices.music_attribute]
        del self.music_attribute_indices[id]

        for k, v in self.music_attribute_indices.items():
            if v > deleted_indices.music_attribute:
                self.music_attribute_indices[k] -= 1

        ## Music AI Section
        del self.music_ai_section[deleted_indices.music_ai_section]
        del self.music_ai_section_indices[id]

        for k, v in self.music_ai_section_indices.items():
            if v > deleted_indices.music_ai_section:
                self.music_ai_section_indices[k] -= 1

        ## Music USB Setting
        del self.music_usbsetting[deleted_indices.music_usbsetting]
        del self.music_usbsetting_indices[id]

        for k, v in self.music_usbsetting_indices.items():
            if v > deleted_indices.music_usbsetting:
                self.music_usbsetting_indices[k] -= 1

        ## Wordlist
        # Get all indices to delete first
        indices_to_delete = []

        # Find all instances of this songid in wordlist
        for i, item in enumerate(self.wordlist):
            if item.key in [f"song_{id}", f"song_sub_{id}", f"song_detail_{id}"]:
                indices_to_delete.append(i)

        # Sort in reverse order so we can delete without affecting other indices
        indices_to_delete.sort(reverse=True)

        # Delete from wordlist
        for index in indices_to_delete:
            del self.wordlist[index]

        # Delete this song's entry from wordlist_indices
        if id in self.wordlist_indices:
            del self.wordlist_indices[id]

        # Update all subsequent indices in wordlist_indices
        for other_songid, (song_idx, sub_idx, detail_idx) in self.wordlist_indices.items():
            updated_indices = []

            # For each index in the tuple, decrease it by the count of deleted items that came before it
            for idx in [song_idx, sub_idx, detail_idx]:
                reduction = sum(1 for del_idx in indices_to_delete if del_idx < idx)
                updated_indices.append(idx - reduction)

            self.wordlist_indices[other_songid] = tuple(updated_indices)

        # Update uid_musicinfo_index_mapping
        updated_mapping = {}
        for uid, index in self.uid_musicinfo_index_mapping.items():
            if index == deleted_indices.musicinfo:
                continue  # Skip the deleted song
            elif index > deleted_indices.musicinfo:
                updated_mapping[uid] = index - 1
            else:
                updated_mapping[uid] = index
        self.uid_musicinfo_index_mapping = updated_mapping

        # Update music_order list
        for order in self.music_order:
            order[:] = [item for item in order if item.id != id]

    def is_song_id_taken(self, song_id: str) -> bool:
        return song_id in self.musicinfo_indices

    def is_uid_taken(self, uniqueId: int) -> bool:
        if uniqueId in self.uid_musicinfo_index_mapping:
            return True
        for i, e in enumerate(self.musicinfo):
            if e.uniqueId == uniqueId:
                self.uid_musicinfo_index_mapping[e.uniqueId] = i
                return True
        return False

    def update_uid(self, old_uniqueId: int,
                   new_uniqueId: int) -> None:  # snake and camel case in one variable name is a first
        if old_uniqueId not in self.uid_musicinfo_index_mapping:
            for i, e in enumerate(self.musicinfo):
                if e.uniqueId == old_uniqueId:
                    self.uid_musicinfo_index_mapping[e.uniqueId] = i
                    break
        song_id = self.musicinfo[self.uid_musicinfo_index_mapping[old_uniqueId]].id
        indices = self.get_indices(song_id)

        self.musicinfo[self.uid_musicinfo_index_mapping[old_uniqueId]].uniqueId = new_uniqueId
        self.music_attribute[indices.music_attribute].uniqueId = new_uniqueId
        self.music_ai_section[indices.music_ai_section].uniqueId = new_uniqueId
        self.music_usbsetting[indices.music_usbsetting].uniqueId = new_uniqueId
        for l in self.music_order:
            for e in l:
                if e.uniqueId == old_uniqueId:
                    e.uniqueId = new_uniqueId
                    break

        self.uid_musicinfo_index_mapping[new_uniqueId] = self.uid_musicinfo_index_mapping[old_uniqueId]
        del self.uid_musicinfo_index_mapping[old_uniqueId]

    def set_music_order(self, song_list: List[List[SongListItem]]):
        for genre, songs in enumerate(song_list):
            self.music_order[genre].clear()
            for song in songs:
                self.music_order[genre].append(MusicOrderItem(
                    genreNo=genre,
                    id=song.id,
                    uniqueId=song.uniqueId,
                    closeDispType=song.closeDispType
                ))

    def remove_songs_from_music_order(self, unique_id_set: set):
        for genre in range(len(self.music_order)):
            self.music_order[genre] = [
                song for song in self.music_order[genre]
                if song.uniqueId not in unique_id_set
            ]

    def get_songid_from_unique_id(self, unique_id):
        if unique_id not in self.uid_musicinfo_index_mapping:
            raise Exception(f"Unique id {unique_id} not found")
        return self.musicinfo[self.uid_musicinfo_index_mapping[unique_id]].id

    def import_songs(self, source_datatable: Datatable, song_ids_to_import: List[str],
                     unique_id_remappings: Dict[int, int]):
        for song_id in song_ids_to_import:
            song = source_datatable.get_song_info(song_id)
            song.musicOrder = [(-1, 0)] * len(constants.GENRE_MAPPING)
            if song.uniqueId in unique_id_remappings:
                song.uniqueId = unique_id_remappings[song.uniqueId]
            if song.uniqueId in self.uid_musicinfo_index_mapping:
                raise Exception(f"Unique id {song.uniqueId} already exists")
            self.set_song_info(song)

    def parse_musicinfo(self) -> None:
        with open(os.path.join(self.filepath, 'musicinfo.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicinfoItem().__dict__  # Use default values from the dataclass

        self.musicinfo = []
        self.musicinfo_indices = dict()
        # Convert the list of dictionaries to a list of musicinfoItem objects
        i = 0
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the musicinfoItem using the merged dictionary
                musicinfo_item = MusicinfoItem(**full_item)
                self.musicinfo.append(musicinfo_item)
                self.musicinfo_indices[musicinfo_item.id] = i
                self.uid_musicinfo_index_mapping[musicinfo_item.uniqueId] = i
                i += 1
                self.songs_not_in_main_genre.add(musicinfo_item.id)
            except TypeError as e:
                print(f"Failed to create musicinfoItem from {item['id']}: {e}")

    def parse_music_attribute(self) -> None:
        with open(os.path.join(self.filepath, 'music_attribute.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicAttributeItem().__dict__  # Use default values from the dataclass

        self.music_attribute = []
        self.music_attribute_indices = dict()
        # Convert the list of dictionaries to a list of MusicAttributeItem objects
        i = 0
        for item in data_dict['items']:
            try:
                # Remove the 'canPlayUra' field if it exists
                if 'canPlayUra' in item:
                    del item['canPlayUra']
                if 'isNotCopyright' in item:
                    del item['isNotCopyright']

                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the MusicAttributeItem using the merged dictionary
                music_attribute_item = MusicAttributeItem(**full_item)
                self.music_attribute.append(music_attribute_item)
                self.music_attribute_indices[music_attribute_item.id] = i
                i += 1
            except TypeError as e:
                print(f"Failed to create MusicAttributeItem from {item.get('id', 'Unknown')}: {e}")

    def parse_music_order(self) -> None:
        with open(os.path.join(self.filepath, 'music_order.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicOrderItem().__dict__

        self.music_order = [[] for _ in range(len(constants.GENRE_MAPPING))]
        # Convert the list of dictionaries to a list of Item objects
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the MusicOrderItem using the merged dictionary
                music_order_item = MusicOrderItem(**full_item)

                # Append to the appropriate genre list based on genreNo
                genre_no = music_order_item.genreNo
                if 0 <= genre_no < len(self.music_order):
                    self.music_order[genre_no].append(music_order_item)
                    if genre_no == self.musicinfo[self.musicinfo_indices[music_order_item.id]].genreNo:
                        self.songs_not_in_main_genre.discard(music_order_item.id)
                else:
                    print(f"Invalid genreNo {genre_no} for item {music_order_item.id}")
            except TypeError as e:
                print(f"Failed to create MusicOrderItem from {item.get('id', 'unknown')}: {e}")

    def parse_music_AI_section(self) -> None:
        with open(os.path.join(self.filepath, 'music_ai_section.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicAISectionItem().__dict__

        self.music_ai_section = []
        self.music_ai_section_indices = dict()

        # Convert the list of dictionaries to a list of Item objects
        i = 0
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the WordlistItem using the merged dictionary
                music_ai_section_item = MusicAISectionItem(**full_item)
                self.music_ai_section.append(music_ai_section_item)
                self.music_ai_section_indices[music_ai_section_item.id] = i
                i += 1
            except TypeError as e:
                print(f"Failed to create MusicAISectionItem from {item['id']}: {e}")

    def parse_music_usbsetting(self) -> None:
        with open(os.path.join(self.filepath, 'music_usbsetting.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = MusicUsbsettingItem().__dict__

        self.music_usbsetting = []
        self.music_usbsetting_indices = dict()

        # Convert the list of dictionaries to a list of Item objects
        i = 0
        for item in data_dict['items']:
            try:
                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the WordlistItem using the merged dictionary
                music_usbsetting_item = MusicUsbsettingItem(**full_item)
                self.music_usbsetting.append(music_usbsetting_item)
                self.music_usbsetting_indices[music_usbsetting_item.id] = i
                i += 1
            except TypeError as e:
                print(f"Failed to create MusicUsbsettingItem from {item['id']}: {e}")

    def parse_wordlist(self) -> None:
        with open(os.path.join(self.filepath, 'wordlist.json'), 'r', encoding='utf-8') as f:
            data_dict = json.load(f)  # Load JSON data as a Python dictionary

        defaults = WordlistItem().__dict__

        self.wordlist = []
        i = 0
        # Convert the list of dictionaries to a list of WordlistItem objects
        for item in data_dict['items']:
            try:
                # # Remove 'chineseSText' and 'chineseSFontType' if they exist in the JSON data
                # item.pop('chineseSText', None)
                # item.pop('chineseSFontType', None)

                # Use dictionary unpacking with defaults
                full_item = {**defaults, **item}

                # Create the WordlistItem using the filtered dictionary
                wordlist_item = WordlistItem(**full_item)

                # #Ignore blank wordlist items
                # if wordlist_item.japaneseText == "" and wordlist_item.englishUsText == "" and wordlist_item.chineseTText == "" and wordlist_item.koreanText == "" and wordlist_item.chineseSText == "":
                #     continue

                if wordlist_item.key.startswith("song"):
                    song_id = wordlist_item.key.split('_')[-1]  # gets the last part after splitting by '_'

                    if song_id not in self.wordlist_indices:
                        self.wordlist_indices[song_id] = (-1, -1, -1)

                    # Now check each condition
                    if wordlist_item.key.startswith('song_detail_') and self.wordlist_indices[song_id][2] == -1:
                        self.wordlist_indices[song_id] = (
                        self.wordlist_indices[song_id][0], self.wordlist_indices[song_id][1], i)
                    elif wordlist_item.key.startswith('song_sub_') and self.wordlist_indices[song_id][1] == -1:
                        self.wordlist_indices[song_id] = (
                        self.wordlist_indices[song_id][0], i, self.wordlist_indices[song_id][2])
                    elif wordlist_item.key.startswith('song_') and self.wordlist_indices[song_id][0] == -1:
                        self.wordlist_indices[song_id] = (
                        i, self.wordlist_indices[song_id][1], self.wordlist_indices[song_id][2])

                self.wordlist.append(wordlist_item)
                i += 1
            except TypeError as e:
                print(f"Failed to create WordlistItem from {item.get('id', 'unknown')}: {e}")

    def export_datatable(self, folder_path: str) -> None:
        items_list = []
        renda_time_fields = ['rendaTimeEasy', 'rendaTimeNormal', 'rendaTimeHard', 'rendaTimeMania', 'rendaTimeUra']

        for item in self.musicinfo:
            item_dict = asdict(item)

            # Check and cast each rendaTime field
            for field in renda_time_fields:
                if not isinstance(item_dict[field], int) and item_dict[field].is_integer():
                    item_dict[field] = int(item_dict[field])

            items_list.append(item_dict)
        data_dict = {"items": items_list}

        # Write the dictionary to a JSON file
        with open(os.path.join(folder_path, 'musicinfo.json'), 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, separators=(',', ':'))

        # Export wordlist
        items_list = [asdict(item) for item in self.wordlist]
        data_dict = {"items": items_list}
        with open(os.path.join(folder_path, 'wordlist.json'), 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, separators=(',', ':'))

        # Export music_attribute
        items_list = [asdict(item) for item in self.music_attribute]
        data_dict = {"items": items_list}
        with open(os.path.join(folder_path, 'music_attribute.json'), 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, separators=(',', ':'))

        # Export music_ai_section
        items_list = [asdict(item) for item in self.music_ai_section]
        data_dict = {"items": items_list}
        with open(os.path.join(folder_path, 'music_ai_section.json'), 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, separators=(',', ':'))

        # Export music_usbsetting
        items_list = [asdict(item) for item in self.music_usbsetting]
        data_dict = {"items": items_list}
        with open(os.path.join(folder_path, 'music_usbsetting.json'), 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, separators=(',', ':'))

        # Re‑order the sublists according to your export order, then flatten
        ordered_sublists = [self.music_order[i] for i in MUSIC_ORDER_EXPORT_ORDER]
        flattened_music_order = [item for sublist in ordered_sublists for item in sublist]

        # Convert to list of dicts
        items_list = [asdict(item) for item in flattened_music_order]
        data_dict = {"items": items_list}

        # Write to JSON
        with open(os.path.join(folder_path, 'music_order.json'), 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, separators=(',', ':'))

        for path, subdirs, files in os.walk(folder_path):
            for name in files:
                if name not in ['musicinfo.json', 'wordlist.json', 'music_attribute.json', 'music_ai_section.json',
                                'music_usbsetting.json', 'music_order.json']:
                    continue
                full_path = os.path.join(path, name)
                if os.path.isfile(full_path):
                    encryption.save_file(
                        file=full_path,  # type: ignore
                        outdir=full_path,
                        encrypt=True,
                    )
                    os.remove(full_path)
