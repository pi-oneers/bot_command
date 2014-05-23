rm -rf docs
sphinx-apidoc -F -o docs pibot 	
echo "sys.path.insert(0, os.path.abspath('../'))" >> docs/conf.py
