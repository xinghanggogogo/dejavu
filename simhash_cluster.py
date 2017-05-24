from db import KugouKrcSong
import urllib2

kcloud = 'http://kcloud.v2.service.ktvdaren.com/MusicService.aspx?op=getksdownurl&timeout=30&url='
    
def get_word_hash(word):
    if word == "":
        return 0
    else:
        x = ord(word[0]) << 7
        m = 1000003
        mask = 2 ** 128 - 1
        for c in word:
            x = ((x * m) ^ ord(c)) & mask
        x ^= len(word)
        if x == -1:
            x = -2
        x = bin(x).replace('0b', '').zfill(64)[-64:]
        return x


def get_sim_hash(content):
    content = content.replace(' ', '')
    content = content.replace('\n', '')

    seg = jieba.cut(content, cut_all=True)
    key_word = jieba.analyse.extract_tags(''.join(seg), topK=20, withWeight=True, allowPOS=())
    print(key_word)

    res_array = '0' * 64
    res_array = [int(item) for item in res_array]

    for word, weight in key_word:
        word_hash = get_word_hash(word)
        weight_list = []
        for i in word_hash:
            weight_list_value = weight if int(i) else -weight
            weight_list.append(weight_list_value)
        res_array += array(weight_list)

    sim_hash = ''
    for item in res_array.tolist():
        hash_code = '1' if int(item) else '0'
        sim_hash += hash_code
    return sim_hash

for i in range(0, 1):
    anchor = 1000 * (i+1)
    songs = KugouKrcSong.select().where((KugouKrcSong.id>i)&(KugouKrcSong.id<=anchor))  

    for song in songs:
        print song.krc_link
        krc_link = song.krc_link 
        krc_link = kcloud + krc_link 
        req = urllib2.Request(krc_link) 
        res = urllib2.urlopen(req).read()
        res = json.loads(res)
        download_link = res.get('result')
        req = urllib2.Request(download_link) 
        txt = urllib2.urlopen(req).read()

        sim_hash = get_sim_hash(txt)
        query =
        KugouKrcSong.update(sim_hash=sim_hash).where(KugouKrcSong.id=song.id)
