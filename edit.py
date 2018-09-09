import blockchain,argparse,os

parser = argparse.ArgumentParser(description="An editor with blockchain history!")
parser.add_argument("filename",help="The file to be edited.")
args = parser.parse_args()

chain = blockchain.Chain(args.filename+".chain.json",blockchain.Block(0,"",""))
os.system(os.environ.get("EDITOR","nano")+" "+args.filename)
with open(args.filename) as f:
	contents = f.read()
if chain.blocks[-1].data != contents:
	chain.add_block(contents)
	chain.save()
