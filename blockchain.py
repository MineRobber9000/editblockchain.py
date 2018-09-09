import hashlib, json
import os.path as fs

class Block:
	def __init__(self,index,data,prev_hash):
		self.__dict__.update(locals())

	@property
	def hash(self):
		sha = hashlib.sha256()
		sha.update(str(self.index).encode("utf-8")+str(self.data).encode("utf-8")+str(self.prev_hash).encode("utf-8"))
		return sha.hexdigest()

	def verify(self,hash):
		return self.hash == hash

class Chain:
	def __init__(self,filename,genesis_block=None):
		self.filename = filename
		if not fs.exists(filename):
			self.blocks = [genesis_block]
			self.save()
		else:
			self.blocks = []
			self.load()

	def load(self):
		self.blocks = []
		with open(self.filename) as f:
			data = json.load(f)
			for block in data["blocks"]:
				b = Block(block["index"],block["data"],block["prev_hash"])
				if not b.verify(block["hash"]):
					raise Exception("Hash of block {!s} doesn't match!".format(b.index))
				self.blocks.append(b)

	def save(self):
		blocks = []
		for block in self.blocks:
			blocks.append(dict(index=block.index,data=block.data,prev_hash=block.prev_hash,hash=block.hash))
		with open(self.filename,"w") as f:
			json.dump(dict(blocks=blocks),f)

	def add_block(self,data):
		self.blocks.append(Block(len(self.blocks),data,self.blocks[-1].hash))
