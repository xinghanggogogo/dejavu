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
    sim_hash = pw.CharField()

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
