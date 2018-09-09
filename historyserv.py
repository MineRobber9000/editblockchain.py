from flask import *
import blockchain

FILE = "test.txt"
chain = blockchain.Chain(FILE+".chain.json",blockchain.Block(0,"",""))
app = Flask(__name__)

@app.route("/")
def base():
	chain.load()
	return render_template("file.html",hashes=[block.hash[:8] for block in chain.blocks if block.data != ""],filename=FILE)

@app.route("/<string:hash>")
def byhash(hash):
	chain.load()
	if len(hash)>8: return abort(400)
	for i in range(chain.blocks[-1].index,-1,-1):
		if chain.blocks[i].hash[:8]==hash:
			return Response(chain.blocks[i].data,mimetype="text/plain")
	return abort(404)

if __name__=="__main__":
	app.run(port=8000)
