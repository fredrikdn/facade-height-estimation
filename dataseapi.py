import psycopg2


def openpgdb(database="norwaybuildings"):
    # connect pgsql database
    pgconn = psycopg2.connect(database=database, user="postgres", password="123456", host="vgi.ibm.ntnu.no", port="5432")
    # open cursor
    cur = pgconn.cursor()
    return pgconn, cur


def searchBuildings(cur, building_id):
    sql = '''select ST_AsGeoJSON(geom)::json, height from building where osm_id='{}' '''.format(building_id)

    cur.execute(sql)
    records = cur.fetchall()

    for row in records:
        footprint = row[0]
        height = row[1]
        print("Foorprint: ", footprint)
        print("Height: ", height)


#def findLocation(cur, location):



if __name__ == '__main__':
    pgconn, cur = openpgdb()

    building_id = '30285315'
    searchBuildings(cur, building_id)