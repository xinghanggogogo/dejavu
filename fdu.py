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
es = ElasticSearch(urls='', 
                   username='elastic',
                   password='changeme')

import peewee as pw
DB = pw.MySQLDatabase("dejavu",
                       host="127.0.0.1",
                       port=3308,
                       user="dbsync",
                       passwd="dbsync123")


class MySQLModel(pw.Model):
    class Meta:
        database = DB


class ThunderSong(MySQLModel):
    id = pw.IntegerField()
    thunder_id = pw.CharField()
    name = pw.CharField()
    artist1 = pw.CharField()
    artist2 = pw.CharField()
    artist3 = pw.CharField()
    artist4 = pw.CharField()
    duration = pw.IntegerField()
    download_link = pw.CharField()
    has_krc = pw.IntegerField()
    dejavu_list = pw.CharField()

    class Meta:
        db_table = 'thunder_song'


class KugouKrcSong(MySQLModel):
    id = pw.IntegerField()
    o2o_id = pw.IntegerField()
    krc_link = pw.CharField()
    download_link = pw.CharField()

    class Meta:
        db_table = 'kugou_krc_song'


class FingerPrints(MySQLModel):
    hash = pw.CharField()
    song_id = pw.IntegerField()
    offset = pw.IntegerField()

    class Meta:
        db_table = 'fingerprints'


class DejavuSongs(MySQLModel):
    song_id = pw.IntegerField()
    song_name = pw.CharField()
    fingerprinted = pw.IntegerField()
    file_sha1 = pw.IntegerField()

    class Meta:
        db_table = 'songs'


DB.connect()

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
    # urllib.urlretrieve(download_link,'mp3/'+thunder_name+'.ts')

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
    dejavu_song = djv.recognize(FileRecognizer, "mp3/地球好危险啊(HD).ts")
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
    dir="/home/work/dejavu/mp3"
    filelist=os.listdir(dir)
    for f in filelist:
        filepath = os.path.join(dir,f)
        os.remove(filepath)
        print filepath+" removed!" 
