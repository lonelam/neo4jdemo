from django.shortcuts import render
from django.http import request, response
from neo4j.v1 import GraphDatabase
import random
# Create your views here.
uri = 'bolt://do.lonelam.me:7687'
auth = ('neo4j', 'password')

def index(req):
    if (req.method == "GET"):
        return render(req, "index.html")
    driver = GraphDatabase.driver(uri, auth=auth)
    ret = []
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for record in tx.run('match p = AllShortestPaths((n{name:"%s"})-[*]-(m{name:"%s"})) return p;' % (req.POST["p1"], req.POST["p2"])):
                ret.append("<hr>")
                for path in record.values():
                    path.start.color = "#%03x" % random.randint(0, 0xFFF)
                    path.end.color = "#%03x" % random.randint(0, 0xFFF)
                    nodes = {path.start.id: path.start, path.end.id:path.end}
                    for nd in path.nodes:
                        nd.color = "#%03x" % random.randint(0, 0xFFF)
                        nodes[nd.id] = nd
                    for rel in path.relationships:
                        if (rel.type == "DIRECTED"):
                            ret.append('<font color="%s">%s</font> <font color="purple">%s</font> <font color="%s">%s</font> \n' % (nodes[rel.start].color,nodes[rel.start].properties['name'], rel.type, nodes[rel.end].color, nodes[rel.end].properties["title"]))
                        else:
                            ret.append('<font color="%s">%s</font> <font color="purple">%s</font> <font color="%s">%s</font> as %s\n' % (nodes[rel.start].color,nodes[rel.start].properties['name'], rel.type, nodes[rel.end].color, nodes[rel.end].properties["title"], rel.properties['name']))
    driver.close()
    return render(req, "index.html", {"response": ret})