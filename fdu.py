# -*- encoding: utf-8 -*-
import warnings
import json
import urllib2
import urllib
import os

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer
warnings.filterwarnings("ignore")
with open("dejavu.cnf") as f:
    config = json.load(f)
djv = Dejavu(config)

from pyelasticsearch import ElasticSearch
es = ElasticSearch(urls='http://106.75.97.4', 
                   username='elastic',
                   password='changeme')

from db import ThunderSong, KugouKrcSong, FingerPrints, DejavuSongs 

kcloud = 'http://kcloud.v2.service.ktvdaren.com/MusicService.aspx?op=getksdownurl&timeout=30&url='
internal_url= 'o2omusic.ks3-cn-beijing-internal.ksyun.com'
out_url = 'o2omusic.ks3-cn-beijing.ksyun.com'

for _id in range(1000, 1001):
    thunder_song = ThunderSong.get(ThunderSong.id == _id)
    thunder_name = thunder_song.name
    thunder_duration = thunder_song.duration
    print 100 * '-'
    print thunder_name

    # _download_link = thunder_song.download_link
    # url = kcloud + _download_link 
    # req = urllib2.Request(url) 
    # res = urllib2.urlopen(req)
    # res = res.read()
    # res = json.loads(res)
    # download_link = res.get('result')
    # urllib.urlretrieve(download_link,'t_music/'+thunder_name+'.ts')

    es_songs = es.search(index='song',
                         size=3,
                         query={'query': {
                             'match': {'name': thunder_name}
                         }}
                        )    
    
    es_songs = es_songs['hits']['hits']
    es_songs = [item['_source'] for item in es_songs]

    for item in es_songs:

        print item.get('id')
        print item.get('name')
        print item.get('artist')
        o2o_id = item.get('id')
        o2o_name = item.get('name')

        # kugou_krc_song = KugouKrcSong.get(KugouKrcSong.o2o_id == o2o_id) 
        # _download_link = kugou_krc_song.download_link
        # url = kcloud + _download_link 
        # req = urllib2.Request(url) 
        # res = urllib2.urlopen(req)
        # res = res.read()
        # res = json.loads(res)
        # download_link = res.get('result')
        # print download_link
        # download_link = download_link.replace(internal_url, out_url)
        # print download_link
        # urllib.urlretrieve(download_link,'/data/dejavu/'+str(o2o_id)+'$'+o2o_name+'.mp3')

    print 100 * '*'                         
    djv.fingerprint_directory("/data/dejavu", [".mp3"])

    print 100 * '*'
    dejavu_song = djv.recognize(FileRecognizer, "t_music/地球好危险啊(HD).ts")
    o2o_id = dejavu_song.get('song_name').split('$')[0]
    confidence = dejavu_song.get('confidence')
    print dejavu_song.get('song_name')
    print o2o_id
    print confidence    
        
    # q = FingerPrints.delete()
    # q.execute()
    # q = DejavuSongs.delete()
    # q.execute()

    filelist=[]
    dir="/data/dejavu"
    filelist=os.listdir(dir)
    for f in filelist:
        filepath = os.path.join(dir,f)
        os.remove(filepath)
        print filepath + " removed!" 
