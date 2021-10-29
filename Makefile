.PHONY: all clean zip

all: zip

zip: build.zip

build.zip: src/* pygments.tgz
	rm -f $@
	rm -f src/meta.json
	rm -rf src/__pycache__
	( mkdir src/vendor; cd src/vendor; mkdir pygments; cd pygments; tar xf ../../../pygments.tgz --strip-components=1 pygments-2.10.0 )
	( cd src/; zip -r ../$@ * )
	cp build.zip fhighlight.ankiaddon

pygments.tgz:
	curl -L -o pygments.tgz https://github.com/pygments/pygments/archive/refs/tags/2.10.0.tar.gz

clean:
	rm -f *.pyc
	rm -f src/*.pyc
	rm -f src/__pycache__
	rm -f build.zip
	rm -f fhighlight.ankiaddon
